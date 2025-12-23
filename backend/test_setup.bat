@echo off
echo ============================================================
echo MySQL Setup Test Script
echo ============================================================
echo.

echo Step 1: Testing MySQL connector...
python -c "import mysql.connector; print('[OK] MySQL connector installed')" 2>nul || echo [ERROR] MySQL connector not installed
echo.

echo Step 2: Please run the following commands manually:
echo   1. python setup_mysql.py
echo   2. python import_hiq_data.py
echo   3. python server.py
echo.

pause


