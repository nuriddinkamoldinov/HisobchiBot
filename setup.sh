#!/bin/bash

# Apartment Expense Bot Setup Script

echo "================================================"
echo "  Apartment Expense Management Bot Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.8"

if (( $(echo "$python_version < $required_version" | bc -l) )); then
    echo "❌ Error: Python 3.8 or higher is required"
    echo "   Your version: $python_version"
    exit 1
fi
echo "✓ Python version OK: $python_version"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi
echo ""

# Get bot token
echo "================================================"
echo "  Bot Token Configuration"
echo "================================================"
echo ""
echo "To create a Telegram bot:"
echo "1. Open Telegram and search for @BotFather"
echo "2. Send /newbot command"
echo "3. Follow the instructions"
echo "4. Copy the bot token you receive"
echo ""
read -p "Enter your bot token: " bot_token

if [ -z "$bot_token" ]; then
    echo "❌ Bot token cannot be empty"
    exit 1
fi

# Update the Python file with the token
sed -i "s/YOUR_BOT_TOKEN_HERE/$bot_token/" apartment_expense_bot.py
echo "✓ Bot token configured"
echo ""

# Initialize database
echo "Initializing database..."
python3 -c "from apartment_expense_bot import init_db; init_db()"
if [ $? -eq 0 ]; then
    echo "✓ Database initialized"
else
    echo "❌ Error initializing database"
    exit 1
fi
echo ""

echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "To start the bot, run:"
echo "  python3 apartment_expense_bot.py"
echo ""
echo "Then open your bot in Telegram and send /start"
echo ""
