@echo OFF
echo.
echo =========================================
echo  SerenDipity Insights - Setup Script
echo =========================================
echo.

REM Check if Python is installed and available in PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python and ensure it is added to your system's PATH.
    pause
    exit /b 1
)

echo [STEP 1] Creating Python virtual environment in 'venv' folder...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment created.
echo.

echo [STEP 2] Activating virtual environment and installing packages...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install required packages. Please check requirements.txt and your internet connection.
    pause
    exit /b 1
)
echo [SUCCESS] All packages installed.
echo.

echo =========================================
echo  Setup Complete!
echo  You can now run the dashboard by double-clicking 'run.bat'.
echo =========================================
echo.
pause