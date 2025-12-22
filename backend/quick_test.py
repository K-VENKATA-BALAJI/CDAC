"""
Quick test script to verify MySQL setup
"""
import sys

print("=" * 60)
print("MySQL Setup Verification")
print("=" * 60)

# Test 1: Check MySQL connector
print("\n1. Checking MySQL connector...")
try:
    import mysql.connector
    print("   [OK] MySQL connector installed")
except ImportError:
    print("   [ERROR] MySQL connector not found")
    print("   Run: pip install mysql-connector-python")
    sys.exit(1)

# Test 2: Check if we can connect (will prompt for password)
print("\n2. Testing MySQL connection...")
try:
    password = input("   Enter MySQL root password (or press Enter if no password): ").strip()
    
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': password if password else ''
    }
    
    connection = mysql.connector.connect(**config)
    print("   [OK] Successfully connected to MySQL")
    connection.close()
except Exception as e:
    print(f"   [ERROR] Connection failed: {e}")
    print("   Please check:")
    print("   - MySQL server is running")
    print("   - Password is correct")
    print("   - MySQL is accessible on localhost")
    sys.exit(1)

# Test 3: Check if database exists
print("\n3. Checking database...")
try:
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': password if password else ''
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    cursor.execute("SHOW DATABASES LIKE 'pcb_rate_contract'")
    result = cursor.fetchone()
    
    if result:
        print("   [OK] Database 'pcb_rate_contract' exists")
        
        # Check tables
        cursor.execute("USE pcb_rate_contract")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   [OK] Found {len(tables)} tables")
        for table in tables:
            print(f"      - {table[0]}")
    else:
        print("   [WARNING] Database 'pcb_rate_contract' does not exist")
        print("   Run: python setup_mysql.py")
    
    cursor.close()
    connection.close()
except Exception as e:
    print(f"   [ERROR] Error checking database: {e}")

# Test 4: Check Excel file
print("\n4. Checking HIQ Excel file...")
import os
excel_path = os.path.join(os.path.dirname(__file__), '..', 'HIQ_Rate contract.xlsx')
if os.path.exists(excel_path):
    print(f"   [OK] Excel file found: {excel_path}")
else:
    print(f"   [ERROR] Excel file not found: {excel_path}")

print("\n" + "=" * 60)
print("Verification complete!")
print("=" * 60)
print("\nNext steps:")
print("1. If database doesn't exist: python setup_mysql.py")
print("2. Import data: python import_hiq_data.py")
print("3. Start server: python server.py")

