#!/usr/bin/env python3
"""
Finance Dashboard Launcher
Simple script to run the Finance Dashboard application
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install requirements")
        return False

def run_application():
    """Run the Flask application"""
    print("Starting Finance Dashboard...")
    print("=" * 50)
    print("🔒 SECURE LOCAL FINANCE DASHBOARD")
    print("=" * 50)
    print("📊 Access your dashboard at: http://127.0.0.1:5000")
    print("🔐 All data is encrypted and stored locally")
    print("🚫 No data leaves your computer")
    print("=" * 50)
    print("Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        from app import app, init_database
        init_database()
        app.run(debug=False, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")
    except Exception as e:
        print(f"\nError starting application: {e}")
        return False
    return True

def main():
    """Main function"""
    print("Finance Dashboard - Secure Local Financial Tracking")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Run the application
    if not run_application():
        sys.exit(1)

if __name__ == "__main__":
    main()
