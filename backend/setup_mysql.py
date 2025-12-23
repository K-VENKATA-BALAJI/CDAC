"""
Setup script to create MySQL database and tables
Run this before importing data
"""
import mysql.connector
from mysql.connector import Error
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''  # Update with your MySQL password
}

DATABASE_NAME = 'pcb_rate_contract'

def create_database():
    """Create the database if it doesn't exist"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database '{DATABASE_NAME}' created or already exists")
        
        cursor.close()
        connection.close()
        
        return True
    except Error as e:
        print(f"Error creating database: {e}")
        return False

def create_tables():
    """Create all tables from schema file"""
    try:
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Connect to the database
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Split by semicolon and execute each statement
        statements = schema_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Error as e:
                    # Ignore "table doesn't exist" errors for DROP statements
                    if 'doesn\'t exist' not in str(e).lower():
                        print(f"Warning: {e}")
        
        connection.commit()
        print("Tables created successfully")
        
        cursor.close()
        connection.close()
        
        return True
    except Error as e:
        print(f"Error creating tables: {e}")
        return False

def main():
    print("Setting up MySQL database...")
    print("=" * 60)
    
    # Update password if needed
    password = input("Enter MySQL root password (press Enter if no password): ").strip()
    if password:
        DB_CONFIG['password'] = password
    
    print("\n1. Creating database...")
    if not create_database():
        print("Failed to create database")
        return
    
    print("\n2. Creating tables...")
    if not create_tables():
        print("Failed to create tables")
        return
    
    print("\n" + "=" * 60)
    print("Database setup completed successfully!")
    print(f"\nNext steps:")
    print(f"1. Update DB_CONFIG in database_mysql.py and import_hiq_data.py with your MySQL password")
    print(f"2. Run: python import_hiq_data.py")

if __name__ == '__main__':
    main()


