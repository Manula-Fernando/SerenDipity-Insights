@echo OFF
echo.
echo =========================================
echo  SerenDipity Insights - Run Script
echo =========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment 'venv' not found.
    echo Please run 'setup.bat' first to set up the project.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [INFO] Starting the Dash application...
echo You can access the dashboard at http://127.0.0.1:8050/
echo Press CTRL+C in this window to stop the server.
echo.

python app.py
