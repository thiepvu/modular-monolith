@echo off
REM Quick Setup Helper Script for Windows

echo Setting up Modular Monolith Project...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Setup environment
echo Setting up environment...
copy .env.example .env
echo Please edit .env with your database credentials

REM Database setup
echo.
echo To complete setup, run:
echo   1. createdb modular_db
echo   2. python scripts/migrate.py --upgrade
echo   3. python scripts/seed.py
echo   4. python src/main.py
echo.
echo Then visit: http://localhost:8000/api/docs

pause
