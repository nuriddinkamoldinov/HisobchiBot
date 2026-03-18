# Hisobchi Bot

Telegram bot for managing shared apartment expenses among roommates.

## Requirements

- Python 3.8+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

---

## Installation

### Linux (Ubuntu)

**1. Clone the repository**
```bash
git clone <repo-url>
cd Kvartira
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Configure the bot token**
```bash
cp .env.example .env
nano .env
```
Set your token:
```
BOT_TOKEN=your_token_here
```

**4. Test run**
```bash
source venv/bin/activate
python3 apartment_expense_bot.py
```

---

### macOS

**1. Clone the repository**
```bash
git clone <repo-url>
cd Kvartira
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Configure the bot token**
```bash
cp .env.example .env
nano .env
```
Set your token:
```
BOT_TOKEN=your_token_here
```

**4. Test run**
```bash
source venv/bin/activate
python3 apartment_expense_bot.py
```

---

### Windows

**1. Clone the repository**
```cmd
git clone <repo-url>
cd Kvartira
```

**2. Create a virtual environment and install dependencies**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configure the bot token**

Create a `.env` file in the project folder with:
```
BOT_TOKEN=your_token_here
```

**4. Test run**
```cmd
venv\Scripts\activate
python apartment_expense_bot.py
```

---

## Running as a System Service

### Linux (Ubuntu) — systemd

This makes the bot start automatically on boot and restart if it crashes.

**1. Create the service file**
```bash
sudo nano /etc/systemd/system/Hisobchibot.service
```

**2. Paste the following** (adjust username and paths if needed):
```ini
[Unit]
Description=Kvartira Telegram Bot
After=network.target

[Service]
Type=simple
User=nooriddin
WorkingDirectory=/home/nooriddin/Projects/Python/TelegramBot/Kvartira
ExecStart=/home/nooriddin/Projects/Python/TelegramBot/Kvartira/venv/bin/python3 /home/nooriddin/Projects/Python/TelegramBot/Kvartira/apartment_expense_bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**3. Enable and start**
```bash
sudo systemctl daemon-reload
sudo systemctl enable Hisobchibot
sudo systemctl start Hisobchibot
```

**Service management:**
```bash
sudo systemctl status Hisobchibot    # check status
sudo systemctl stop Hisobchibot      # stop
sudo systemctl start Hisobchibot     # start
sudo systemctl restart Hisobchibot   # restart after code changes
journalctl -u Hisobchibot -f         # live logs
```

---

### macOS — launchd

**1. Create the plist file**
```bash
nano ~/Library/LaunchAgents/com.hisobchibot.plist
```

**2. Paste the following** (adjust username and paths if needed):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hisobchibot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/username/Kvartira/venv/bin/python3</string>
        <string>/Users/username/Kvartira/apartment_expense_bot.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/username/Kvartira</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/hisobchibot.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/hisobchibot.err</string>
</dict>
</plist>
```

**3. Enable and start**
```bash
launchctl load ~/Library/LaunchAgents/com.hisobchibot.plist
```

**Service management:**
```bash
launchctl start com.hisobchibot      # start
launchctl stop com.hisobchibot       # stop
launchctl unload ~/Library/LaunchAgents/com.hisobchibot.plist  # remove
tail -f /tmp/hisobchibot.log         # live logs
```

---

### Windows — Task Scheduler

This makes the bot start automatically on boot.

**1. Create a startup script**

Create `start_bot.bat` in the project folder:
```bat
@echo off
cd /d C:\path\to\Kvartira
call venv\Scripts\activate
python apartment_expense_bot.py
```

**2. Open Task Scheduler**
- Press `Win + S`, search for **Task Scheduler**, open it
- Click **Create Basic Task**

**3. Configure the task**
- Name: `Hisobchibot`
- Trigger: **When the computer starts**
- Action: **Start a program**
- Program: `C:\path\to\Kvartira\start_bot.bat`
- Check **"Run whether user is logged on or not"**
- Check **"Run with highest privileges"**
- Click Finish

**4. Verify**

Open Task Scheduler, find `Hisobchibot`, right-click → **Run** to test it.

**Task management (Command Prompt as Administrator):**
```cmd
schtasks /run /tn "Hisobchibot"      # start
schtasks /end /tn "Hisobchibot"      # stop
schtasks /delete /tn "Hisobchibot"   # remove task
```

---

## Fresh Start (Reset Data)

To reset all data, stop the bot, delete the database, then start again:

**Linux:**
```bash
sudo systemctl stop Hisobchibot
rm apartment_bot.db
sudo systemctl start Hisobchibot
```

**macOS:**
```bash
launchctl stop com.hisobchibot
rm apartment_bot.db
launchctl start com.hisobchibot
```

**Windows:**
```cmd
schtasks /end /tn "Hisobchibot"
del apartment_bot.db
schtasks /run /tn "Hisobchibot"
```

The database will be recreated automatically on next start.
