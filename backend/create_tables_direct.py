"""
Direct table creation script
"""
import mysql.connector
from mysql.connector import Error

MYSQL_PASSWORD = 'Balu@6688'
DATABASE_NAME = 'pcb_rate_contract'

def create_tables():
    """Create tables directly"""
    try:
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': MYSQL_PASSWORD,
            'database': DATABASE_NAME
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Drop tables if exist
        print("Dropping existing tables...")
        cursor.execute("DROP TABLE IF EXISTS user_files")
        cursor.execute("DROP TABLE IF EXISTS vendor_rates")
        cursor.execute("DROP TABLE IF EXISTS vendors")
        cursor.execute("DROP TABLE IF EXISTS pcb_specification_options")
        
        # Create vendors table
        print("Creating vendors table...")
        cursor.execute("""
            CREATE TABLE vendors (
                vendor_id INT AUTO_INCREMENT PRIMARY KEY,
                vendor_name VARCHAR(255) NOT NULL,
                company_name VARCHAR(255),
                address TEXT,
                phone VARCHAR(50),
                email VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_vendor_name (vendor_name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create vendor_rates table
        print("Creating vendor_rates table...")
        cursor.execute("""
            CREATE TABLE vendor_rates (
                rate_id INT AUTO_INCREMENT PRIMARY KEY,
                vendor_id INT NOT NULL,
                num_layers INT NOT NULL,
                solder_mask ENUM('YES', 'NO') NOT NULL,
                thickness VARCHAR(50) NOT NULL,
                track_spacing VARCHAR(50) NOT NULL,
                via_drill_pad VARCHAR(50) NOT NULL,
                rate_per_sqcm DECIMAL(10, 4) NOT NULL,
                currency VARCHAR(10) DEFAULT 'INR',
                material VARCHAR(100),
                surface_finish VARCHAR(100),
                copper_thickness VARCHAR(50),
                min_quantity VARCHAR(50),
                bbt_charges VARCHAR(50),
                contract_period_start DATE,
                contract_period_end DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id) ON DELETE CASCADE,
                INDEX idx_vendor_specs (vendor_id, num_layers, solder_mask, thickness),
                INDEX idx_track_via (track_spacing, via_drill_pad),
                INDEX idx_rate (rate_per_sqcm)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create user_files table
        print("Creating user_files table...")
        cursor.execute("""
            CREATE TABLE user_files (
                file_id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                file_name VARCHAR(255),
                file_description TEXT,
                specifications JSON,
                vendors JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create pcb_specification_options table
        print("Creating pcb_specification_options table...")
        cursor.execute("""
            CREATE TABLE pcb_specification_options (
                option_id INT AUTO_INCREMENT PRIMARY KEY,
                field_name VARCHAR(100) NOT NULL,
                option_value VARCHAR(255) NOT NULL,
                display_order INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_field_option (field_name, option_value),
                INDEX idx_field_name (field_name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        connection.commit()
        print("\n[SUCCESS] All tables created successfully!")
        
        # Verify tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\nTables created: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        connection.close()
        
        return True
    except Error as e:
        print(f"\n[ERROR] {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Creating Database Tables")
    print("=" * 60)
    print()
    create_tables()

