#!/usr/bin/env python3
"""
Test database connection script
Run this to verify your database is accessible before starting the app
"""

import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection():
    print("Testing database connection...")
    print("-" * 50)
    
    config = {
        'host': os.getenv('DB_HOST', 'm7wltxurw8d2n21q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'),
        'user': os.getenv('DB_USER', 'it2jpmptcbrfz9gq'),
        'password': os.getenv('DB_PASSWORD', 'nxmebq1lgfp56e15'),
        'database': os.getenv('DB_NAME', 'ond7op6xmute4kcm'),
        'port': int(os.getenv('DB_PORT', 3306))
    }
    
    print(f"Host: {config['host']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    print("-" * 50)
    
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) as count FROM alerts")
        result = cursor.fetchone()
        alert_count = result[0]
        
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        user_count = result[0]
        
        print("✅ Connection successful!")
        print(f"✅ Found {alert_count} alerts in database")
        print(f"✅ Found {user_count} users in database")
        
        cursor.close()
        conn.close()
        
        print("-" * 50)
        print("Your database is ready! Run 'python app.py' to start.")
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Connection failed: {e}")
        print("-" * 50)
        print("Troubleshooting:")
        print("1. Check your .env file has correct credentials")
        print("2. Ensure you have internet access")
        print("3. Verify your IP is allowed by AWS RDS security group")
        return False

if __name__ == '__main__':
    test_connection()

