# 🚀 Quick Start - PythonAnywhere Deployment

## Copy-Paste Commands (In Order)

### 1️⃣ After signing up and opening Bash console:

```bash
# Install dependencies
pip3 install --user python-telegram-bot[job-queue] python-dotenv
```

### 2️⃣ Upload your files via "Files" tab:
- `apartment_expense_bot.py`
- `.env`
- `start_bot.sh`

### 3️⃣ Make start script executable:

```bash
cd ~/  # or wherever you uploaded files
chmod +x start_bot.sh
```

### 4️⃣ Start the bot:

```bash
nohup ./start_bot.sh > bot.log 2>&1 &
```

### 5️⃣ Check if it's running:

```bash
ps aux | grep apartment_expense_bot
```

### 6️⃣ View logs (to see if it's working):

```bash
tail -f bot.log
```

Press `Ctrl+C` to stop viewing logs (bot keeps running).

---

## 🔄 Daily Commands

### Check if bot is running:
```bash
ps aux | grep apartment_expense_bot
```

### View recent logs:
```bash
tail -30 bot.log
```

### Stop the bot:
```bash
pkill -f apartment_expense_bot
```

### Restart the bot:
```bash
nohup ./start_bot.sh > bot.log 2>&1 &
```

---

## ⚠️ Important

**Free tier limitation:** You'll need to log in and restart the bot every few days/weeks.

**Solution:** Set up a scheduled task in PythonAnywhere:
- Go to "Tasks" tab
- Add: `cd /home/yourusername && nohup ./start_bot.sh > bot.log 2>&1 &`
- Run daily

---

## ✅ Done!

Your bot should now be running 24/7 (with occasional manual restarts on free tier).

Test it in Telegram by sending `/start` to your bot!
