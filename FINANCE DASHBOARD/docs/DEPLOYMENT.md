# Finance Dashboard - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Finance Dashboard application in various environments. The application is designed to run locally for maximum security and data privacy, but can also be deployed in controlled environments.

## Deployment Options

### 1. Local Deployment (Recommended)
- **Primary Use Case**: Personal financial management
- **Security**: Maximum security with local data storage
- **Requirements**: Single user, local machine
- **Data Privacy**: Complete control over data

### 2. Local Network Deployment
- **Use Case**: Family or small team access
- **Security**: Network-isolated deployment
- **Requirements**: Local network access
- **Data Privacy**: Controlled network environment

### 3. Cloud Deployment (Advanced)
- **Use Case**: Remote access with security controls
- **Security**: Enhanced security measures required
- **Requirements**: Cloud infrastructure
- **Data Privacy**: Encrypted cloud storage

## Local Deployment

### System Requirements

#### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.7 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 1GB free space for application and data
- **Network**: Internet connection for API integrations

#### Recommended Requirements
- **Operating System**: Latest version with security updates
- **Python**: Version 3.9 or higher
- **Memory**: 8GB RAM or more
- **Storage**: 5GB free space for data and backups
- **Network**: Stable broadband connection

### Installation Steps

#### 1. Download and Extract
```bash
# Download the application
git clone https://github.com/your-repo/finance-dashboard.git
cd finance-dashboard

# Or extract from ZIP file
unzip finance-dashboard.zip
cd finance-dashboard
```

#### 2. Python Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

#### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

#### 4. Initialize Application
```bash
# Run the application launcher
python run.py

# Or run directly
python app.py
```

#### 5. Access Application
- Open web browser
- Navigate to `http://127.0.0.1:5000`
- Register your first account
- Begin using the application

### Configuration

#### Environment Variables
```bash
# Optional: Set custom secret key
export SECRET_KEY="your-custom-secret-key"

# Optional: Set custom database path
export DATABASE_PATH="/path/to/your/database.db"

# Optional: Set custom port
export PORT=5000
```

#### Application Configuration
```python
# app.py configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', secrets.token_hex(32)),
    DATABASE_PATH=os.environ.get('DATABASE_PATH', 'data/finance_dashboard.db'),
    PORT=int(os.environ.get('PORT', 5000))
)
```

## Local Network Deployment

### Network Configuration

#### Firewall Setup
```bash
# Windows Firewall
netsh advfirewall firewall add rule name="Finance Dashboard" dir=in action=allow protocol=TCP localport=5000

# Linux UFW
sudo ufw allow 5000/tcp

# macOS (System Preferences > Security & Privacy > Firewall)
# Add Python to allowed applications
```

#### Network Access
```python
# app.py network configuration
if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',  # Allow network access
        port=5000,
        ssl_context='adhoc'  # Optional: Enable HTTPS
    )
```

### Security Considerations

#### Network Security
- **Firewall Rules**: Restrict access to trusted IP addresses
- **HTTPS**: Enable SSL/TLS for encrypted communication
- **Authentication**: Ensure strong user authentication
- **Network Isolation**: Use VPN or private network

#### Access Control
```python
# IP whitelist example
ALLOWED_IPS = ['192.168.1.0/24', '10.0.0.0/8']

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
```

## Cloud Deployment

### Security Requirements

#### Data Protection
- **Encryption at Rest**: Database and file encryption
- **Encryption in Transit**: HTTPS/TLS for all communications
- **Access Control**: Multi-factor authentication
- **Audit Logging**: Comprehensive access logging

#### Infrastructure Security
- **VPC**: Virtual Private Cloud for network isolation
- **Security Groups**: Restrictive firewall rules
- **IAM**: Identity and Access Management
- **Secrets Management**: Secure credential storage

### AWS Deployment

#### EC2 Instance Setup
```bash
# Launch EC2 instance
aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --instance-type t3.micro \
    --key-name your-key-pair \
    --security-group-ids sg-xxxxxxxxx \
    --subnet-id subnet-xxxxxxxxx
```

#### Application Deployment
```bash
# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip git -y

# Clone and setup application
git clone https://github.com/your-repo/finance-dashboard.git
cd finance-dashboard
pip3 install -r requirements.txt
```

#### Database Setup
```bash
# Install and configure PostgreSQL
sudo yum install postgresql postgresql-server -y
sudo postgresql-setup initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE finance_dashboard;
CREATE USER finance_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE finance_dashboard TO finance_user;
```

#### Web Server Configuration
```bash
# Install and configure Nginx
sudo yum install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx

# Configure Nginx
sudo nano /etc/nginx/conf.d/finance-dashboard.conf
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### SSL Certificate
```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com
```

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  finance-dashboard:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - SECRET_KEY=your-secret-key
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - finance-dashboard
    restart: unless-stopped
```

#### Deployment Commands
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Production Deployment

### Performance Optimization

#### Database Optimization
```python
# Database connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'sqlite:///data/finance_dashboard.db',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

#### Caching
```python
# Redis caching
import redis
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})
```

#### Static File Serving
```python
# Nginx static file configuration
location /static {
    alias /path/to/finance-dashboard/static;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Monitoring and Logging

#### Application Monitoring
```python
# Logging configuration
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/finance_dashboard.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

#### Health Checks
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })
```

### Backup and Recovery

#### Database Backup
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/finance_dashboard"
DB_PATH="/app/data/finance_dashboard.db"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
cp $DB_PATH $BACKUP_DIR/finance_dashboard_$DATE.db

# Backup encryption key
cp /app/data/encryption.key $BACKUP_DIR/encryption_$DATE.key

# Compress backups
gzip $BACKUP_DIR/finance_dashboard_$DATE.db
gzip $BACKUP_DIR/encryption_$DATE.key

# Remove old backups (keep 30 days)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
```

#### Automated Backups
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

### Security Hardening

#### System Security
```bash
# Update system
sudo yum update -y

# Install security tools
sudo yum install fail2ban -y

# Configure fail2ban
sudo nano /etc/fail2ban/jail.local
```

**Fail2ban Configuration:**
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/secure
maxretry = 3
```

#### Application Security
```python
# Security headers
from flask_talisman import Talisman

Talisman(app, force_https=True)

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## Maintenance and Updates

### Regular Maintenance

#### System Updates
```bash
# Update system packages
sudo yum update -y

# Update Python packages
pip install --upgrade -r requirements.txt
```

#### Database Maintenance
```sql
-- Optimize database
VACUUM;
ANALYZE;

-- Check database integrity
PRAGMA integrity_check;
```

#### Log Rotation
```bash
# Configure logrotate
sudo nano /etc/logrotate.d/finance-dashboard
```

**Logrotate Configuration:**
```
/var/log/finance_dashboard/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload finance-dashboard
    endscript
}
```

### Monitoring

#### System Monitoring
```bash
# Install monitoring tools
sudo yum install htop iotop nethogs -y

# Monitor system resources
htop
iotop
nethogs
```

#### Application Monitoring
```python
# Performance monitoring
import time
from functools import wraps

def monitor_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        app.logger.info(f"{f.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return decorated_function
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 5000
sudo netstat -tulpn | grep :5000

# Kill process
sudo kill -9 <PID>

# Or use different port
export PORT=5001
python app.py
```

#### Database Locked
```bash
# Check for database locks
lsof data/finance_dashboard.db

# Kill processes using database
sudo kill -9 <PID>
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R www-data:www-data /path/to/finance-dashboard
sudo chmod -R 755 /path/to/finance-dashboard
```

### Log Analysis

#### Application Logs
```bash
# View application logs
tail -f logs/finance_dashboard.log

# Search for errors
grep -i error logs/finance_dashboard.log
```

#### System Logs
```bash
# View system logs
sudo journalctl -u finance-dashboard -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Disaster Recovery

### Recovery Procedures

#### Database Recovery
```bash
# Restore from backup
cp /backups/finance_dashboard/finance_dashboard_20231201_020000.db.gz data/
gunzip data/finance_dashboard_20231201_020000.db.gz
mv data/finance_dashboard_20231201_020000.db data/finance_dashboard.db
```

#### Application Recovery
```bash
# Redeploy application
git pull origin main
pip install -r requirements.txt
systemctl restart finance-dashboard
```

### Business Continuity

#### High Availability
- **Load Balancing**: Multiple application instances
- **Database Replication**: Master-slave database setup
- **Failover**: Automatic failover mechanisms
- **Monitoring**: Continuous health monitoring

#### Backup Strategy
- **Daily Backups**: Automated daily database backups
- **Offsite Storage**: Backup storage in different locations
- **Recovery Testing**: Regular recovery procedure testing
- **Documentation**: Comprehensive recovery documentation

This deployment guide provides comprehensive instructions for deploying the Finance Dashboard in various environments while maintaining security and data privacy.
