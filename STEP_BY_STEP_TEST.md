# Step-by-Step Testing Guide

## Quick Start - Follow These Steps in Order

### Step 1: Verify MySQL is Running

Make sure MySQL Server is installed and running on your system.

**Check MySQL:**
- Open Command Prompt or PowerShell
- Try: `mysql --version`
- If not found, install MySQL Server first

### Step 2: Setup Database

Open a terminal in the `backend` folder and run:

```bash
cd backend
python setup_mysql.py
```

**What to expect:**
- It will ask for MySQL root password
- Enter your MySQL password (or press Enter if no password)
- It will create the database and tables
- You should see: "Database setup completed successfully!"

### Step 3: Configure Database Password

Before importing data, update the MySQL password in these files:

**File 1: `backend/database_mysql.py`**
- Find line ~12: `'password': ''`
- Change to: `'password': 'your_mysql_password'`

**File 2: `backend/import_hiq_data.py`**
- Find line ~10: `'password': ''`
- Change to: `'password': 'your_mysql_password'`

### Step 4: Import HIQ Data

```bash
python import_hiq_data.py
```

**What to expect:**
- It will parse the Excel file
- Show vendor information
- Show sample rate records
- Import data into MySQL
- You should see: "Successfully imported [number] rate records"

### Step 5: Verify Import

Connect to MySQL to verify:

```bash
mysql -u root -p
```

Then run:
```sql
USE pcb_rate_contract;
SELECT COUNT(*) FROM vendor_rates;
SELECT * FROM vendors;
SELECT * FROM vendor_rates LIMIT 5;
EXIT;
```

You should see:
- 1 vendor (HIQ)
- Hundreds of rate records
- Sample rate data

### Step 6: Start Backend Server

```bash
python server.py
```

**What to expect:**
- Server starts on http://localhost:8888
- No errors about database connection
- Message: "Server running on http://localhost:8888"

### Step 7: Test API (Optional)

Open a new terminal and test:

```bash
# Test specifications endpoint
curl http://localhost:8888/api/specifications

# Test rate calculation
curl -X POST http://localhost:8888/api/calculate-rates -H "Content-Type: application/json" -d "{\"specifications\":{\"Num of Layers\":\"2\",\"Thickness\":\"1.6mm\",\"Track / Spacing\":\"6/6 mil\",\"Via Hole/Pad\":\"12/24 mil\"}}"
```

### Step 8: Test Frontend

**Terminal 1 (Backend):**
```bash
cd backend
python server.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

**Browser:**
1. Open http://localhost:3000
2. Click "File" → "New File"
3. Select specifications:
   - Num of Layers: 2
   - Thickness: 1.6mm
   - Track / Spacing: 6/6 mil
   - Via Hole/Pad: 12/24 mil
4. Click "Calculate Rate Contract"
5. Should see HIQ vendor rates displayed

### Step 9: Test Save/Load

1. Fill in File Name, Description, Email
2. Click "SAVE"
3. Click "File" → "Load File"
4. Enter the same email
5. Should load your saved data

## Troubleshooting

### "Error connecting to MySQL"
- **Check:** MySQL server is running
- **Check:** Password is correct in both files
- **Check:** MySQL is accessible on localhost

### "Database doesn't exist"
- **Solution:** Run `python setup_mysql.py` again

### "No rates returned"
- **Check:** Data was imported: `SELECT COUNT(*) FROM vendor_rates;`
- **Check:** Specifications match exactly (case-sensitive)
- **Note:** Thickness format must match (e.g., "1.6" not "1.6mm" in database)

### "Import script fails"
- **Check:** Excel file path is correct
- **Check:** Excel file is not open
- **Check:** File permissions

## Quick Verification Commands

```bash
# Check MySQL connector
python -c "import mysql.connector; print('OK')"

# Check if database exists (requires MySQL access)
mysql -u root -p -e "SHOW DATABASES LIKE 'pcb_rate_contract';"

# Check table count
mysql -u root -p -e "USE pcb_rate_contract; SHOW TABLES;"

# Check rate count
mysql -u root -p -e "USE pcb_rate_contract; SELECT COUNT(*) FROM vendor_rates;"
```

## Success Indicators

✅ Database created  
✅ Tables created (4 tables)  
✅ HIQ vendor imported  
✅ Hundreds of rate records imported  
✅ Backend server starts without errors  
✅ Frontend displays rates  
✅ Save/Load works  

## Next Steps After Testing

1. Add more vendors by importing their Excel files
2. Customize specification options
3. Test with different specification combinations
4. Verify all rates are correct

