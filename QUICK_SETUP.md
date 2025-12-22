# Quick Setup Guide - Fixed Import Script

## ✅ Good News!
The import script is now fixed and working! It successfully parsed **1132 rate records** from the HIQ Excel file.

## Next Steps:

### Step 1: Setup Database

**Option A: Simple Method (Recommended)**

1. Open `backend/setup_database_simple.py`
2. Update line 9 with your MySQL password:
   ```python
   MYSQL_PASSWORD = 'your_password'  # Or leave empty if no password
   ```
3. Run:
   ```bash
   cd backend
   python setup_database_simple.py
   ```

**Option B: Original Method**

Run and enter password when prompted:
```bash
cd backend
python setup_mysql.py
```

### Step 2: Configure Password in Import Script

Open `backend/import_hiq_data.py` and update line 10:
```python
'password': 'your_mysql_password'  # Update this
```

### Step 3: Import Data

```bash
python import_hiq_data.py
```

**Expected Output:**
```
Parsing Excel file...
Vendor: Hi-Q Electronics Private Limited
Total rate records found: 1132
...
Importing to database...
Vendor ID: 1
Successfully imported 1132 rate records
Import completed!
```

### Step 4: Verify Import

```bash
mysql -u root -p
```

Then:
```sql
USE pcb_rate_contract;
SELECT COUNT(*) FROM vendor_rates;
SELECT * FROM vendors;
EXIT;
```

Should show:
- 1 vendor (HIQ)
- 1132 rate records

### Step 5: Start Server and Test

```bash
# Terminal 1 - Backend
cd backend
python server.py

# Terminal 2 - Frontend  
cd frontend
npm start
```

Then test in browser at http://localhost:3000

## What Was Fixed

The import script now:
- ✅ Properly validates layer values (skips text rows)
- ✅ Handles "Additional Cost" and other non-data rows
- ✅ Extracts numbers from strings when needed
- ✅ Successfully parsed 1132 rate records

## Troubleshooting

**"Table doesn't exist"**
→ Run `python setup_database_simple.py` first

**"Error connecting to MySQL"**
→ Check password is correct in both files

**"No rates imported"**
→ Check Excel file path is correct

