"""
Secure Finance Dashboard
A local web application for tracking investment, checking, savings, and stock accounts.
Runs locally with authentication and data encryption.
"""

import os
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, List, Optional

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from cryptography.fernet import Fernet
from api_integrations import FinancialDataManager, PlaidAPI, YFinanceAPI

# Configuration
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Database configuration
DATABASE = 'data/finance_dashboard.db'
ENCRYPTION_KEY_FILE = 'data/encryption.key'

# Initialize encryption
def get_or_create_encryption_key():
    """Get or create encryption key for sensitive data"""
    if os.path.exists(ENCRYPTION_KEY_FILE):
        with open(ENCRYPTION_KEY_FILE, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(ENCRYPTION_KEY_FILE), exist_ok=True)
        with open(ENCRYPTION_KEY_FILE, 'wb') as f:
            f.write(key)
        return key

ENCRYPTION_KEY = get_or_create_encryption_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Initialize financial data manager
financial_manager = FinancialDataManager(DATABASE, cipher_suite)

def init_database():
    """Initialize the database with required tables"""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_name TEXT NOT NULL,
            account_type TEXT NOT NULL,
            encrypted_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            transaction_type TEXT NOT NULL,
            date TIMESTAMP NOT NULL,
            encrypted_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def encrypt_data(data: str) -> str:
    """Encrypt sensitive data"""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt sensitive data"""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('register.html')
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                         (username, password_hash))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing all accounts"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get all accounts for the user
    cursor.execute('''
        SELECT id, account_name, account_type, encrypted_data, updated_at 
        FROM accounts WHERE user_id = ?
    ''', (session['user_id'],))
    accounts = cursor.fetchall()
    
    # Decrypt and format account data
    account_data = []
    total_balance = 0
    
    for account in accounts:
        try:
            decrypted_data = json.loads(decrypt_data(account[3]))
            balance = decrypted_data.get('balance', 0)
            total_balance += balance
            
            account_data.append({
                'id': account[0],
                'name': account[1],
                'type': account[2],
                'balance': balance,
                'currency': decrypted_data.get('currency', 'USD'),
                'updated_at': account[4]
            })
        except Exception as e:
            print(f"Error decrypting account {account[0]}: {e}")
    
    conn.close()
    
    return render_template('dashboard.html', 
                         accounts=account_data, 
                         total_balance=total_balance)

@app.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    """Add a new account"""
    if request.method == 'POST':
        account_name = request.form['account_name']
        account_type = request.form['account_type']
        balance = float(request.form['balance'])
        currency = request.form.get('currency', 'USD')
        institution = request.form.get('institution', '')
        account_number = request.form.get('account_number', '')
        
        # Encrypt sensitive data
        account_data = {
            'balance': balance,
            'currency': currency,
            'institution': institution,
            'account_number': account_number
        }
        encrypted_data = encrypt_data(json.dumps(account_data))
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (user_id, account_name, account_type, encrypted_data)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], account_name, account_type, encrypted_data))
        conn.commit()
        conn.close()
        
        flash('Account added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_account.html')

@app.route('/account/<int:account_id>')
@login_required
def account_detail(account_id):
    """View detailed account information"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get account info
    cursor.execute('''
        SELECT account_name, account_type, encrypted_data 
        FROM accounts WHERE id = ? AND user_id = ?
    ''', (account_id, session['user_id']))
    account = cursor.fetchone()
    
    if not account:
        flash('Account not found.', 'error')
        return redirect(url_for('dashboard'))
    
    # Decrypt account data
    account_data = json.loads(decrypt_data(account[2]))
    
    # Get recent transactions
    cursor.execute('''
        SELECT amount, description, transaction_type, date, encrypted_notes
        FROM transactions WHERE account_id = ?
        ORDER BY date DESC LIMIT 20
    ''', (account_id,))
    transactions = cursor.fetchall()
    
    # Decrypt transaction notes
    transaction_data = []
    for trans in transactions:
        notes = ''
        if trans[4]:
            try:
                notes = decrypt_data(trans[4])
            except:
                notes = ''
        
        transaction_data.append({
            'amount': trans[0],
            'description': trans[1],
            'type': trans[2],
            'date': trans[3],
            'notes': notes
        })
    
    conn.close()
    
    return render_template('account_detail.html', 
                         account={'id': account_id, 'name': account[0], 'type': account[1]},
                         account_data=account_data,
                         transactions=transaction_data)

@app.route('/api/account_summary')
@login_required
def account_summary_api():
    """API endpoint for account summary data"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT account_type, encrypted_data FROM accounts WHERE user_id = ?
    ''', (session['user_id'],))
    accounts = cursor.fetchall()
    
    summary = {}
    for account in accounts:
        account_type = account[0]
        try:
            data = json.loads(decrypt_data(account[1]))
            balance = data.get('balance', 0)
            
            if account_type not in summary:
                summary[account_type] = {'count': 0, 'total': 0}
            
            summary[account_type]['count'] += 1
            summary[account_type]['total'] += balance
        except:
            continue
    
    conn.close()
    return jsonify(summary)

@app.route('/api_connections')
@login_required
def api_connections():
    """Manage API connections page"""
    connections = financial_manager.get_api_connections(session['user_id'])
    return render_template('api_connections.html', connections=connections)

@app.route('/add_api_connection', methods=['GET', 'POST'])
@login_required
def add_api_connection():
    """Add new API connection"""
    if request.method == 'POST':
        institution_name = request.form['institution_name']
        api_type = request.form['api_type']
        
        # Collect credentials based on API type
        credentials = {}
        if api_type == 'plaid':
            credentials = {
                'client_id': request.form['plaid_client_id'],
                'secret': request.form['plaid_secret'],
                'access_token': request.form['plaid_access_token']
            }
        elif api_type == 'yfinance':
            # YFinance doesn't need credentials
            credentials = {}
        
        success = financial_manager.add_api_connection(
            session['user_id'], institution_name, api_type, credentials
        )
        
        if success:
            flash('API connection added successfully!', 'success')
        else:
            flash('Failed to add API connection.', 'error')
        
        return redirect(url_for('api_connections'))
    
    return render_template('add_api_connection.html')

@app.route('/sync_data')
@login_required
def sync_data():
    """Synchronize data from all connected APIs"""
    sync_results = financial_manager.sync_account_data(session['user_id'])
    
    if sync_results['success']:
        flash(f"Data synchronized successfully! Updated {sync_results['accounts_updated']} accounts.", 'success')
    else:
        flash('Data synchronization completed with errors.', 'warning')
    
    if sync_results['errors']:
        for error in sync_results['errors']:
            flash(error, 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/stock_data')
@login_required
def stock_data():
    """View stock and crypto holdings"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get stock holdings
    cursor.execute('''
        SELECT symbol, shares, purchase_price, current_price, last_updated
        FROM stock_holdings WHERE user_id = ?
    ''', (session['user_id'],))
    stocks = cursor.fetchall()
    
    # Get crypto holdings
    cursor.execute('''
        SELECT symbol, amount, purchase_price, current_price, last_updated
        FROM crypto_holdings WHERE user_id = ?
    ''', (session['user_id'],))
    crypto = cursor.fetchall()
    
    conn.close()
    
    return render_template('stock_data.html', stocks=stocks, crypto=crypto)

@app.route('/add_stock_holding', methods=['POST'])
@login_required
def add_stock_holding():
    """Add stock holding"""
    symbol = request.form['symbol'].upper()
    shares = float(request.form['shares'])
    purchase_price = float(request.form.get('purchase_price', 0))
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO stock_holdings 
        (user_id, symbol, shares, purchase_price, current_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (session['user_id'], symbol, shares, purchase_price, 0))
    conn.commit()
    conn.close()
    
    flash(f'Added {shares} shares of {symbol}', 'success')
    return redirect(url_for('stock_data'))

@app.route('/add_crypto_holding', methods=['POST'])
@login_required
def add_crypto_holding():
    """Add crypto holding"""
    symbol = request.form['symbol'].upper()
    amount = float(request.form['amount'])
    purchase_price = float(request.form.get('purchase_price', 0))
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO crypto_holdings 
        (user_id, symbol, amount, purchase_price, current_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (session['user_id'], symbol, amount, purchase_price, 0))
    conn.commit()
    conn.close()
    
    flash(f'Added {amount} {symbol}', 'success')
    return redirect(url_for('stock_data'))

@app.route('/delete_api_connection/<int:connection_id>', methods=['POST'])
@login_required
def delete_api_connection(connection_id):
    """Delete an API connection"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Verify the connection belongs to the user
    cursor.execute('''
        SELECT institution_name FROM api_connections 
        WHERE id = ? AND user_id = ?
    ''', (connection_id, session['user_id']))
    
    connection = cursor.fetchone()
    if not connection:
        flash('API connection not found.', 'error')
        conn.close()
        return redirect(url_for('api_connections'))
    
    # Delete the connection
    cursor.execute('''
        DELETE FROM api_connections WHERE id = ? AND user_id = ?
    ''', (connection_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    flash(f'API connection for {connection[0]} has been deleted.', 'success')
    return redirect(url_for('api_connections'))

@app.route('/edit_api_connection/<int:connection_id>', methods=['GET', 'POST'])
@login_required
def edit_api_connection(connection_id):
    """Edit an API connection"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get the connection details
    cursor.execute('''
        SELECT institution_name, api_type, encrypted_credentials 
        FROM api_connections WHERE id = ? AND user_id = ?
    ''', (connection_id, session['user_id']))
    
    connection = cursor.fetchone()
    if not connection:
        flash('API connection not found.', 'error')
        conn.close()
        return redirect(url_for('api_connections'))
    
    # Decrypt credentials for editing
    try:
        credentials = json.loads(decrypt_data(connection[2]))
    except:
        credentials = {}
    
    conn.close()
    
    if request.method == 'POST':
        institution_name = request.form['institution_name']
        api_type = request.form['api_type']
        
        # Collect credentials based on API type
        new_credentials = {}
        if api_type == 'plaid':
            new_credentials = {
                'client_id': request.form['plaid_client_id'],
                'secret': request.form['plaid_secret'],
                'access_token': request.form['plaid_access_token']
            }
        elif api_type == 'yfinance':
            new_credentials = {}
        
        # Update the connection
        encrypted_credentials = encrypt_data(json.dumps(new_credentials))
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE api_connections 
            SET institution_name = ?, api_type = ?, encrypted_credentials = ?, last_sync = NULL
            WHERE id = ? AND user_id = ?
        ''', (institution_name, api_type, encrypted_credentials, connection_id, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('API connection updated successfully!', 'success')
        return redirect(url_for('api_connections'))
    
    return render_template('edit_api_connection.html', 
                         connection={
                             'id': connection_id,
                             'institution_name': connection[0],
                             'api_type': connection[1],
                             'credentials': credentials
                         })

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='127.0.0.1', port=5000)
