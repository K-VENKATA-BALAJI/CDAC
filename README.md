# PCB Rate Calculator

A full-stack application for managing PCB (Printed Circuit Board) specifications and calculating vendor rates.

## Features

- **New File**: Create new PCB specifications and calculate rates from multiple vendors
- **Load File**: Load previously saved PCB specifications using email
- **PCB Specifications**: Configure various PCB parameters (layers, material, surface finish, etc.)
- **Rate Calculation**: Calculate and compare rates from multiple vendors
- **File Management**: Save specifications and rates with email reference

## Tech Stack

- **Frontend**: React with Axios
- **Backend**: Python with Tornado
- **Database**: SQLite
- **Data Source**: Excel files (for PCB specifications and vendor data)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create Excel files:
```bash
python create_excel_files.py
```

4. Start the Tornado server:
```bash
python server.py
```

The backend server will run on `http://localhost:8888`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Project Structure

```
CDAC/
├── backend/
│   ├── data/
│   │   ├── pcb_specifications.xlsx
│   │   └── pcb_vendors.xlsx
│   ├── database.py
│   ├── server.py
│   ├── create_excel_files.py
│   ├── requirements.txt
│   └── pcb_data.db (created automatically)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileSelection.js
│   │   │   ├── PCBCalculator.js
│   │   │   ├── PCBSpecifications.js
│   │   │   ├── PCBRates.js
│   │   │   └── FileManagement.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── README.md
```

## API Endpoints

- `GET /api/specifications` - Get PCB specification options
- `POST /api/calculate-rates` - Calculate vendor rates based on specifications
- `POST /api/save-file` - Save user file data
- `POST /api/load-file` - Load user file data by email

## Usage

1. Start both backend and frontend servers
2. Open the application in your browser
3. Choose "New File" to create specifications or "Load File" to load existing data
4. Fill in PCB specifications and click "Calculate Rate Contract"
5. Review vendor rates in the PCB Rates table
6. Save your configuration using the File Management section


