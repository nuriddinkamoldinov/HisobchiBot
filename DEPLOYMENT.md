# Kvartira Bot Deployment Guide

## Option 1: PythonAnywhere (Free & Easy)

### Steps:
1. Sign up at https://www.pythonanywhere.com (Free account)
2. Go to "Files" tab and upload your files:
   - `apartment_expense_bot.py`
   - `requirements.txt`
3. Open a Bash console and install dependencies:
   ```bash
   pip3 install --user -r requirements.txt
   ```
4. Go to "Tasks" tab and create a new task:
   - Command: `python3 apartment_expense_bot.py`
   - Set to run daily (it will keep running)
5. Or use "Always-on tasks" (requires paid account)

**Pros:** Easy setup, free tier
**Cons:** Free tier has limitations, may need paid account for always-on

---

## Option 2: VPS (DigitalOcean, AWS, Google Cloud)

### Steps:
1. Create a VPS (Ubuntu 22.04 recommended)
2. SSH into your server
3. Install Python and dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install python-telegram-bot
   ```
4. Upload your bot files using `scp` or `git clone`
5. Create a systemd service to keep it running:

Create `/etc/systemd/system/kvartira-bot.service`:
```ini
[Unit]
Description=Kvartira Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/kvartira-bot
ExecStart=/usr/bin/python3 apartment_expense_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

6. Enable and start the service:
   ```bash
   sudo systemctl enable kvartira-bot
   sudo systemctl start kvartira-bot
   sudo systemctl status kvartira-bot
   ```

**Pros:** Full control, reliable, scalable
**Cons:** Requires Linux knowledge, costs $5-10/month

---

## Option 3: Railway.app (Modern & Easy)

### Steps:
1. Sign up at https://railway.app
2. Connect your GitHub repository or upload code
3. Add `runtime.txt` with Python version:
   ```
   python-3.12
   ```
4. Railway will auto-detect Python and install requirements
5. Deploy!

**Pros:** Modern, easy deployment, free tier
**Cons:** Free tier has limits

---

## Option 4: Heroku (Popular Choice)

### Steps:
1. Sign up at https://heroku.com
2. Install Heroku CLI
3. Create `Procfile`:
   ```
   worker: python3 apartment_expense_bot.py
   ```
4. Deploy:
   ```bash
   heroku login
   heroku create kvartira-bot
   git push heroku main
   heroku ps:scale worker=1
   ```

**Pros:** Easy to use, good documentation
**Cons:** No free tier anymore (starts at $5/month)

---

## Option 5: Local Server / Raspberry Pi

### Steps:
1. Install Python on your server/Pi
2. Set up the bot to run on startup using cron or systemd
3. Keep your computer/Pi running 24/7

**Pros:** Free, full control
**Cons:** Needs 24/7 power, internet connection

---

## Recommended Option for You:

**For beginners:** Start with **PythonAnywhere** (free and easy)
**For production:** Use a **VPS with systemd service** (most reliable)
**For quick deploy:** Try **Railway.app** (modern and simple)

---

## Before Deploying - IMPORTANT SECURITY:

⚠️ **Never commit your bot token to GitHub!**

Your current code has the token hardcoded (line 938). You should:

1. Create a `.env` file:
   ```
   BOT_TOKEN=8569912959:AAETePcMQ4KTmAjCS9N2h4a9X2BOwMjw-oI
   ```

2. Add `.env` to `.gitignore`:
   ```
   .env
   apartment_bot.db
   __pycache__/
   ```

3. Update your code to use environment variables:
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   TOKEN = os.getenv('BOT_TOKEN')
   ```

4. Add `python-dotenv` to requirements.txt
