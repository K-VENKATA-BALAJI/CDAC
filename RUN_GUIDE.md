# Step-by-Step Run Guide

## Prerequisites Check
Make sure you have:
- ✅ Python 3.7 or higher installed
- ✅ Node.js and npm installed

To check:
```bash
python --version
node --version
npm --version
```

---

## Step 1: Install Backend Dependencies

Open a terminal/PowerShell and run:

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- tornado (web server)
- openpyxl (Excel file handling)
- sqlalchemy (database)

**Note:** Excel files are already created in `backend/data/` folder.

---

## Step 2: Start the Backend Server

Keep the terminal open and run:

```bash
python server.py
```

You should see:
```
Server running on http://localhost:8888
```

**Keep this terminal window open!** The backend must stay running.

---

## Step 3: Install Frontend Dependencies

Open a **NEW** terminal/PowerShell window and run:

```bash
cd frontend
npm install
```

This will install React and all frontend dependencies. This may take a few minutes.

---

## Step 4: Start the Frontend

In the same frontend terminal, run:

```bash
npm start
```

This will:
- Start the React development server
- Open your browser automatically at `http://localhost:3000`
- If it doesn't open automatically, go to `http://localhost:3000` manually

---

## You're Ready! 🎉

The application should now be running:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8888

### How to Use:
1. Click **"New File"** to create a new PCB specification
2. Select specifications from dropdowns
3. Click **"Calculate Rate Contract"** to see vendor rates
4. Fill in File Name, Description, and Email
5. Click **"SAVE"** to save your configuration
6. Click **"Load File"** and enter your email to retrieve saved files

---

## Troubleshooting

### Backend Issues:
- **Port 8888 already in use**: Close other applications using that port
- **Module not found**: Make sure you ran `pip install -r requirements.txt`
- **Excel file error**: Run `python create_excel_files.py` in the backend folder

### Frontend Issues:
- **Port 3000 already in use**: The terminal will ask to use a different port (press Y)
- **npm install fails**: Make sure Node.js is installed correctly
- **Can't connect to backend**: Make sure backend is running first!

### Both Running but Not Working:
- Check that backend shows "Server running on http://localhost:8888"
- Check browser console (F12) for any errors
- Make sure CORS is working (backend has CORS enabled)

---

## Quick Commands Reference

**Backend:**
```bash
cd backend
pip install -r requirements.txt    # First time only
python server.py                   # Start server
```

**Frontend:**
```bash
cd frontend
npm install                        # First time only
npm start                          # Start app
```

---

## Stopping the Application

- **Backend**: Press `Ctrl+C` in the backend terminal
- **Frontend**: Press `Ctrl+C` in the frontend terminal


