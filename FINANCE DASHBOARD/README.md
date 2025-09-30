# Finance Dashboard

A secure, local web application for tracking and managing your financial accounts including investment accounts, checking accounts, savings accounts, and stock trading accounts.

## 🔒 Security Features

- **Local Only**: Runs entirely on your local machine - no data leaves your computer
- **Encrypted Storage**: All sensitive data is encrypted using industry-standard Fernet encryption
- **User Authentication**: Secure login system with password hashing
- **Session Management**: Secure session handling with automatic logout
- **No External Dependencies**: All data processing happens locally

## 🚀 Features

### Account Management
- **Multiple Account Types**: Support for checking, savings, investment, stock, credit, and loan accounts
- **Secure Data Storage**: All account information is encrypted before storage
- **Account Details**: Track institution, account numbers (last 4 digits), and balances
- **Multi-Currency Support**: USD, EUR, GBP, CAD, AUD, JPY

### Dashboard & Analytics
- **Visual Dashboard**: Beautiful, responsive interface with charts and graphs
- **Portfolio Overview**: Total balance across all accounts
- **Account Distribution**: Pie charts showing account balance distribution
- **Account Type Summary**: Bar charts comparing different account types
- **Real-time Updates**: Live data updates as you add accounts

### Transaction Tracking
- **Transaction History**: Track all account transactions
- **Transaction Types**: Credit (money in) and Debit (money out)
- **Detailed Records**: Description, date, amount, and notes for each transaction
- **Secure Notes**: Encrypted transaction notes for sensitive information

### API Integration & Data Sync
- **Bank Account Integration**: Connect to 11,000+ financial institutions via Plaid
- **Real-time Stock Data**: Yahoo Finance integration for stocks and cryptocurrency
- **Automatic Data Sync**: Pull account balances and transactions automatically
- **Secure Credential Storage**: All API credentials encrypted and stored locally
- **Investment Tracking**: Monitor stock and crypto holdings with live prices

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or download** this repository to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd "FINANCE DASHBOARD"
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the dashboard**:
   - Open your web browser
   - Navigate to `http://127.0.0.1:5000`
   - Create your first account or login if you already have one

## 📁 Project Structure

```
FINANCE DASHBOARD/
├── app.py                 # Main Flask application
├── api_integrations.py    # Financial API integrations
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard
│   ├── add_account.html  # Add new account form
│   ├── account_detail.html # Account details page
│   ├── api_connections.html # API connections management
│   ├── add_api_connection.html # Add API connection form
│   └── stock_data.html   # Stock and crypto holdings
├── static/               # Static files (CSS, JS, images)
└── data/                 # Local data storage
    ├── finance_dashboard.db  # SQLite database
    └── encryption.key        # Encryption key (auto-generated)
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key (auto-generated if not set)
- The application will automatically generate encryption keys and database files

### Database
- Uses SQLite for local data storage
- Database file: `data/finance_dashboard.db`
- Automatically created on first run

### Encryption
- Encryption key: `data/encryption.key`
- Automatically generated on first run
- **Important**: Keep this file secure and backed up

## 🎯 Usage

### First Time Setup
1. Run the application
2. Register a new account
3. Login with your credentials
4. Add your financial accounts

### Adding Accounts
1. Click "Add Account" from the dashboard
2. Fill in account details:
   - Account name (e.g., "Chase Checking")
   - Account type (checking, savings, investment, etc.)
   - Current balance
   - Currency
   - Financial institution
   - Account number (last 4 digits only)

### Viewing Your Dashboard
- **Total Portfolio Value**: See your total balance across all accounts
- **Account Cards**: Visual cards for each account with balances
- **Charts**: Interactive charts showing account distribution and types
- **Account Details**: Click any account to see detailed information

### Managing Transactions
1. Click on any account to view details
2. Use "Add Transaction" to record money in/out
3. View transaction history with dates, amounts, and notes

### API Integration Setup

#### Bank Account Integration (Plaid)
1. **Get Plaid API Keys**:
   - Visit [Plaid Developers](https://plaid.com/developers/)
   - Create a free account
   - Get your Client ID and Secret key

2. **Connect Your Bank**:
   - Use Plaid's Link flow to connect your bank account
   - Copy the access token from the Link response
   - Add the connection in the dashboard

3. **Supported Banks**:
   - Chase, Bank of America, Wells Fargo, Capital One
   - Credit unions, investment firms, and 11,000+ institutions

#### Stock & Crypto Data (Yahoo Finance)
1. **No Setup Required**: Yahoo Finance integration is completely free
2. **Add Holdings**: Go to "Stocks & Crypto" page
3. **Enter Symbols**: Add stock symbols (AAPL, GOOGL) and crypto (BTC, ETH)
4. **Automatic Updates**: Prices update when you sync data

### Data Synchronization
1. **Manual Sync**: Click "Sync Data" to update all connected accounts
2. **Automatic Updates**: Stock and crypto prices update in real-time
3. **Secure Process**: All data is fetched and stored locally

## 🔐 Security Best Practices

1. **Keep Your Data Local**: This application is designed to run locally only
2. **Backup Your Data**: Regularly backup the `data/` folder
3. **Strong Passwords**: Use strong, unique passwords for your dashboard account
4. **Secure Your Computer**: Ensure your computer is secure and up-to-date
5. **Encryption Key**: Keep the `encryption.key` file secure and backed up

## 🚨 Important Security Notes

- **No Internet Required**: This application works completely offline
- **No Data Transmission**: Your financial data never leaves your computer
- **Local Encryption**: All sensitive data is encrypted before storage
- **Session Security**: Automatic logout and secure session management
- **No Third-Party Services**: No external APIs or cloud services used

## 🛠️ Troubleshooting

### Common Issues

1. **Port Already in Use**:
   - Change the port in `app.py`: `app.run(port=5001)`

2. **Database Errors**:
   - Delete `data/finance_dashboard.db` and restart the application

3. **Encryption Errors**:
   - Delete `data/encryption.key` and restart (you'll need to re-enter data)

4. **Permission Errors**:
   - Ensure the application has write permissions to the `data/` folder

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Ensure all dependencies are installed correctly
3. Verify Python version compatibility
4. Check file permissions in the project directory

## 📊 Data Privacy

- **100% Local**: All data stays on your computer
- **No Tracking**: No analytics or tracking of any kind
- **No External Connections**: Application doesn't connect to the internet
- **Your Data, Your Control**: You have complete control over your financial data

## 🔄 Updates and Maintenance

- **Regular Backups**: Backup your `data/` folder regularly
- **Update Dependencies**: Periodically update Python packages for security
- **Monitor Logs**: Check console output for any errors or warnings

## 📝 License

This project is for personal use. Feel free to modify and customize for your needs.

---

**Remember**: This application is designed for personal financial tracking. Always verify your account balances with your financial institutions and keep backups of your data.
