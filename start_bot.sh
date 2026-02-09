#!/bin/bash
# Keep-alive script for PythonAnywhere
# This script will automatically restart your bot if it crashes

cd "$(dirname "$0")"

echo "Starting Kvartira Telegram Bot..."
echo "Bot will auto-restart if it crashes"
echo "Press Ctrl+C to stop"
echo ""

while true; do
    echo "[$(date)] Starting bot..."
    python3 apartment_expense_bot.py

    EXIT_CODE=$?
    echo "[$(date)] Bot stopped with exit code: $EXIT_CODE"

    if [ $EXIT_CODE -eq 0 ]; then
        echo "Bot stopped normally. Restarting in 5 seconds..."
    else
        echo "Bot crashed! Restarting in 10 seconds..."
        sleep 10
        continue
    fi

    sleep 5
done
