# Finance Dashboard - Architecture Documentation

## Overview

The Finance Dashboard is a secure, local web application built with Flask that provides comprehensive financial account management, API integrations, and real-time data synchronization. The application is designed to run entirely on the user's local machine, ensuring complete data privacy and security.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Finance Dashboard                        │
├─────────────────────────────────────────────────────────────┤
│  Web Interface (Flask + Bootstrap + Chart.js)              │
├─────────────────────────────────────────────────────────────┤
│  Application Layer (Python Flask)                          │
│  ├── Authentication & Authorization                        │
│  ├── API Integration Layer                                 │
│  ├── Data Processing & Encryption                          │
│  └── Business Logic                                        │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                │
│  ├── SQLite Database (Local)                               │
│  ├── Encrypted Storage                                     │
│  └── File System (Config & Keys)                           │
├─────────────────────────────────────────────────────────────┤
│  External APIs                                             │
│  ├── Plaid API (Banking)                                   │
│  └── Yahoo Finance API (Stocks/Crypto)                     │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Web Interface Layer

**Technology Stack:**
- **Frontend Framework:** HTML5, CSS3, JavaScript
- **UI Framework:** Bootstrap 5.3.0
- **Charts:** Chart.js
- **Icons:** Font Awesome 6.4.0

**Components:**
- **Base Template:** `base.html` - Common layout and navigation
- **Authentication:** `login.html`, `register.html` - User authentication
- **Dashboard:** `dashboard.html` - Main financial overview
- **Account Management:** `add_account.html`, `account_detail.html`
- **API Management:** `api_connections.html`, `add_api_connection.html`
- **Investment Tracking:** `stock_data.html`

### 2. Application Layer

**Core Components:**

#### Flask Application (`app.py`)
```python
# Main application structure
├── Configuration & Initialization
├── Database Management
├── Authentication & Session Management
├── Route Handlers
│   ├── Authentication Routes
│   ├── Dashboard Routes
│   ├── Account Management Routes
│   ├── API Integration Routes
│   └── Data Synchronization Routes
└── Security Middleware
```

#### API Integration Module (`api_integrations.py`)
```python
# API integration structure
├── FinancialAPI (Base Class)
├── PlaidAPI (Bank Account Integration)
├── YFinanceAPI (Stock/Crypto Data)
├── FinancialDataManager
│   ├── Credential Management
│   ├── Data Synchronization
│   ├── Account Updates
│   └── Transaction Processing
└── Data Models & Structures
```

### 3. Data Layer

#### Database Schema (SQLite)

**Users Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Accounts Table:**
```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    account_name TEXT NOT NULL,
    account_type TEXT NOT NULL,
    encrypted_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

**Transactions Table:**
```sql
CREATE TABLE transactions (
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
```

**API Connections Table:**
```sql
CREATE TABLE api_connections (
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
```

**Stock Holdings Table:**
```sql
CREATE TABLE stock_holdings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares REAL NOT NULL,
    purchase_price REAL,
    current_price REAL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

**Crypto Holdings Table:**
```sql
CREATE TABLE crypto_holdings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    amount REAL NOT NULL,
    purchase_price REAL,
    current_price REAL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

## Data Flow Architecture

### 1. User Authentication Flow

```
User Login Request
       ↓
Session Validation
       ↓
Password Verification (Werkzeug)
       ↓
Session Creation
       ↓
Dashboard Redirect
```

### 2. Account Data Flow

```
Manual Account Entry
       ↓
Data Validation
       ↓
Encryption (Fernet)
       ↓
Database Storage
       ↓
Dashboard Display
```

### 3. API Integration Flow

```
API Connection Setup
       ↓
Credential Encryption
       ↓
Database Storage
       ↓
Data Sync Request
       ↓
API Call (Plaid/YFinance)
       ↓
Data Processing
       ↓
Local Storage Update
       ↓
Dashboard Refresh
```

### 4. Data Synchronization Flow

```
Sync Request
       ↓
Active API Connections
       ↓
Parallel API Calls
       ↓
Data Processing & Validation
       ↓
Database Updates
       ↓
Error Handling & Logging
       ↓
Sync Results Display
```

## Security Architecture

### Encryption Strategy

**Data Encryption:**
- **Algorithm:** Fernet (symmetric encryption)
- **Key Management:** Auto-generated, stored locally
- **Encrypted Data:** Account details, API credentials, transaction notes

**Password Security:**
- **Hashing:** Werkzeug PBKDF2 with salt
- **Storage:** Hashed passwords only
- **Session Management:** Secure session tokens

### Access Control

**Authentication:**
- Username/password based
- Session-based authentication
- Automatic session timeout

**Authorization:**
- User-scoped data access
- API credential isolation
- Database-level user separation

## API Integration Architecture

### Plaid Integration

**Connection Flow:**
1. User provides Plaid credentials
2. Credentials encrypted and stored
3. API connection established
4. Account data retrieved
5. Transactions synchronized

**Data Mapping:**
- Plaid account types → Internal account types
- Transaction categorization
- Balance normalization

### Yahoo Finance Integration

**Data Retrieval:**
1. Stock/crypto symbols collected
2. Batch API calls to Yahoo Finance
3. Price data processing
4. Portfolio calculations
5. Database updates

## Performance Considerations

### Database Optimization

**Indexing Strategy:**
- Primary keys on all tables
- Foreign key indexes
- User ID indexes for data isolation

**Query Optimization:**
- Prepared statements
- Connection pooling
- Efficient data retrieval

### API Rate Limiting

**Plaid API:**
- Respect rate limits
- Error handling and retry logic
- Batch processing where possible

**Yahoo Finance:**
- Efficient symbol batching
- Caching strategies
- Error resilience

## Scalability Considerations

### Local Deployment

**Current Limitations:**
- Single-user application
- Local file system storage
- Single-machine deployment

**Future Enhancements:**
- Multi-user support
- Database migration options
- Cloud deployment capabilities

### Data Growth Management

**Storage Optimization:**
- Transaction archiving
- Data compression
- Cleanup routines

## Error Handling Architecture

### Error Categories

**Application Errors:**
- User input validation
- Business logic errors
- Database constraint violations

**API Errors:**
- Network connectivity issues
- API rate limiting
- Authentication failures

**System Errors:**
- File system errors
- Encryption/decryption failures
- Database corruption

### Error Recovery

**Graceful Degradation:**
- Partial data loading
- Offline mode capabilities
- User notification systems

**Logging Strategy:**
- Error categorization
- User action logging
- System performance monitoring

## Deployment Architecture

### Local Deployment

**Requirements:**
- Python 3.7+
- Local file system access
- Network access for API calls

**File Structure:**
```
FINANCE DASHBOARD/
├── app.py                 # Main application
├── api_integrations.py    # API integration layer
├── requirements.txt       # Dependencies
├── run.py                # Application launcher
├── templates/            # Web templates
├── static/               # Static assets
├── data/                 # Local data storage
│   ├── finance_dashboard.db
│   └── encryption.key
└── docs/                 # Documentation
```

### Security Considerations

**Local Security:**
- File system permissions
- Encryption key protection
- Database access control

**Network Security:**
- HTTPS for API communications
- Credential transmission security
- API endpoint validation

## Monitoring and Maintenance

### Health Monitoring

**Application Health:**
- Database connectivity
- API service availability
- Encryption key integrity

**Performance Monitoring:**
- Response times
- Memory usage
- Database performance

### Maintenance Tasks

**Regular Maintenance:**
- Database optimization
- Log file cleanup
- Security updates
- Dependency updates

**Backup Strategy:**
- Database backups
- Configuration backups
- Encryption key backups

## Future Architecture Considerations

### Potential Enhancements

**Multi-User Support:**
- User management system
- Role-based access control
- Data isolation improvements

**Advanced Analytics:**
- Machine learning integration
- Predictive analytics
- Advanced reporting

**Mobile Support:**
- Responsive design improvements
- Mobile-specific features
- Offline capabilities

**Cloud Integration:**
- Optional cloud backup
- Multi-device synchronization
- Enhanced security features

This architecture provides a solid foundation for a secure, scalable, and maintainable financial dashboard application while maintaining the core principle of local data storage and user privacy.
