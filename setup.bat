@echo off
REM Apartment Expense Bot Setup Script for Windows

echo ================================================
echo   Apartment Expense Management Bot Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Get bot token
echo ================================================
echo   Bot Token Configuration
echo ================================================
echo.
echo To create a Telegram bot:
echo 1. Open Telegram and search for @BotFather
echo 2. Send /newbot command
echo 3. Follow the instructions
echo 4. Copy the bot token you receive
echo.
set /p bot_token="Enter your bot token: "

if "%bot_token%"=="" (
    echo Bot token cannot be empty
    pause
    exit /b 1
)

REM Update the Python file with the token
powershell -Command "(gc apartment_expense_bot.py) -replace 'YOUR_BOT_TOKEN_HERE', '%bot_token%' | Out-File -encoding ASCII apartment_expense_bot.py"
echo Bot token configured
echo.

REM Initialize database
echo Initializing database...
python -c "from apartment_expense_bot import init_db; init_db()"
if errorlevel 1 (
    echo Error initializing database
    pause
    exit /b 1
)
echo Database initialized
echo.

echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To start the bot, run:
echo   python apartment_expense_bot.py
echo.
echo Then open your bot in Telegram and send /start
echo.
pause
