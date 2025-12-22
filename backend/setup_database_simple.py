"""
Simplified database setup - update password in this file before running
"""
import mysql.connector
from mysql.connector import Error
import os

# ============================================
# UPDATE THIS WITH YOUR MYSQL PASSWORD
# ============================================
MYSQL_PASSWORD = 'Balu@6688'  # Enter your MySQL root password here, or leave empty if no password

DATABASE_NAME = 'pcb_rate_contract'

def create_database():
    """Create the database if it doesn't exist"""
    try:
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': MYSQL_PASSWORD
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"[OK] Database '{DATABASE_NAME}' created or already exists")
        
        cursor.close()
        connection.close()
        
        return True
    except Error as e:
        print(f"[ERROR] Error creating database: {e}")
        return False

def create_tables():
    """Create all tables from schema file"""
    try:
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Connect to the database
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': MYSQL_PASSWORD,
            'database': DATABASE_NAME
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Split by semicolon and execute each statement
        statements = schema_sql.split(';')
        executed = 0
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    executed += 1
                except Error as e:
                    # Ignore "table doesn't exist" errors for DROP statements
                    error_msg = str(e).lower()
                    if 'doesn\'t exist' in error_msg or 'already exists' in error_msg:
                        # This is expected for DROP/CREATE statements
                        if 'DROP' in statement.upper():
                            pass  # Ignore DROP errors
                        elif 'CREATE' in statement.upper():
                            pass  # Ignore CREATE IF EXISTS errors
                    else:
                        print(f"[WARNING] {e}")
                        print(f"  Statement: {statement[:100]}...")
        
        connection.commit()
        print(f"[OK] Executed {executed} SQL statements")
        print("[OK] Tables created successfully")
        
        cursor.close()
        connection.close()
        
        return True
    except Error as e:
        print(f"[ERROR] Error creating tables: {e}")
        return False

def main():
    print("=" * 60)
    print("MySQL Database Setup")
    print("=" * 60)
    print(f"\nUsing password: {'(set)' if MYSQL_PASSWORD else '(empty - no password)'}")
    print()
    
    if not create_database():
        print("\n[ERROR] Failed to create database")
        return
    
    if not create_tables():
        print("\n[ERROR] Failed to create tables")
        return
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Database setup completed!")
    print("=" * 60)
    print("\nNext step: Run 'python import_hiq_data.py' to import data")

if __name__ == '__main__':
    main()

