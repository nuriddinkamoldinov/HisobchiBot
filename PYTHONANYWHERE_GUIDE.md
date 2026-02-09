# PythonAnywhere Deployment Guide - Step by Step

## 🎯 Overview
This guide will help you deploy your Kvartira Telegram bot on PythonAnywhere for **FREE**.

---

## 📋 Step 1: Sign Up

1. Go to https://www.pythonanywhere.com
2. Click **"Start running Python online in less than a minute!"**
3. Choose the **FREE "Beginner" account**
4. Complete registration (no credit card needed!)

---

## 📁 Step 2: Upload Your Files

### Option A: Upload via Web Interface (Easiest)

1. After logging in, click on **"Files"** tab at the top
2. Click **"Upload a file"** button
3. Upload these files one by one:
   - `apartment_expense_bot.py`
   - `requirements.txt`
   - `.env`

### Option B: Use Git (Recommended)

1. Click on **"Consoles"** tab
2. Click **"Bash"** to open a bash console
3. Run these commands:
   ```bash
   git clone YOUR_REPOSITORY_URL
   cd YOUR_REPOSITORY_NAME
   ```

---

## 🔧 Step 3: Install Dependencies

1. In the **Bash console**, run:
   ```bash
   cd ~/apartment_bot  # or your folder name
   pip3 install --user -r requirements.txt
   ```

2. Wait for installation to complete (2-3 minutes)

3. Verify installation:
   ```bash
   pip3 list | grep telegram
   ```
   You should see `python-telegram-bot`

---

## 🔑 Step 4: Set Up Environment Variables

If you uploaded `.env` file, you're good! Otherwise:

1. In Bash console, create the `.env` file:
   ```bash
   nano .env
   ```

2. Add your bot token:
   ```
   BOT_TOKEN=8569912959:AAETePcMQ4KTmAjCS9N2h4a9X2BOwMjw-oI
   ```

3. Save and exit:
   - Press `Ctrl + X`
   - Press `Y` to confirm
   - Press `Enter`

---

## 🚀 Step 5: Run Your Bot

### Method 1: Using Always-On Task (Paid Only - $5/month)

If you upgrade to paid account:
1. Go to **"Tasks"** tab
2. Create a new **always-on task**
3. Command: `python3 /home/yourusername/apartment_bot/apartment_expense_bot.py`

### Method 2: Using Scheduled Task (FREE - Recommended)

1. Go to **"Tasks"** tab
2. Under **"Scheduled tasks"** section
3. Click **"Create a new scheduled task"**
4. Settings:
   - **Frequency**: Daily at a specific time (e.g., 00:00)
   - **Command**: `cd /home/yourusername/apartment_bot && python3 apartment_expense_bot.py &`

⚠️ **Important**: Free tier tasks auto-stop after 100 seconds. We need Method 3 below!

### Method 3: Keep-Alive Script (FREE - Best for Free Tier)

**This is the BEST method for free tier!**

1. Create a keep-alive script in Bash console:
   ```bash
   nano ~/start_bot.sh
   ```

2. Add this content:
   ```bash
   #!/bin/bash
   cd ~/apartment_bot
   while true; do
       python3 apartment_expense_bot.py
       echo "Bot stopped. Restarting in 5 seconds..."
       sleep 5
   done
   ```

3. Save and exit (Ctrl+X, Y, Enter)

4. Make it executable:
   ```bash
   chmod +x ~/start_bot.sh
   ```

5. Create a scheduled task:
   - Go to **"Tasks"** tab
   - Create task with command: `/home/yourusername/start_bot.sh &`
   - Set to run daily

6. Start it manually first time:
   ```bash
   nohup ~/start_bot.sh > ~/bot.log 2>&1 &
   ```

---

## ✅ Step 6: Test Your Bot

1. Open Telegram and find your bot
2. Send `/start` command
3. Bot should respond in Uzbek!

---

## 📊 Step 7: Monitor Your Bot

### Check if bot is running:
```bash
ps aux | grep apartment_expense_bot
```

### View logs:
```bash
tail -f ~/bot.log
```

### Stop the bot:
```bash
pkill -f apartment_expense_bot
```

### Restart the bot:
```bash
~/start_bot.sh &
```

---

## 🔄 Step 8: Keep Bot Running (Important!)

⚠️ **PythonAnywhere Free Tier Limitations:**
- Console sessions timeout after 1 hour of inactivity
- You need to manually restart every few days/weeks

**Solutions:**

### A. Manual Restart (Simple)
- Log in to PythonAnywhere every few days
- Run: `~/start_bot.sh &`

### B. Use Scheduled Task (Better)
- Set up daily scheduled task to restart the bot
- Task command: `pkill -f apartment_expense_bot; nohup ~/start_bot.sh > ~/bot.log 2>&1 &`

### C. Upgrade to Paid ($5/month)
- Get "Always-On" tasks
- Bot runs 24/7 without manual intervention

---

## 🐛 Troubleshooting

### Bot not responding?
```bash
# Check if running
ps aux | grep apartment_expense_bot

# Check logs
tail -30 ~/bot.log

# Check for errors
python3 apartment_expense_bot.py
```

### Import errors?
```bash
# Reinstall dependencies
pip3 install --user --upgrade -r requirements.txt
```

### Database errors?
```bash
# Check if database file exists
ls -la ~/apartment_bot/apartment_bot.db

# If not, bot will create it on first run
```

### Bot token error?
```bash
# Check .env file
cat .env

# Make sure it has:
# BOT_TOKEN=your_token_here
```

---

## 🎉 Success Checklist

- ✅ Account created on PythonAnywhere
- ✅ Files uploaded (bot script, requirements.txt, .env)
- ✅ Dependencies installed
- ✅ Bot token configured
- ✅ Bot running and responding in Telegram
- ✅ Keep-alive script configured
- ✅ Scheduled task set up

---

## 📝 Important Notes

1. **Free Tier Limits:**
   - One console session at a time
   - Files expire after 3 months of inactivity (just log in to keep active)
   - 512 MB disk space
   - CPU time limited

2. **Database:**
   - Your SQLite database will persist on PythonAnywhere
   - It's saved in `~/apartment_bot/apartment_bot.db`

3. **Updates:**
   - To update bot code, just edit files or re-upload
   - Restart the bot after changes

4. **Security:**
   - Never share your `.env` file
   - Keep your PythonAnywhere password secure

---

## 💰 When to Upgrade?

Consider upgrading to paid ($5/month) if:
- You want true 24/7 uptime without manual restarts
- You have multiple users depending on the bot
- You want "Always-On" tasks

---

## 🆘 Need Help?

If you run into issues:
1. Check the logs: `tail -f ~/bot.log`
2. PythonAnywhere forums: https://www.pythonanywhere.com/forums/
3. Their help page: https://help.pythonanywhere.com/

---

**Your bot is now deployed! 🎉**
