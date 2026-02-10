# Update Guide - Expense Reason & Group Notifications

## What's New

✅ **Expense Reason**: Users now enter what they bought after entering the amount
✅ **Group Notifications**: All expenses are automatically sent to a connected group chat
✅ **Formatted Messages**: Beautiful formatted messages showing expense details

## 1. BotFather Settings (REQUIRED)

You MUST update your bot settings in BotFather to allow it to work in groups:

1. Open Telegram and find **@BotFather**
2. Send `/mybots`
3. Select your bot: **HisobchiBot** (or your bot name)
4. Click **Bot Settings**
5. Click **Allow Groups?** → Choose **Turn groups on**
6. (Optional but recommended) Click **Group Privacy** → Choose **Turn off**
   - This allows the bot to read all messages in the group
   - Needed for the `/connect_group` command to work

## 2. Deploy to Railway

Since you've already set up Railway with GitHub, just push your changes:

```bash
# Make sure you're in the Kvartira directory
cd /home/nooriddin/Projects/Python/TelegramBot/Kvartira

# Add all changes
git add .

# Commit with a descriptive message
git commit -m "Add expense reason and group notifications feature"

# Push to GitHub (Railway will auto-deploy)
git push origin main
```

Railway will automatically:
- Detect the push
- Run database migrations (new columns will be added automatically)
- Restart your bot with the new code

## 3. Create New Home (Fresh Start)

After deployment, the database is fresh so you'll need to:

1. Send `/start` to the bot
2. Enter your name
3. Select "Uy yaratish" (Create home)
4. Enter home name and password
5. **Bot will ask you to connect a group:**
   - Create a Telegram group (or use existing)
   - Add the bot to the group
   - Send any message in the group (e.g., "test")
   - Bot automatically connects and confirms!
6. Done! Share home name + password with roommates

## 4. How It Works Now

### New Home Creation Flow:

1. Admin creates home name + password
2. Bot says: "Add me to your group and send any message there"
3. Admin adds bot to group
4. Admin sends any message in the group (e.g., "test")
   - **For groups with topics/forums:** Send the message in the specific topic where you want expense notifications
   - Bot will remember the topic and always post there!
5. Bot automatically connects the group ✅
6. Setup complete!

### New Expense Flow:

1. User enters amount: `15000`
2. Bot asks: "Nima uchun sarflandi?"
3. User enters reason:
   ```
   Tovuq
   Olma
   Sabzi
   ```
   (can be one line or multiple lines)
4. Bot asks: "Kim iste'mol qiladi?"
5. User selects: `1 2` or `0` for all
6. Bot saves expense and sends message to GROUP:

```
Harajat: 15,000

Sabab:

Tovuq
Olma
Sabzi

Iste'molchilar:

1. Jack
2. Mole

Har biriga: 7,500
```

If all members selected, shows "Barcha uy a'zolari" instead of numbered list.

### Topics/Forums Support:

**For groups with topics enabled:**
- Whichever topic the admin sends the initial connection message in, that's where all future expense notifications will be posted
- This keeps expenses organized in a dedicated topic
- Example: Create a "💰 Harajatlar" (Expenses) topic and connect the bot there

## Deployment Commands (Quick Reference)

```bash
# Check current status
git status

# Push changes
git add .
git commit -m "Your message here"
git push origin main

# Check Railway deployment
# Visit: https://railway.app/dashboard
```

## Troubleshooting

### Bot not sending to group?
- Make sure you completed group connection during home creation
- Check that bot is still a member of the group
- Verify "Allow Groups" is enabled in BotFather
- If group was disconnected: Admin can create a new home and reconnect

### Database errors?
- The migrations run automatically
- Old data will not be affected
- New transactions will have the `reason` field

### Bot not responding?
- Check Railway logs for errors
- Verify BOT_TOKEN is correct in Railway environment variables
