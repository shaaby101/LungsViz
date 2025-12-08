@echo off
REM Lungs Exposure Risk Visualizer - Quick Start (Windows)

echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║     LUNGS EXPOSURE RISK VISUALIZER - Quick Start (Windows)       ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python detected
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt -q

echo.
echo 🔑 Checking for .env file...
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo.
    echo 1. Visit: https://openweathermap.org/api
    echo 2. Create a free account
    echo 3. Get your API key
    echo 4. Create a .env file in this directory with:
    echo.
    echo OPENWEATHER_API_KEY=your_api_key_here
    echo.
    pause
)

echo.
echo 🚀 Starting Flask server...
echo.
echo ==========================================
echo Opening browser to: http://localhost:5000
echo ==========================================
echo.
echo Press Ctrl+C to stop the server
echo.

start http://localhost:5000
python app.py

pause
