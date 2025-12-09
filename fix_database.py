#!/usr/bin/env python3
"""
Fix database schema - Add user_id column to vulnerabilities table
Run this once to fix the save functionality
"""

import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def fix_database():
    print("Fixing database schema...")
    print("-" * 50)
    
    config = {
        'host': os.getenv('DB_HOST', 'm7wltxurw8d2n21q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'),
        'user': os.getenv('DB_USER', 'it2jpmptcbrfz9gq'),
        'password': os.getenv('DB_PASSWORD', 'e5voj8n91k1ni3m6'),
        'database': os.getenv('DB_NAME', 'ond7op6xmute4kcm'),
        'port': int(os.getenv('DB_PORT', 3306))
    }
    
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'vulnerabilities' 
            AND COLUMN_NAME = 'user_id'
        """, (config['database'],))
        
        exists = cursor.fetchone()[0] > 0
        
        if exists:
            print("✅ user_id column already exists!")
        else:
            print("Adding user_id column to vulnerabilities table...")
            
            # Add user_id column
            cursor.execute("""
                ALTER TABLE vulnerabilities 
                ADD COLUMN user_id INT NULL AFTER notes
            """)
            
            # Add index for faster queries
            cursor.execute("""
                CREATE INDEX idx_vulnerabilities_user_id ON vulnerabilities(user_id)
            """)
            
            conn.commit()
            print("✅ Successfully added user_id column!")
            print("✅ Added index for faster queries")
        
        cursor.close()
        conn.close()
        
        print("-" * 50)
        print("Database fix complete! Save button should work now.")
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error: {e}")
        print("-" * 50)
        return False

if __name__ == '__main__':
    fix_database()

