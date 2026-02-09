# 🚂 Railway.app Deployment Guide

## 🎯 Overview
Deploy your Kvartira Telegram bot to Railway.app in minutes!

**Cost:** $5/month after free trial ($5 free credit for new users)

---

## ✅ **Prerequisites Checklist**

Before starting, make sure you have:
- ✅ All your bot files ready
- ✅ GitHub account (free)
- ✅ Railway account (sign up below)

---

## 📦 **Step 1: Prepare Your Code (Already Done!)**

Your code is already prepared with these files:
- ✅ `apartment_expense_bot.py` - Your bot code
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Tells Railway how to run your bot
- ✅ `runtime.txt` - Specifies Python version
- ✅ `.env` - Your bot token (will be added in Railway)
- ✅ `.gitignore` - Protects sensitive files

**All set!** ✨

---

## 🔐 **Step 2: Push to GitHub**

### Option A: Using Git Command Line

```bash
cd ~/Projects/Python/TelegramBot/Kvartira

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Kvartira Telegram bot"

# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/kvartira-bot.git
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Desktop (Easier)

1. Download GitHub Desktop: https://desktop.github.com/
2. Sign in to your GitHub account
3. Click "Add" → "Add Existing Repository"
4. Select the `Kvartira` folder
5. Click "Publish repository"
6. Uncheck "Keep this code private" (or keep it private, your choice)
7. Click "Publish repository"

---

## 🚂 **Step 3: Deploy to Railway**

### 1️⃣ **Sign Up**

1. Go to https://railway.app
2. Click **"Login"** or **"Start a New Project"**
3. Sign in with **GitHub** (easiest)
4. You'll get **$5 free credit** (good for ~1 month)

### 2️⃣ **Create New Project**

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Connect your GitHub account (if not already)
4. Select your `kvartira-bot` repository

### 3️⃣ **Configure Environment Variables**

Railway will start building, but you need to add your bot token:

1. In your Railway project, click **"Variables"** tab
2. Click **"New Variable"**
3. Add:
   - **Key:** `BOT_TOKEN`
   - **Value:** `8569912959:AAETePcMQ4KTmAjCS9N2h4a9X2BOwMjw-oI`
4. Click **"Add"**

### 4️⃣ **Deploy**

Railway will automatically:
- ✅ Detect it's a Python project
- ✅ Install dependencies from `requirements.txt`
- ✅ Run the command from `Procfile`

**Your bot will start automatically!** 🎉

---

## 📊 **Step 4: Monitor Your Bot**

### View Logs:
1. Go to your Railway project
2. Click on your service
3. Click **"Deployments"** → Latest deployment
4. Click **"View Logs"**

You should see:
```
Boshlang'ich tozalash tugatildi
Bot ishga tushdi...
Application started
```

### Check Status:
- Green dot = Running ✅
- Red dot = Error ❌

---

## 🔄 **Step 5: Auto-Deploy Updates**

Every time you push to GitHub, Railway will automatically redeploy!

```bash
# Make changes to your code
git add .
git commit -m "Updated bot features"
git push

# Railway will automatically deploy! 🚀
```

---

## 💰 **Pricing & Free Trial**

### Free Trial:
- ✅ $5 credit for new users
- ✅ Good for ~1 month
- ✅ No credit card needed initially

### After Trial:
- 💳 $5/month minimum (Hobby plan)
- 💰 Pay-as-you-go for usage
- 📊 Includes 500 hours of compute

### Your Bot Usage:
- Your bot will use ~730 hours/month (24/7)
- Cost: ~$5-7/month

---

## 🐛 **Troubleshooting**

### Bot not starting?

**Check logs for errors:**
1. Railway dashboard → Your service → Logs

**Common issues:**

#### 1. Missing BOT_TOKEN
```
ValueError: BOT_TOKEN not found
```
**Fix:** Add `BOT_TOKEN` in Variables tab

#### 2. Build failed
```
Error: Could not install requirements
```
**Fix:** Check `requirements.txt` is correct

#### 3. Database errors
```
Error: Unable to open database
```
**Fix:** Railway provides ephemeral storage. For persistent database, you need to add Railway's PostgreSQL (but SQLite works fine for restarts)

---

## 🔧 **Advanced: Persistent Database**

Railway's disk is ephemeral (resets on restart). For persistent data:

### Option 1: Keep SQLite (Simple)
- Your database will reset on each deploy
- Good for testing

### Option 2: Use Railway PostgreSQL (Production)
1. Click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway will create a database
3. Update your bot to use PostgreSQL instead of SQLite
   (This requires code changes - let me know if you need help)

### Option 3: Use Railway Volume (Persistent SQLite)
1. In your service settings
2. Add a volume mount
3. Store database in the volume path

---

## 📱 **Test Your Bot**

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Bot should respond in Uzbek! 🎉

---

## ✅ **Success Checklist**

- ✅ Code pushed to GitHub
- ✅ Railway project created
- ✅ BOT_TOKEN environment variable set
- ✅ Bot deployed and running (green status)
- ✅ Logs show "Bot ishga tushdi..."
- ✅ Bot responds in Telegram

---

## 🆘 **Need Help?**

**Railway Issues:**
- Railway Docs: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway

**Bot Issues:**
- Check logs in Railway dashboard
- Common fix: Restart deployment

---

## 🎉 **You're Done!**

Your bot is now:
- ✅ Running 24/7 on Railway
- ✅ Auto-deploys on git push
- ✅ Monitored and managed
- ✅ Scalable and reliable

**Enjoy your deployed bot!** 🚀

---

## 💡 **Pro Tips**

1. **Free Alternative:** If $5/month is too much, use PythonAnywhere (free) or Oracle Cloud (always free VPS)

2. **Monitor Usage:** Check Railway dashboard to see your monthly costs

3. **Backup Your Database:** Periodically download `apartment_bot.db` from your local testing

4. **Security:** Never commit `.env` to git (it's in `.gitignore`)

5. **Updates:** Push to GitHub = Auto deploy to Railway!
