# 🚀 Railway Quick Start - Copy & Paste Commands

## Step 1: Initialize Git Repository

```bash
cd ~/Projects/Python/TelegramBot/Kvartira

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Kvartira Telegram Bot"
```

---

## Step 2: Create GitHub Repository

### Option A: Using GitHub CLI (if installed)
```bash
gh repo create kvartira-bot --public --source=. --remote=origin --push
```

### Option B: Manual (Most Common)

1. Go to https://github.com/new
2. Repository name: `kvartira-bot`
3. Keep it **Public** (or Private, your choice)
4. **Don't** initialize with README (your code already has files)
5. Click **"Create repository"**
6. Copy the commands GitHub shows, or use:

```bash
git remote add origin https://github.com/YOUR_USERNAME/kvartira-bot.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 3: Deploy to Railway

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**
4. Authorize GitHub (if first time)
5. Select **"kvartira-bot"** repository
6. Railway starts deploying automatically!

---

## Step 4: Add Environment Variable

**IMPORTANT:** Your bot won't work until you add the token!

1. In Railway dashboard, click your service
2. Click **"Variables"** tab
3. Click **"+ New Variable"**
4. Add:
   ```
   BOT_TOKEN=8569912959:AAETePcMQ4KTmAjCS9N2h4a9X2BOwMjw-oI
   ```
5. Railway will automatically redeploy

---

## Step 5: Check Status

1. Click **"Deployments"** tab
2. Click latest deployment
3. Click **"View Logs"**

Look for:
```
✅ Boshlang'ich tozalash tugatildi
✅ Bot ishga tushdi...
✅ Application started
```

---

## Step 6: Test!

Open Telegram → Your bot → Send `/start`

**Should respond in Uzbek!** 🎉

---

## Future Updates

Whenever you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Railway auto-deploys! 🚀

---

## Total Time: ~10 minutes ⏱️

That's it! Your bot is now running 24/7 on Railway!
