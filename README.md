# Apartment Expense Management Telegram Bot

A Telegram bot for managing shared expenses among roommates with automatic settlement calculations and transaction optimization.

## Features

### 🏠 Home Management
- Create or join shared apartments ("homes")
- Password-protected homes
- Admin and member roles
- Manage members (add/remove)

### 💰 Expense Tracking
- Easy expense entry with flexible number formats (14000 or 14 000)
- Select who consumed each product
- Automatic cost splitting
- Weekly transaction tracking

### 📊 Smart Settlements
- Optimized settlement calculations
- Minimizes number of transactions
- Net balance method (if Jack owes Mole 15,000 and Mole owes Jack 12,000, Jack only pays 3,000)
- Automatic weekly summaries

### 👥 Role-Based Access
**Home Admin (Creator):**
- Manage Home (edit name/password, delete members)
- Get Calculations with refresh (clears weekly data)
- Get Calculations without refresh
- Add expenses
- Quit home

**Home Members:**
- Get Calculations (view only)
- Add expenses
- Quit home

## Installation

### Prerequisites
- Python 3.8 or higher
- A Telegram account
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Setup Steps

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create your Telegram bot:**
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` command
   - Follow the instructions to choose a name and username
   - Copy the bot token you receive

4. **Configure the bot:**
   - Open `apartment_expense_bot.py`
   - Find the line `TOKEN = "YOUR_BOT_TOKEN_HERE"`
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token

5. **Run the bot:**
```bash
python apartment_expense_bot.py
```

## Usage Guide

### First Time Setup

1. **Start the bot:**
   - Open your bot in Telegram
   - Send `/start`
   - Enter your name when prompted

2. **Create a Home (Admin):**
   - Choose "Create Home"
   - Enter a home name (e.g., "Apartment 8A")
   - Set a password
   - Share the home name and password with your roommates

3. **Join a Home (Member):**
   - Choose "Join Home"
   - Enter the home name provided by your admin
   - Enter the password

### Daily Operations

#### Adding an Expense

1. From the main menu, tap **"Add Expense"**
2. Enter the amount you spent (e.g., `14000` or `14 000`)
3. Select who consumed the product by entering numbers:
   ```
   Whose going to consume it:
   1. Jack
   2. Mole
   3. Alex
   4. Bond
   5. James
   
   Enter: 1 3 5
   ```
   (This splits the cost between Jack, Alex, and James)

#### Viewing Settlements

**Get Calculations (no refresh):**
- View current week's settlement without clearing data
- Useful for checking status mid-week

**Get Calculations (Refresh)** - Admin only:
- Sends settlement summary to all members
- Clears the week's transactions
- Use this at the end of the week after everyone has paid

Example settlement message:
```
📊 Week 6 Settlement
==============================

💰 You receive money from:
  • Jack: 45,000 sum
  • Mole: 12,000 sum

💸 You give money to:
  • Bond: 28,000 sum
```

### Admin Functions

#### Manage Home
1. Tap **"Manage Home"**
2. Choose from:
   - **Edit Home Name:** Change the home name
   - **Edit Password:** Change the home password
   - **Delete Member:** Remove a member from the home

#### Example Scenarios

**Scenario 1: Grocery Shopping**
- Jack spends 45,000 on groceries
- Everyone except Bond will eat them
- Jack adds expense: 45,000
- Selects: 1 2 3 5 (everyone except Bond)
- Each of the 4 people owes Jack: 11,250

**Scenario 2: Pizza Night**
- Mole orders pizza for 28,000
- Only Mole, Jack, and Alex eat it
- Mole adds expense: 28,000
- Selects: 1 2 3
- Each person owes Mole: 9,333

**Scenario 3: End of Week Settlement**
After a week of transactions:
- Jack paid: 45,000 (4 people consumed)
- Mole paid: 28,000 (3 people consumed)
- Alex paid: 30,000 (5 people consumed)

The bot automatically calculates:
- Who owes whom
- Optimizes payments (minimizes transactions)
- Sends summary to everyone

## Database Structure

The bot uses SQLite with three tables:

**users**: Stores user information and home membership
**homes**: Stores home details and credentials
**transactions**: Stores all expenses with week number for periodic clearing

## Commands Reference

- `/start` - Initialize bot or create/join home
- `/menu` - Access main menu
- `/cancel` - Cancel current operation

## Tips

1. **Weekly Routine:**
   - Members add expenses throughout the week
   - Admin refreshes calculations at week's end
   - Everyone settles up based on the summary

2. **Number Format:**
   - Both `14000` and `14 000` are accepted
   - The bot automatically removes spaces

3. **Transaction Optimization:**
   - If you owe Jack 15,000 and Jack owes you 12,000
   - You only pay Jack 3,000 (net balance)

4. **Privacy:**
   - Each home is password-protected
   - Only home members see transactions
   - Settlements are sent privately to each member

## Troubleshooting

**Bot doesn't respond:**
- Check if the bot is running (`python apartment_expense_bot.py`)
- Verify your token is correct in the code

**Can't join home:**
- Double-check the home name (case-sensitive)
- Verify the password with the admin

**Calculations seem wrong:**
- Ensure all expenses are entered correctly
- Check that the right people are selected for each expense
- Remember: calculations show NET balance (optimized)

## Security Notes

- Keep your bot token secret
- Use strong passwords for homes
- Only share credentials with trusted roommates
- The database file contains all transaction data

## Future Enhancements

Possible improvements:
- Export transaction history to Excel
- Monthly reports
- Category tagging for expenses
- Support for multiple currencies
- Recurring expense handling
- Photo receipts storage

## Support

For issues or questions:
1. Check this README
2. Review the error messages
3. Ensure all dependencies are installed
4. Verify your bot token is correct

## License

This project is provided as-is for personal use.

---

**Happy expense tracking! 💰🏠**
