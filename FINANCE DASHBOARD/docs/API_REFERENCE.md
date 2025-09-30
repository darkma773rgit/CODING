# Finance Dashboard - API Reference Documentation

## Overview

The Finance Dashboard integrates with external financial APIs to provide real-time data synchronization and account management. This document provides comprehensive information about the API integrations, endpoints, and data structures used in the application.

## API Integration Architecture

### Supported APIs

1. **Plaid API**: Bank account integration and transaction data
2. **Yahoo Finance API**: Stock and cryptocurrency price data
3. **Internal API**: Application's own REST endpoints

## Plaid API Integration

### Overview

Plaid provides secure access to financial account data from over 11,000 financial institutions. The integration allows users to connect their bank accounts and automatically sync transaction data.

### Authentication

**API Credentials Required:**
- `client_id`: Your Plaid client identifier
- `secret`: Your Plaid secret key
- `access_token`: Token obtained from Link flow

**Environment Configuration:**
```python
# Production environment
PLAID_ENV = 'production'
PLAID_CLIENT_ID = 'your_client_id'
PLAID_SECRET = 'your_secret_key'
```

### Endpoints Used

#### 1. Accounts Get
**Endpoint:** `POST /accounts/get`

**Purpose:** Retrieve account information and balances

**Request:**
```json
{
  "access_token": "access-sandbox-xxx",
  "client_id": "your_client_id",
  "secret": "your_secret_key"
}
```

**Response:**
```json
{
  "accounts": [
    {
      "account_id": "vzeNDwK7KQIm4yEog683uElbp9GRLEFXGK98D",
      "balances": {
        "available": 100,
        "current": 110,
        "iso_currency_code": "USD",
        "limit": null,
        "unofficial_currency_code": null
      },
      "mask": "0000",
      "name": "Plaid Checking",
      "official_name": "Plaid Gold Standard 0% Interest Checking",
      "subtype": "checking",
      "type": "depository"
    }
  ],
  "item": {
    "available_products": ["balance", "identity", "payment_initiation"],
    "billed_products": ["auth", "transactions"],
    "consent_expiration_time": null,
    "error": null,
    "institution_id": "ins_3",
    "item_id": "eVBnVMp7zdTJLkRNr33Rs6zr7KNJqBFL9DrE6",
    "webhook": "https://www.genericwebhookurl.com/webhook"
  },
  "request_id": "45QSn"
}
```

#### 2. Transactions Get
**Endpoint:** `POST /transactions/get`

**Purpose:** Retrieve transaction history

**Request:**
```json
{
  "access_token": "access-sandbox-xxx",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "account_ids": ["vzeNDwK7KQIm4yEog683uElbp9GRLEFXGK98D"],
  "client_id": "your_client_id",
  "secret": "your_secret_key"
}
```

**Response:**
```json
{
  "accounts": [...],
  "transactions": [
    {
      "account_id": "vzeNDwK7KQIm4yEog683uElbp9GRLEFXGK98D",
      "account_owner": null,
      "amount": 2307.21,
      "authorized_date": "2023-01-27",
      "category": ["Shops", "Computers and Electronics"],
      "category_id": "19013000",
      "date": "2023-01-29",
      "location": {
        "address": "300 Post St",
        "city": "San Francisco",
        "country": "US",
        "lat": 40.740352,
        "lon": -74.001761,
        "postal_code": "94108",
        "region": "CA",
        "store_number": "1235"
      },
      "merchant_name": "Apple Store",
      "name": "Apple Store",
      "payment_meta": {
        "by_order_of": null,
        "payee": null,
        "payer": null,
        "payment_method": null,
        "payment_processor": null,
        "ppd_id": null,
        "reason": null,
        "reference_number": null
      },
      "pending": false,
      "transaction_id": "lPNjeW1nR6CDn5okmGQ6hEpMo4lLNoSrzqDje",
      "transaction_type": "place"
    }
  ],
  "total_transactions": 1,
  "request_id": "45QSn"
}
```

### Data Mapping

#### Account Type Mapping
```python
PLAID_TO_INTERNAL_TYPE_MAPPING = {
    'depository': 'checking',
    'credit': 'credit',
    'loan': 'loan',
    'investment': 'investment',
    'brokerage': 'stock'
}
```

#### Transaction Processing
```python
def process_plaid_transaction(transaction):
    return {
        'amount': abs(transaction['amount']),
        'description': transaction['name'],
        'transaction_type': 'credit' if transaction['amount'] > 0 else 'debit',
        'date': transaction['date'],
        'category': transaction.get('category', [])
    }
```

### Error Handling

**Common Plaid Errors:**
- `INVALID_ACCESS_TOKEN`: Access token is invalid or expired
- `ITEM_LOGIN_REQUIRED`: User needs to re-authenticate
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INSTITUTION_DOWN`: Bank system temporarily unavailable

**Error Response Format:**
```json
{
  "error": {
    "error_code": "INVALID_ACCESS_TOKEN",
    "error_message": "The provided access token is invalid",
    "error_type": "INVALID_REQUEST",
    "request_id": "45QSn"
  }
}
```

## Yahoo Finance API Integration

### Overview

Yahoo Finance provides free access to stock and cryptocurrency price data. No authentication is required, making it ideal for real-time price updates.

### Data Retrieval

#### Stock Data
**Symbol Format:** Standard ticker symbols (e.g., AAPL, GOOGL, MSFT)

**Data Retrieved:**
- Current price
- Daily change
- Volume
- Market cap
- 52-week high/low

#### Cryptocurrency Data
**Symbol Format:** Crypto symbol + USD (e.g., BTC-USD, ETH-USD)

**Data Retrieved:**
- Current price
- Daily change
- Volume
- Market cap

### Implementation

#### Stock Data Retrieval
```python
import yfinance as yf

def get_stock_data(symbols):
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
```

#### Cryptocurrency Data Retrieval
```python
def get_crypto_data(symbols):
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
```

### Rate Limiting

**Yahoo Finance Limits:**
- No official rate limits documented
- Recommended: 1 request per second per symbol
- Batch requests when possible
- Implement retry logic with exponential backoff

### Error Handling

**Common Yahoo Finance Errors:**
- `Symbol not found`: Invalid ticker symbol
- `Network timeout`: Connection issues
- `Data unavailable`: Market closed or symbol delisted

## Internal API Endpoints

### Authentication Endpoints

#### POST /login
**Purpose:** User authentication

**Request:**
```json
{
  "username": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user_id": 123
}
```

#### POST /register
**Purpose:** User registration

**Request:**
```json
{
  "username": "user@example.com",
  "password": "secure_password",
  "confirm_password": "secure_password"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Registration successful"
}
```

### Account Management Endpoints

#### GET /dashboard
**Purpose:** Retrieve dashboard data

**Response:**
```json
{
  "accounts": [
    {
      "id": 1,
      "name": "Chase Checking",
      "type": "checking",
      "balance": 2500.00,
      "currency": "USD",
      "updated_at": "2023-12-01T10:30:00Z"
    }
  ],
  "total_balance": 2500.00
}
```

#### POST /add_account
**Purpose:** Add new account

**Request:**
```json
{
  "account_name": "Chase Checking",
  "account_type": "checking",
  "balance": 2500.00,
  "currency": "USD",
  "institution": "Chase Bank",
  "account_number": "1234"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Account added successfully",
  "account_id": 123
}
```

### API Connection Endpoints

#### GET /api_connections
**Purpose:** List API connections

**Response:**
```json
{
  "connections": [
    {
      "id": 1,
      "institution_name": "Chase Bank",
      "api_type": "plaid",
      "is_active": true,
      "last_sync": "2023-12-01T10:30:00Z"
    }
  ]
}
```

#### POST /add_api_connection
**Purpose:** Add API connection

**Request:**
```json
{
  "institution_name": "Chase Bank",
  "api_type": "plaid",
  "plaid_client_id": "client_id",
  "plaid_secret": "secret_key",
  "plaid_access_token": "access_token"
}
```

**Response:**
```json
{
  "success": true,
  "message": "API connection added successfully"
}
```

### Data Synchronization Endpoints

#### POST /sync_data
**Purpose:** Synchronize all account data

**Response:**
```json
{
  "success": true,
  "accounts_updated": 5,
  "errors": [],
  "last_sync": "2023-12-01T10:30:00Z"
}
```

### Investment Data Endpoints

#### GET /stock_data
**Purpose:** Retrieve stock and crypto holdings

**Response:**
```json
{
  "stocks": [
    {
      "symbol": "AAPL",
      "shares": 10,
      "purchase_price": 150.00,
      "current_price": 175.00,
      "last_updated": "2023-12-01T10:30:00Z"
    }
  ],
  "crypto": [
    {
      "symbol": "BTC",
      "amount": 0.5,
      "purchase_price": 30000.00,
      "current_price": 45000.00,
      "last_updated": "2023-12-01T10:30:00Z"
    }
  ]
}
```

#### POST /add_stock_holding
**Purpose:** Add stock holding

**Request:**
```json
{
  "symbol": "AAPL",
  "shares": 10,
  "purchase_price": 150.00
}
```

**Response:**
```json
{
  "success": true,
  "message": "Stock holding added successfully"
}
```

## Data Models

### Account Data Model
```python
@dataclass
class AccountData:
    account_id: str
    account_name: str
    account_type: str
    balance: float
    currency: str
    institution: str
    last_updated: datetime
    transactions: List[Dict[str, Any]] = None
```

### Transaction Data Model
```python
@dataclass
class TransactionData:
    transaction_id: str
    account_id: str
    amount: float
    description: str
    transaction_type: str  # 'credit' or 'debit'
    date: datetime
    category: List[str]
    notes: str = None
```

### API Connection Data Model
```python
@dataclass
class APIConnection:
    connection_id: str
    user_id: str
    institution_name: str
    api_type: str  # 'plaid' or 'yfinance'
    credentials: Dict[str, str]
    is_active: bool
    last_sync: datetime
```

## Error Handling

### HTTP Status Codes

**Success Codes:**
- `200 OK`: Request successful
- `201 Created`: Resource created successfully

**Client Error Codes:**
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

**Server Error Codes:**
- `500 Internal Server Error`: Server error
- `502 Bad Gateway`: External API error
- `503 Service Unavailable`: Service temporarily unavailable

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "balance",
      "issue": "Must be a positive number"
    }
  }
}
```

## Rate Limiting

### Plaid API Limits
- **Development**: 100 requests per minute
- **Production**: Varies by plan
- **Best Practice**: Implement exponential backoff

### Yahoo Finance Limits
- **No Official Limits**: Use reasonable request rates
- **Recommended**: 1 request per second
- **Best Practice**: Batch requests when possible

## Security Considerations

### API Key Management
- **Encryption**: All API keys encrypted before storage
- **Access Control**: Keys only accessible to authenticated users
- **Rotation**: Regular key rotation recommended

### Data Transmission
- **HTTPS Only**: All API communications over HTTPS
- **Certificate Validation**: Proper SSL certificate verification
- **Timeout Handling**: Network timeout protection

### Error Information
- **No Credential Exposure**: API keys never exposed in error messages
- **Generic Error Messages**: User-friendly error messages
- **Detailed Logging**: Server-side detailed error logging

## Testing and Development

### Sandbox Environments

#### Plaid Sandbox
- **Environment**: `sandbox.plaid.com`
- **Test Data**: Pre-configured test accounts
- **No Real Data**: Safe for development and testing

#### Yahoo Finance
- **No Sandbox**: Use production environment
- **Test Symbols**: Use real symbols for testing
- **Rate Limiting**: Be mindful of request rates

### Development Setup
```python
# Development configuration
PLAID_ENV = 'sandbox'
PLAID_CLIENT_ID = 'your_sandbox_client_id'
PLAID_SECRET = 'your_sandbox_secret'
```

## Monitoring and Logging

### API Monitoring
- **Request/Response Logging**: Log all API interactions
- **Error Tracking**: Monitor API error rates
- **Performance Metrics**: Track response times

### Logging Format
```json
{
  "timestamp": "2023-12-01T10:30:00Z",
  "level": "INFO",
  "service": "plaid_api",
  "endpoint": "/accounts/get",
  "status_code": 200,
  "response_time_ms": 150,
  "user_id": "123"
}
```

This comprehensive API reference provides all the information needed to understand and work with the Finance Dashboard's API integrations.
