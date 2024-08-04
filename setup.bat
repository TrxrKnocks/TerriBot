@echo off
echo Setting up the environment and running the script...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    pause
    exit /b 1
)

pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed or not in PATH. Please install pip and try again.
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

echo Running main.py...
python main.py

pause
