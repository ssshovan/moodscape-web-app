#!/usr/bin/env python3
"""
MoodScape - Quick Start Script
Run this script to start the Flask application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import mysql.connector
        import werkzeug
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def start_flask():
    """Start the Flask application"""
    print("Starting Flask application...")
    os.chdir('backend')
    subprocess.check_call([sys.executable, 'app.py'])

def main():
    print("MoodScape - Mood-Based Movie Review Platform")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        response = input("Install missing dependencies? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("Please install dependencies manually: pip install -r requirements.txt")
            sys.exit(1)
    
    # Check if database exists
    print("\nMake sure you have run the database setup:")
    print("  cd database")
    print("  python setup.py")
    print("\nOr manually execute schema.sql and sample_data.sql in MySQL")
    
    response = input("\nStart Flask application? (y/n): ")
    if response.lower() == 'y':
        start_flask()
    else:
        print("To start manually: cd backend && python app.py")

if __name__ == "__main__":
    main()