# 🚀 How to Run - Complete Guide

## Step 1: Setup Database ✅

Run this command in the `backend` folder:

```bash
cd backend
python setup_database_simple.py
```

**Expected Output:**
```
============================================================
MySQL Database Setup
============================================================

Using password: (set)
[OK] Database 'pcb_rate_contract' created or already exists
[OK] Executed X SQL statements
[OK] Tables created successfully
[SUCCESS] Database setup completed!
```

---

## Step 2: Import HIQ Data ✅

Still in the `backend` folder, run:

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

---

## Step 3: Start Backend Server ✅

Keep the terminal in `backend` folder and run:

```bash
python server.py
```

**Expected Output:**
```
Server running on http://localhost:8888
```

**Keep this terminal open!** The server must keep running.

---

## Step 4: Start Frontend ✅

Open a **NEW** terminal/PowerShell window and run:

```bash
cd frontend
npm start
```

**Expected Output:**
```
Compiled successfully!
You can now view pcb-rate-calculator in the browser.
  Local:            http://localhost:3000
```

The browser should automatically open at `http://localhost:3000`

---

## Step 5: Test the Application ✅

### Test Rate Calculation:

1. **Click "File"** in the top-left corner
2. **Click "New File"**
3. **Select specifications:**
   - Num of Layers: **2**
   - Thickness: **1.6mm**
   - Track / Spacing: **6/6 mil**
   - Via Hole/Pad: **12/24 mil**
   - (Other fields can be left as default)
4. **Click "Calculate Rate Contract"** (yellow button)
5. **Expected:** You should see HIQ vendor rates displayed in the table

### Test Save/Load:

1. **Fill in the form at the bottom:**
   - File Name: `Test PCB`
   - File Description: `Test description`
   - Email: `test@example.com`
2. **Click "SAVE"** (green button)
3. **Click "File" → "Load File"**
4. **Enter the same email:** `test@example.com`
5. **Expected:** Your saved data loads with all specifications and rates

---

## Quick Command Reference

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

---

## Troubleshooting

### Backend won't start?
- Check MySQL is running
- Verify password is correct in `database_mysql.py`
- Check port 8888 is not in use

### No rates showing?
- Verify data was imported: Check terminal output for "Successfully imported"
- Check specifications match exactly (case-sensitive)
- Try different specification combinations

### Frontend won't connect?
- Make sure backend is running first
- Check browser console (F12) for errors
- Verify backend shows "Server running on http://localhost:8888"

### Import failed?
- Check MySQL password is correct in `import_hiq_data.py`
- Verify Excel file exists: `HIQ_Rate contract.xlsx`
- Check MySQL server is running

---

## Success Indicators ✅

- ✅ Database created with 4 tables
- ✅ 1132 rate records imported
- ✅ Backend server running on port 8888
- ✅ Frontend running on port 3000
- ✅ Rates display when calculating
- ✅ Save/Load functionality works

---

## What's Running?

**Backend Server:**
- Port: 8888
- URL: http://localhost:8888
- Status: Check terminal for "Server running..."

**Frontend App:**
- Port: 3000
- URL: http://localhost:3000
- Status: Browser should be open

---

## Next Steps After Testing

1. ✅ Test with different specification combinations
2. ✅ Verify all rates are correct
3. ✅ Add more vendors (import their Excel files)
4. ✅ Customize specification options

---

**You're all set! Start with Step 1 and work through each step.** 🎉

