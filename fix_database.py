#!/usr/bin/env python3
"""
Fix database schema - Add user_id column and fix unique constraints
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
        'password': os.getenv('DB_PASSWORD', 'nxmebq1lgfp56e15'),
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
        
        # Fix unique constraint - remove old one on cve_id alone, add composite
        print("\nFixing unique constraints...")
        
        # Try to find and remove unique constraint on just cve_id
        cursor.execute("SHOW INDEX FROM vulnerabilities WHERE Key_name != 'PRIMARY'")
        indexes = cursor.fetchall()
        
        for index in indexes:
            index_name = index[2]  # Key_name
            column_name = index[4]  # Column_name
            non_unique = index[1]  # Non_unique
            
            # If it's a unique index on just cve_id (not composite)
            if non_unique == 0 and column_name == 'cve_id':
                # Check if it's a single-column index
                cursor.execute(f"SHOW INDEX FROM vulnerabilities WHERE Key_name = '{index_name}'")
                index_cols = cursor.fetchall()
                if len(index_cols) == 1:  # Only one column in this index
                    print(f"Removing unique constraint on cve_id: {index_name}")
                    try:
                        cursor.execute(f"ALTER TABLE vulnerabilities DROP INDEX {index_name}")
                        conn.commit()
                        print(f"✅ Removed {index_name}")
                    except Exception as e:
                        print(f"⚠️  Could not remove {index_name}: {e}")
        
        # Add composite unique constraint (cve_id, user_id) if it doesn't exist
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.STATISTICS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'vulnerabilities' 
            AND INDEX_NAME = 'unique_user_cve'
        """, (config['database'],))
        
        composite_exists = cursor.fetchone()[0] > 0
        
        if not composite_exists:
            print("\nAdding composite unique constraint (cve_id, user_id)...")
            try:
                cursor.execute("""
                    ALTER TABLE vulnerabilities 
                    ADD UNIQUE KEY unique_user_cve (cve_id, user_id)
                """)
                conn.commit()
                print("✅ Added composite unique constraint!")
                print("   Now each user can save the same CVE once")
            except Exception as e:
                if "Duplicate key name" in str(e) or "already exists" in str(e).lower():
                    print("✅ Composite unique constraint already exists!")
                else:
                    print(f"⚠️  Could not add constraint: {e}")
        else:
            print("✅ Composite unique constraint already exists!")
        
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
