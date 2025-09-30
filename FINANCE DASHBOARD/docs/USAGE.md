# Finance Dashboard - Usage Documentation

## Getting Started

### Initial Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Application:**
   ```bash
   python run.py
   ```

3. **Access Dashboard:**
   - Open browser to `http://127.0.0.1:5000`
   - Register your first account
   - Login to access the dashboard

## User Interface Guide

### Navigation

The Finance Dashboard features a clean, intuitive interface with the following main sections:

#### Sidebar Navigation
- **Dashboard**: Main overview with charts and account summaries
- **Add Account**: Manually add financial accounts
- **API Connections**: Manage external service connections
- **Stocks & Crypto**: Track investment holdings
- **Sync Data**: Update all connected accounts
- **Logout**: Secure session termination

### Dashboard Overview

#### Portfolio Summary
- **Total Portfolio Value**: Combined balance across all accounts
- **Account Cards**: Visual representation of each account
- **Account Distribution Chart**: Pie chart showing balance distribution
- **Account Types Summary**: Bar chart comparing account types

#### Account Cards
Each account is displayed as a color-coded card:
- **Blue**: Checking accounts
- **Green**: Savings accounts
- **Purple**: Investment accounts
- **Orange**: Stock trading accounts
- **Red**: Credit cards
- **Gray**: Other account types

## Account Management

### Adding Accounts Manually

1. **Navigate to Add Account:**
   - Click "Add Account" in the sidebar
   - Fill in the account details form

2. **Required Information:**
   - **Account Name**: Descriptive name (e.g., "Chase Checking")
   - **Account Type**: Select from dropdown menu
   - **Current Balance**: Enter current account balance
   - **Currency**: Select currency type

3. **Optional Information:**
   - **Financial Institution**: Bank or institution name
   - **Account Number**: Last 4 digits for identification

4. **Submit Account:**
   - Click "Add Account" to save
   - Account appears on dashboard immediately

### Account Types Supported

#### Banking Accounts
- **Checking**: Primary transaction accounts
- **Savings**: Interest-bearing savings accounts
- **Credit**: Credit card accounts
- **Loan**: Personal, auto, mortgage loans

#### Investment Accounts
- **Investment**: 401k, IRA, mutual funds
- **Stock**: Individual stock trading accounts
- **Other**: Any other financial account type

### Viewing Account Details

1. **Access Account Details:**
   - Click "View Details" on any account card
   - Navigate to detailed account view

2. **Account Information Display:**
   - Current balance and currency
   - Account type and institution
   - Last updated timestamp
   - Transaction history

3. **Transaction Management:**
   - View recent transactions
   - Add new transactions manually
   - Edit transaction details
   - Export transaction data

## API Integration

### Setting Up Bank Account Integration (Plaid)

#### Prerequisites
1. **Plaid Account Setup:**
   - Visit [Plaid Developers](https://plaid.com/developers/)
   - Create a free developer account
   - Obtain API credentials (Client ID, Secret)

2. **Bank Account Connection:**
   - Use Plaid's Link flow to connect your bank
   - Complete bank authentication process
   - Obtain access token from Link response

#### Adding Plaid Connection

1. **Navigate to API Connections:**
   - Click "API Connections" in sidebar
   - Click "Add Connection" button

2. **Select Service Type:**
   - Choose "Bank Accounts (Plaid)"
   - Enter institution name

3. **Enter Credentials:**
   - **Plaid Client ID**: Your Plaid client identifier
   - **Plaid Secret**: Your Plaid secret key
   - **Access Token**: Token from bank connection

4. **Save Connection:**
   - Click "Add Connection"
   - Connection appears in API connections list

#### Supported Banks
Plaid supports 11,000+ financial institutions including:
- Chase Bank
- Bank of America
- Wells Fargo
- Capital One
- Credit unions
- Investment firms
- And many more

### Stock and Cryptocurrency Integration

#### Yahoo Finance Setup
- **No Credentials Required**: Yahoo Finance is completely free
- **No Setup Needed**: Just add your holdings
- **Real-time Data**: Live price updates available

#### Adding Stock Holdings

1. **Navigate to Stocks & Crypto:**
   - Click "Stocks & Crypto" in sidebar
   - Click "Add Stock" button

2. **Enter Stock Information:**
   - **Stock Symbol**: Ticker symbol (e.g., AAPL, GOOGL)
   - **Number of Shares**: Quantity owned
   - **Purchase Price**: Optional, for profit/loss tracking

3. **Save Holding:**
   - Click "Add Stock"
   - Stock appears in holdings list

#### Adding Cryptocurrency Holdings

1. **Click "Add Crypto" Button:**
   - In the Stocks & Crypto section
   - Select "Add Cryptocurrency Holding"

2. **Enter Crypto Information:**
   - **Cryptocurrency Symbol**: Symbol (e.g., BTC, ETH, ADA)
   - **Amount**: Quantity owned
   - **Purchase Price**: Optional, for profit/loss tracking

3. **Save Holding:**
   - Click "Add Crypto"
   - Cryptocurrency appears in holdings list

## Data Synchronization

### Manual Data Sync

1. **Initiate Sync:**
   - Click "Sync Data" in sidebar
   - System processes all active connections

2. **Sync Process:**
   - Bank account data retrieval
   - Stock/crypto price updates
   - Transaction history updates
   - Database updates

3. **Sync Results:**
   - Success/failure notifications
   - Number of accounts updated
   - Error messages if applicable

### Automatic Updates

#### Stock and Crypto Prices
- **Real-time Updates**: Prices update when you sync
- **Market Hours**: Updates available during market hours
- **Historical Data**: Previous day's closing prices

#### Bank Account Data
- **Transaction History**: Last 30 days of transactions
- **Balance Updates**: Current account balances
- **Account Information**: Institution and account details

## Transaction Management

### Adding Transactions

1. **Access Transaction Form:**
   - Go to account details page
   - Click "Add Transaction" button

2. **Transaction Information:**
   - **Amount**: Transaction amount
   - **Type**: Credit (money in) or Debit (money out)
   - **Description**: Transaction description
   - **Date**: Transaction date
   - **Notes**: Optional additional notes

3. **Save Transaction:**
   - Click "Add Transaction"
   - Transaction appears in history

### Transaction History

#### Viewing Transactions
- **Recent Transactions**: Last 20 transactions displayed
- **Transaction Details**: Amount, description, date, type
- **Notes**: Encrypted notes for sensitive information
- **Categories**: Automatic categorization from bank data

#### Transaction Types
- **Credit**: Money coming into account
- **Debit**: Money going out of account
- **Automatic**: Transactions from bank sync
- **Manual**: User-entered transactions

## Charts and Analytics

### Portfolio Overview Charts

#### Account Distribution Chart
- **Pie Chart**: Visual breakdown of account balances
- **Interactive**: Hover for detailed information
- **Color Coded**: Different colors for each account
- **Percentage Display**: Shows percentage of total portfolio

#### Account Types Summary
- **Bar Chart**: Comparison of account types
- **Total Balances**: Sum of each account type
- **Interactive**: Click for detailed breakdown
- **Real-time Updates**: Updates with data sync

### Investment Analytics

#### Stock Performance
- **Current Prices**: Real-time stock prices
- **Total Value**: Shares × current price
- **Purchase Price**: Original purchase price
- **Profit/Loss**: Calculated gains or losses

#### Cryptocurrency Performance
- **Current Prices**: Real-time crypto prices
- **Total Value**: Amount × current price
- **Purchase Price**: Original purchase price
- **Profit/Loss**: Calculated gains or losses

## Data Export and Backup

### Exporting Data

1. **Account Data Export:**
   - Navigate to account details
   - Click "Export Data" button
   - Choose export format (CSV, JSON)

2. **Transaction Export:**
   - Select date range
   - Choose export format
   - Download transaction history

### Backup Procedures

#### Manual Backup
1. **Database Backup:**
   - Copy `data/finance_dashboard.db` file
   - Store in secure location
   - Regular backup schedule recommended

2. **Configuration Backup:**
   - Copy `data/encryption.key` file
   - Store separately from database
   - Critical for data decryption

#### Automated Backup
- **Scheduled Backups**: Set up regular backup schedule
- **Multiple Locations**: Store backups in different locations
- **Backup Testing**: Regularly test backup restoration

## Troubleshooting

### Common Issues

#### Login Problems
- **Forgot Password**: No password recovery (by design for security)
- **Account Lockout**: Clear browser data and try again
- **Session Expired**: Login again to continue

#### API Connection Issues
- **Plaid Connection Failed**: Check credentials and network
- **Stock Data Not Updating**: Verify internet connection
- **Sync Errors**: Check API connection status

#### Data Display Issues
- **Missing Accounts**: Check if accounts are properly added
- **Incorrect Balances**: Verify manual entry or sync data
- **Chart Not Loading**: Refresh page or check browser console

### Error Messages

#### Authentication Errors
- **"Invalid username or password"**: Check credentials
- **"Please log in to access this page"**: Session expired
- **"Username already exists"**: Choose different username

#### API Errors
- **"API connection failed"**: Check network and credentials
- **"Data synchronization error"**: Check API service status
- **"Invalid API credentials"**: Verify Plaid credentials

#### Data Errors
- **"Account not found"**: Account may have been deleted
- **"Invalid data format"**: Check input format and try again
- **"Database error"**: Contact support or restore from backup

## Best Practices

### Security Best Practices

1. **Password Security:**
   - Use strong, unique passwords
   - Don't share login credentials
   - Logout when finished

2. **Data Protection:**
   - Regular backups of data folder
   - Secure storage of backup files
   - Keep encryption key safe

3. **System Security:**
   - Keep operating system updated
   - Use antivirus software
   - Enable firewall protection

### Data Management Best Practices

1. **Regular Updates:**
   - Sync data regularly for current information
   - Update account balances manually if needed
   - Review transaction history regularly

2. **Account Organization:**
   - Use descriptive account names
   - Group similar accounts together
   - Keep account information current

3. **Transaction Tracking:**
   - Add transactions promptly
   - Use descriptive transaction descriptions
   - Categorize transactions appropriately

## Advanced Features

### Custom Account Types
- **Flexible Categorization**: Create custom account types
- **Color Coding**: Visual distinction between account types
- **Filtering**: Filter accounts by type

### Multi-Currency Support
- **Currency Selection**: Choose from major world currencies
- **Exchange Rates**: Real-time exchange rate updates
- **Currency Conversion**: Automatic conversion for display

### Data Analytics
- **Trend Analysis**: Track balance changes over time
- **Spending Patterns**: Analyze transaction patterns
- **Investment Performance**: Monitor portfolio performance

## Support and Resources

### Documentation
- **User Guide**: This comprehensive usage guide
- **Architecture Documentation**: Technical system overview
- **Security Documentation**: Security features and best practices
- **API Reference**: External API integration details

### Getting Help
- **Error Messages**: Check error descriptions and solutions
- **Troubleshooting Guide**: Common issues and resolutions
- **Best Practices**: Recommended usage patterns
- **Security Guidelines**: Security recommendations

### Updates and Maintenance
- **Regular Updates**: Keep application and dependencies updated
- **Security Patches**: Apply security updates promptly
- **Backup Maintenance**: Regular backup and testing procedures
- **Performance Monitoring**: Monitor application performance

This comprehensive usage guide provides everything you need to effectively use the Finance Dashboard application while maintaining security and data integrity.
