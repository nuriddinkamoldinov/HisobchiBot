# Quick Start Guide

## 5-Minute Setup

### Step 1: Get Your Bot Token (2 minutes)
1. Open Telegram
2. Search for `@BotFather`
3. Send: `/newbot`
4. Choose a name: "My Apartment Bot" (or any name)
5. Choose a username: "myapartment_bot" (must end with 'bot')
6. Copy the token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Step 2: Install the Bot (2 minutes)

**Option A: Automatic Setup (Linux/Mac)**
```bash
chmod +x setup.sh
./setup.sh
```

**Option B: Automatic Setup (Windows)**
```cmd
setup.bat
```

**Option C: Manual Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Edit apartment_expense_bot.py
# Replace YOUR_BOT_TOKEN_HERE with your actual token

# Run the bot
python apartment_expense_bot.py
```

### Step 3: Start Using (1 minute)
1. Open your bot in Telegram
2. Send: `/start`
3. Enter your name
4. Create or join a home
5. Done! 🎉

---

## First Day Usage

### As Home Creator (Admin):

**Morning - Create Home:**
```
You: /start
Bot: Welcome! Enter your name:
You: Jack
Bot: Create Home or Join Home?
You: Create Home
Bot: Enter home name:
You: Apartment 8A
Bot: Enter password:
You: roomies2026
Bot: ✅ Home created! Share with roommates.
```

**Share with Roommates:**
Send them:
- Home name: `Apartment 8A`
- Password: `roomies2026`
- Bot link: `@your_bot_username`

**Evening - Add First Expense:**
```
You: /menu
You: [Tap "Add Expense"]
Bot: Enter amount:
You: 25000
Bot: Who consumed it?
    1. Jack
    2. Mole
    3. Alex
You: 1 2 3
Bot: ✅ Expense recorded! Each pays: 8,333 sum
```

---

### As Member:

**Join Home:**
```
You: /start
Bot: Enter your name:
You: Mole
Bot: Create Home or Join Home?
You: Join Home
Bot: Enter home name:
You: Apartment 8A
Bot: Enter password:
You: roomies2026
Bot: ✅ Successfully joined!
```

**Add Expense:**
```
You: /menu
You: [Tap "Add Expense"]
Bot: Enter amount:
You: 15 000
Bot: Who consumed it?
    1. Jack
    2. Mole
You: 2
Bot: ✅ Expense recorded!
```

---

## Weekly Routine

### Throughout the Week:
Everyone adds their expenses as they make purchases.

### Sunday Evening:
Admin runs "Get Calculations (Refresh)"

### Example Output:
```
📊 Week 6 Settlement
==============================

💰 You receive money from:
  • Jack: 15,000 sum
  • Mole: 8,000 sum

💸 You give money to:
  • Bond: 12,000 sum
```

### Settle Up:
Transfer money via cash or bank transfer according to the settlement.

---

## Common Commands

- `/start` - Initial setup or reset
- `/menu` - Main menu
- `/cancel` - Cancel current operation

---

## Quick Tips

✅ **DO:**
- Add expenses right after purchase
- Select only people who consumed
- Run weekly settlements
- Use clear home names

❌ **DON'T:**
- Forget to add expenses
- Select wrong consumers
- Wait too long to settle
- Share passwords publicly

---

## Troubleshooting

**Bot not responding?**
- Check if `python apartment_expense_bot.py` is running
- Verify bot token is correct

**Can't join home?**
- Check home name spelling (case-sensitive)
- Verify password with admin

**Calculations look wrong?**
- Bot shows optimized amounts (net balance)
- Check all expenses were entered correctly

---

## Need Help?

1. Read the full [README.md](README.md)
2. Check [EXAMPLES.md](EXAMPLES.md) for detailed scenarios
3. Review error messages carefully
4. Ensure all roommates understand how to use the bot

---

## Next Steps

Once you're comfortable with basic usage:
- Explore admin features (Manage Home)
- Try checking calculations mid-week
- Establish a weekly settlement routine
- Customize home name and password

**Happy expense tracking! 💰**
