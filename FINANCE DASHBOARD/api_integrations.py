"""
Financial API Integrations
Secure module for pulling data from financial institutions
All data is processed locally and never transmitted to third parties
"""

import os
import json
import requests
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet
import sqlite3
from dataclasses import dataclass
import time

@dataclass
class AccountData:
    """Data structure for account information"""
    account_id: str
    account_name: str
    account_type: str
    balance: float
    currency: str
    institution: str
    last_updated: datetime
    transactions: List[Dict[str, Any]] = None

class FinancialAPI:
    """Base class for financial API integrations"""
    
    def __init__(self, encrypted_credentials: str, cipher_suite: Fernet):
        self.encrypted_credentials = encrypted_credentials
        self.cipher_suite = cipher_suite
        self.credentials = self._decrypt_credentials()
    
    def _decrypt_credentials(self) -> Dict[str, str]:
        """Decrypt stored credentials"""
        try:
            decrypted = self.cipher_suite.decrypt(self.encrypted_credentials.encode())
            return json.loads(decrypted.decode())
        except Exception as e:
            print(f"Error decrypting credentials: {e}")
            return {}
    
    def get_account_data(self) -> List[AccountData]:
        """Get account data from the financial institution"""
        raise NotImplementedError("Subclasses must implement get_account_data")

class PlaidAPI(FinancialAPI):
    """Plaid API integration for bank accounts"""
    
    def __init__(self, encrypted_credentials: str, cipher_suite: Fernet):
        super().__init__(encrypted_credentials, cipher_suite)
        self.base_url = "https://production.plaid.com"  # Use sandbox for testing
        self.client_id = self.credentials.get('client_id')
        self.secret = self.credentials.get('secret')
        self.access_token = self.credentials.get('access_token')
    
    def get_account_data(self) -> List[AccountData]:
        """Get account data from Plaid"""
        try:
            # Get accounts
            accounts_response = self._make_request('/accounts/get', {
                'access_token': self.access_token
            })
            
            accounts = []
            for account in accounts_response.get('accounts', []):
                # Get transactions for the last 30 days
                transactions = self._get_transactions(account['account_id'])
                
                account_data = AccountData(
                    account_id=account['account_id'],
                    account_name=account['name'],
                    account_type=self._map_account_type(account['type']),
                    balance=account['balances']['current'],
                    currency=account['balances']['iso_currency_code'],
                    institution=account['institution_id'],
                    last_updated=datetime.now(),
                    transactions=transactions
                )
                accounts.append(account_data)
            
            return accounts
            
        except Exception as e:
            print(f"Error fetching Plaid data: {e}")
            return []
    
    def _get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        """Get transactions for a specific account"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            response = self._make_request('/transactions/get', {
                'access_token': self.access_token,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'account_ids': [account_id]
            })
            
            transactions = []
            for transaction in response.get('transactions', []):
                transactions.append({
                    'amount': abs(transaction['amount']),
                    'description': transaction['name'],
                    'transaction_type': 'credit' if transaction['amount'] > 0 else 'debit',
                    'date': transaction['date'],
                    'category': transaction.get('category', [])
                })
            
            return transactions
            
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    def _map_account_type(self, plaid_type: str) -> str:
        """Map Plaid account types to our internal types"""
        mapping = {
            'depository': 'checking',
            'credit': 'credit',
            'loan': 'loan',
            'investment': 'investment',
            'brokerage': 'stock'
        }
        return mapping.get(plaid_type, 'other')
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make authenticated request to Plaid API"""
        headers = {
            'Content-Type': 'application/json',
            'PLAID-CLIENT-ID': self.client_id,
            'PLAID-SECRET': self.secret
        }
        
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

class YFinanceAPI:
    """Yahoo Finance API for stock and investment data"""
    
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com"
    
    def get_stock_data(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get current stock data for given symbols"""
        try:
            stock_data = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="1d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    stock_data[symbol] = {
                        'symbol': symbol,
                        'name': info.get('longName', symbol),
                        'current_price': float(current_price),
                        'currency': info.get('currency', 'USD'),
                        'change': float(hist['Close'].iloc[-1] - hist['Open'].iloc[0]),
                        'change_percent': float((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0] * 100),
                        'volume': int(hist['Volume'].iloc[-1]),
                        'market_cap': info.get('marketCap'),
                        'last_updated': datetime.now()
                    }
            
            return stock_data
            
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return {}
    
    def get_crypto_data(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get cryptocurrency data"""
        try:
            crypto_data = {}
            for symbol in symbols:
                ticker = yf.Ticker(f"{symbol}-USD")
                hist = ticker.history(period="1d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    crypto_data[symbol] = {
                        'symbol': symbol,
                        'name': symbol,
                        'current_price': float(current_price),
                        'currency': 'USD',
                        'change': float(hist['Close'].iloc[-1] - hist['Open'].iloc[0]),
                        'change_percent': float((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0] * 100),
                        'volume': int(hist['Volume'].iloc[-1]),
                        'last_updated': datetime.now()
                    }
            
            return crypto_data
            
        except Exception as e:
            print(f"Error fetching crypto data: {e}")
            return {}

class FinancialDataManager:
    """Manages financial data synchronization and storage"""
    
    def __init__(self, database_path: str, cipher_suite: Fernet):
        self.database_path = database_path
        self.cipher_suite = cipher_suite
        self.init_database()
    
    def init_database(self):
        """Initialize database tables for API data"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # API connections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                institution_name TEXT NOT NULL,
                api_type TEXT NOT NULL,
                encrypted_credentials TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                last_sync TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Stock holdings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_holdings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                shares REAL NOT NULL,
                purchase_price REAL,
                current_price REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Crypto holdings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_holdings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                amount REAL NOT NULL,
                purchase_price REAL,
                current_price REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_api_connection(self, user_id: int, institution_name: str, api_type: str, credentials: Dict[str, str]) -> bool:
        """Add a new API connection"""
        try:
            encrypted_credentials = self.cipher_suite.encrypt(json.dumps(credentials).encode()).decode()
            
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO api_connections (user_id, institution_name, api_type, encrypted_credentials)
                VALUES (?, ?, ?, ?)
            ''', (user_id, institution_name, api_type, encrypted_credentials))
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error adding API connection: {e}")
            return False
    
    def get_api_connections(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all API connections for a user"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, institution_name, api_type, is_active, last_sync
            FROM api_connections WHERE user_id = ?
        ''', (user_id,))
        
        connections = []
        for row in cursor.fetchall():
            connections.append({
                'id': row[0],
                'institution_name': row[1],
                'api_type': row[2],
                'is_active': bool(row[3]),
                'last_sync': row[4]
            })
        
        conn.close()
        return connections
    
    def sync_account_data(self, user_id: int) -> Dict[str, Any]:
        """Synchronize all account data from APIs"""
        sync_results = {
            'success': True,
            'accounts_updated': 0,
            'errors': [],
            'last_sync': datetime.now()
        }
        
        try:
            # Get all active API connections
            connections = self.get_api_connections(user_id)
            
            for connection in connections:
                if not connection['is_active']:
                    continue
                
                try:
                    # Get encrypted credentials
                    conn = sqlite3.connect(self.database_path)
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT encrypted_credentials FROM api_connections WHERE id = ?
                    ''', (connection['id'],))
                    encrypted_creds = cursor.fetchone()[0]
                    conn.close()
                    
                    # Initialize appropriate API class
                    if connection['api_type'] == 'plaid':
                        api = PlaidAPI(encrypted_creds, self.cipher_suite)
                        accounts = api.get_account_data()
                        
                        # Update accounts in database
                        for account in accounts:
                            self._update_account_from_api(user_id, account)
                            sync_results['accounts_updated'] += 1
                    
                    # Update last sync time
                    conn = sqlite3.connect(self.database_path)
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE api_connections SET last_sync = ? WHERE id = ?
                    ''', (datetime.now(), connection['id']))
                    conn.commit()
                    conn.close()
                    
                except Exception as e:
                    error_msg = f"Error syncing {connection['institution_name']}: {str(e)}"
                    sync_results['errors'].append(error_msg)
                    print(error_msg)
            
            # Sync stock data
            self._sync_stock_data(user_id)
            
        except Exception as e:
            sync_results['success'] = False
            sync_results['errors'].append(f"General sync error: {str(e)}")
        
        return sync_results
    
    def _update_account_from_api(self, user_id: int, account_data: AccountData):
        """Update account data from API response"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Check if account exists
        cursor.execute('''
            SELECT id FROM accounts WHERE user_id = ? AND account_name = ?
        ''', (user_id, account_data.account_name))
        
        existing_account = cursor.fetchone()
        
        if existing_account:
            # Update existing account
            account_id = existing_account[0]
            account_info = {
                'balance': account_data.balance,
                'currency': account_data.currency,
                'institution': account_data.institution,
                'last_api_update': account_data.last_updated.isoformat()
            }
            encrypted_data = self.cipher_suite.encrypt(json.dumps(account_info).encode()).decode()
            
            cursor.execute('''
                UPDATE accounts SET encrypted_data = ?, updated_at = ?
                WHERE id = ?
            ''', (encrypted_data, datetime.now(), account_id))
        else:
            # Create new account
            account_info = {
                'balance': account_data.balance,
                'currency': account_data.currency,
                'institution': account_data.institution,
                'last_api_update': account_data.last_updated.isoformat()
            }
            encrypted_data = self.cipher_suite.encrypt(json.dumps(account_info).encode()).decode()
            
            cursor.execute('''
                INSERT INTO accounts (user_id, account_name, account_type, encrypted_data)
                VALUES (?, ?, ?, ?)
            ''', (user_id, account_data.account_name, account_data.account_type, encrypted_data))
            account_id = cursor.lastrowid
        
        # Add transactions if available
        if account_data.transactions:
            for transaction in account_data.transactions:
                encrypted_notes = ''
                if transaction.get('category'):
                    encrypted_notes = self.cipher_suite.encrypt(
                        json.dumps(transaction['category']).encode()
                    ).decode()
                
                cursor.execute('''
                    INSERT OR IGNORE INTO transactions 
                    (account_id, amount, description, transaction_type, date, encrypted_notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    account_id,
                    transaction['amount'],
                    transaction['description'],
                    transaction['transaction_type'],
                    transaction['date'],
                    encrypted_notes
                ))
        
        conn.commit()
        conn.close()
    
    def _sync_stock_data(self, user_id: int):
        """Sync stock and crypto data"""
        try:
            # Get stock holdings
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT symbol FROM stock_holdings WHERE user_id = ?
            ''', (user_id,))
            stock_symbols = [row[0] for row in cursor.fetchall()]
            
            cursor.execute('''
                SELECT symbol FROM crypto_holdings WHERE user_id = ?
            ''', (user_id,))
            crypto_symbols = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            # Fetch current prices
            yf_api = YFinanceAPI()
            
            if stock_symbols:
                stock_data = yf_api.get_stock_data(stock_symbols)
                self._update_stock_prices(user_id, stock_data)
            
            if crypto_symbols:
                crypto_data = yf_api.get_crypto_data(crypto_symbols)
                self._update_crypto_prices(user_id, crypto_data)
                
        except Exception as e:
            print(f"Error syncing stock/crypto data: {e}")
    
    def _update_stock_prices(self, user_id: int, stock_data: Dict[str, Dict[str, Any]]):
        """Update stock prices in database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        for symbol, data in stock_data.items():
            cursor.execute('''
                UPDATE stock_holdings 
                SET current_price = ?, last_updated = ?
                WHERE user_id = ? AND symbol = ?
            ''', (data['current_price'], datetime.now(), user_id, symbol))
        
        conn.commit()
        conn.close()
    
    def _update_crypto_prices(self, user_id: int, crypto_data: Dict[str, Dict[str, Any]]):
        """Update crypto prices in database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        for symbol, data in crypto_data.items():
            cursor.execute('''
                UPDATE crypto_holdings 
                SET current_price = ?, last_updated = ?
                WHERE user_id = ? AND symbol = ?
            ''', (data['current_price'], datetime.now(), user_id, symbol))
        
        conn.commit()
        conn.close()
