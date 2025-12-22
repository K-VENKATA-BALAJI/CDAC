# Complete Testing Guide - MySQL Implementation

## Prerequisites Check

Before starting, ensure you have:
- ✅ MySQL Server installed and running
- ✅ MySQL root password (or user credentials)
- ✅ Python installed
- ✅ Backend dependencies installed

## Step-by-Step Testing Process

### Step 1: Install MySQL Python Dependencies

```bash
cd backend
pip install mysql-connector-python pymysql
```

### Step 2: Setup MySQL Database

Run the setup script:

```bash
python setup_mysql.py
```

This will:
- Prompt for MySQL password
- Create `pcb_rate_contract` database
- Create all necessary tables

**Expected Output:**
```
Setting up MySQL database...
============================================================
1. Creating database...
Database 'pcb_rate_contract' created or already exists

2. Creating tables...
Tables created successfully
============================================================
Database setup completed successfully!
```

### Step 3: Configure Database Connection

Update MySQL password in these files:

1. **backend/database_mysql.py** (around line 12):
```python
'password': 'your_mysql_password'  # Replace with your password
```

2. **backend/import_hiq_data.py** (around line 10):
```python
'password': 'your_mysql_password'  # Replace with your password
```

### Step 4: Import HIQ Rate Contract Data

```bash
python import_hiq_data.py
```

**Expected Output:**
```
Parsing Excel file...
Vendor: Hi-Q Electronics Private Limited
Total rate records found: [number]

Sample rate records:
1. Layers: 2, Solder Mask: YES, Thickness: below 0.8, ...
...

Importing to database...
Vendor ID: 1
Cleared existing rates for vendor HIQ
Successfully imported [number] rate records
Import completed!
```

### Step 5: Verify Database Import

Connect to MySQL and verify:

```bash
mysql -u root -p
```

Then run:
```sql
USE pcb_rate_contract;

-- Check vendor
SELECT * FROM vendors;

-- Check rate count
SELECT COUNT(*) as total_rates FROM vendor_rates;

-- Sample rates
SELECT * FROM vendor_rates LIMIT 10;

-- Check rates for 2 layers
SELECT num_layers, thickness, track_spacing, via_drill_pad, rate_per_sqcm 
FROM vendor_rates 
WHERE num_layers = 2 
LIMIT 10;
```

### Step 6: Start Backend Server

```bash
python server.py
```

**Expected Output:**
```
Server running on http://localhost:8888
```

If you see a warning about MySQL, check your configuration.

### Step 7: Test API Endpoints

#### Test 1: Get Specifications
```bash
curl http://localhost:8888/api/specifications
```

Should return JSON with specification options.

#### Test 2: Calculate Rates
```bash
curl -X POST http://localhost:8888/api/calculate-rates \
  -H "Content-Type: application/json" \
  -d "{\"specifications\":{\"Num of Layers\":\"2\",\"Thickness\":\"1.6mm\",\"Track / Spacing\":\"6/6 mil\",\"Via Hole/Pad\":\"12/24 mil\"}}"
```

Should return vendor rates matching the specifications.

### Step 8: Test Frontend

1. Start frontend (in a new terminal):
```bash
cd frontend
npm start
```

2. Open browser to `http://localhost:3000`

3. Test Flow:
   - Click "File" → "New File"
   - Select specifications:
     - Num of Layers: 2
     - Thickness: 1.6mm
     - Track / Spacing: 6/6 mil
     - Via Hole/Pad: 12/24 mil
   - Click "Calculate Rate Contract"
   - Should see HIQ vendor rates
   - Fill in File Name, Description, Email
   - Click "SAVE"
   - Click "File" → "Load File"
   - Enter email
   - Should load saved data

## Troubleshooting

### Issue: "Error connecting to MySQL"
**Solution:**
- Check MySQL server is running
- Verify password is correct
- Check host is 'localhost'

### Issue: "Database doesn't exist"
**Solution:**
- Run `python setup_mysql.py` again
- Check MySQL user has CREATE DATABASE privileges

### Issue: "No rates returned"
**Solution:**
- Verify data was imported: `SELECT COUNT(*) FROM vendor_rates;`
- Check specifications match exactly (case-sensitive)
- Verify thickness format matches (e.g., "1.6" vs "1.6mm")

### Issue: "Import script fails"
**Solution:**
- Check Excel file path is correct
- Verify Excel file is not open in another program
- Check file permissions

### Issue: "Server shows SQLite warning"
**Solution:**
- Check `database_mysql.py` import works
- Verify MySQL dependencies installed
- Check for syntax errors in database_mysql.py

## Verification Checklist

- [ ] MySQL dependencies installed
- [ ] Database created successfully
- [ ] Tables created successfully
- [ ] HIQ data imported (check count > 0)
- [ ] Backend server starts without errors
- [ ] API endpoints respond correctly
- [ ] Frontend connects to backend
- [ ] Rate calculation works
- [ ] Save/Load file works

## Expected Results

After successful setup:
- Database has 1 vendor (HIQ)
- Database has hundreds of rate records
- API returns rates when specifications match
- Frontend displays rates correctly
- Save/Load functionality works

## Next Steps After Testing

1. Add more vendors by importing their Excel files
2. Customize specification options
3. Add more specification fields if needed
4. Optimize queries if performance is slow

