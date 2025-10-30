@echo off
echo 🛡️ SHIELD Backend Startup Script
echo.

REM Try different Python commands to find available Python
set PYTHON_CMD=

REM Try py launcher first (Windows)
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :found_python
)

REM Try python3
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :found_python
)

REM Try python
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :found_python
)

echo ❌ Python is not installed or not in PATH
echo Please install Python 3.8+ from https://python.org
echo Make sure to check "Add Python to PATH" during installation
pause
exit /b 1

:found_python
REM Get Python version and check if it's 3.8+
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found using %PYTHON_CMD%

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        echo This might be due to missing python-venv package
        echo Try installing Python from python.org with full installer
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    echo Trying to recreate virtual environment...
    rmdir /s /q venv
    %PYTHON_CMD% -m venv venv
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ❌ Still failed to activate virtual environment
        pause
        exit /b 1
    )
)

REM Upgrade pip first
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies with better error handling
echo 📦 Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install some dependencies
    echo Trying to install core dependencies only...
    python -m pip install "fastapi>=0.95.0,<1.0.0" "uvicorn[standard]>=0.20.0,<1.0.0" "pydantic>=2.0.0,<3.0.0" "pydantic-settings>=2.0.0,<3.0.0" "python-multipart>=0.0.5"
    if errorlevel 1 (
        echo ❌ Failed to install core dependencies
        echo Please check your internet connection and Python installation
        pause
        exit /b 1
    )
    echo ⚠️ Installed core dependencies only. Some features may be limited.
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    if exist ".env.example" (
        copy .env.example .env
    ) else (
        echo DEBUG=true > .env
        echo HOST=127.0.0.1 >> .env
        echo PORT=8000 >> .env
        echo LOG_LEVEL=INFO >> .env
    )
)

REM Start the server
echo.
echo 🚀 Starting SHIELD Backend Server...
echo.
echo The API will be available at:
echo   • API: http://127.0.0.1:8000
echo   • Docs: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause