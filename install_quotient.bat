@echo off
echo 🚀 QUOTIENT BOT - INSTALLATION SCRIPT
echo ======================================
echo.
echo This script will install and setup Quotient Discord Bot
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11+ first.
    echo    Visit: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detected

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available. Please install pip first.
    pause
    exit /b 1
)

echo ✅ pip detected

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Run setup script
echo.
echo 🎯 Running Quotient Bot Setup...
python setup_quotient.py

echo.
echo 🎉 Installation completed!
echo.
echo 📖 Next steps:
echo    1. Read README_SETUP.md for detailed instructions
echo    2. Start your bot with: start_quotient.bat
echo    3. Join our support server for help
echo.
echo 🚀 Welcome to Quotient Bot!
pause

