# Quick Setup Guide

## Prerequisites
- Python 3.7+ installed
- Node.js and npm installed

## Step-by-Step Setup

### 1. Backend Setup

Open a terminal and run:

```bash
cd backend
pip install -r requirements.txt
python create_excel_files.py
python server.py
```

The backend will start on `http://localhost:8888`

### 2. Frontend Setup

Open a **new** terminal window and run:

```bash
cd frontend
npm install
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

## Using the Application

1. **New File**: Click "New File" to create a new PCB specification
   - Select specifications from the dropdowns
   - Click "Calculate Rate Contract" to see vendor rates
   - Fill in File Name, Description, and Email
   - Click "SAVE" to save your configuration

2. **Load File**: Click "Load File" to retrieve saved configurations
   - Enter your email address
   - Your saved file will be loaded with all specifications and rates

## Troubleshooting

- **Backend not starting**: Make sure port 8888 is not in use
- **Frontend not connecting**: Ensure backend is running first
- **Excel files missing**: Run `python create_excel_files.py` in the backend directory
- **Database errors**: The SQLite database will be created automatically on first run


