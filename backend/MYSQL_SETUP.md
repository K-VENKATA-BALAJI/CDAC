# MySQL Database Setup Guide

## Prerequisites
- MySQL Server installed and running
- MySQL root access (or user with CREATE DATABASE privileges)

## Step 1: Install MySQL Python Connector

```bash
pip install mysql-connector-python pymysql
```

## Step 2: Setup Database

Run the setup script to create the database and tables:

```bash
python setup_mysql.py
```

This will:
- Create the `pcb_rate_contract` database
- Create all necessary tables (vendors, vendor_rates, user_files, pcb_specification_options)

## Step 3: Configure Database Connection

Update the database configuration in these files:

1. **backend/database_mysql.py** - Update the `config` dictionary:
```python
self.config = {
    'host': 'localhost',
    'database': 'pcb_rate_contract',
    'user': 'root',
    'password': 'your_mysql_password'  # Update this
}
```

2. **backend/import_hiq_data.py** - Update the `DB_CONFIG` dictionary:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'pcb_rate_contract',
    'user': 'root',
    'password': 'your_mysql_password'  # Update this
}
```

3. **backend/setup_mysql.py** - Update the `DB_CONFIG` dictionary if needed

## Step 4: Import HIQ Rate Contract Data

```bash
python import_hiq_data.py
```

This will:
- Parse the "HIQ_Rate contract.xlsx" file
- Extract vendor information
- Extract all rate data
- Import into MySQL database

## Step 5: Update Server to Use MySQL

Update `backend/server.py` to use MySQL instead of SQLite:

```python
# Change this import
from database_mysql import Database  # Instead of database
```

## Database Schema Overview

### vendors
Stores vendor/company information

### vendor_rates
Stores rate contract data with specifications:
- num_layers (1, 2, 4, 6, etc.)
- solder_mask (YES/NO)
- thickness (0.8, 1.6, 2.4, etc.)
- track_spacing (8/8 mil, 6/6 mil, etc.)
- via_drill_pad (12/24 mil, 10/20 mil, etc.)
- rate_per_sqcm (rate in Rs per square cm)

### user_files
Stores user-saved specifications and calculated rates

### pcb_specification_options
Stores available options for each specification field

## Testing the Import

After importing, verify the data:

```sql
-- Check vendor
SELECT * FROM vendors;

-- Check rate count
SELECT COUNT(*) FROM vendor_rates;

-- Sample rates
SELECT * FROM vendor_rates LIMIT 10;

-- Rates for 2 layers, YES solder mask
SELECT * FROM vendor_rates 
WHERE num_layers = 2 AND solder_mask = 'YES' 
LIMIT 10;
```

## Adding More Vendors

To add more vendors:
1. Create similar Excel files with the same structure
2. Modify `import_hiq_data.py` to handle multiple files or create new import scripts
3. Run the import script for each vendor


