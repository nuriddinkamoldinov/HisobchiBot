# Example Scenarios

This document provides real-world examples of how to use the Apartment Expense Bot.

## Scenario 1: Week 1 - Setting Up

### Monday - Creating the Home

**Jack (Admin):**
1. Sends `/start` to the bot
2. Enters name: "Jack"
3. Chooses "Create Home"
4. Home name: "Apartment 8A"
5. Password: "roommates2026"
6. Shares credentials with roommates

**Other Members Join:**
- **Mole:** Uses the same credentials to join
- **Alex:** Uses the same credentials to join
- **Bond:** Uses the same credentials to join
- **James:** Uses the same credentials to join

Result: 5 people in "Apartment 8A"

---

## Scenario 2: Daily Expenses

### Tuesday - Grocery Shopping

**Jack goes shopping:**
- Buys vegetables, meat, rice: 85,000 sum
- Everyone will eat except Bond (he's vegetarian and bought separately)

**Jack's actions:**
1. Opens bot menu
2. Taps "Add Expense"
3. Enters: `85000`
4. Bot shows member list
5. Jack enters: `1 2 3 5` (Jack, Mole, Alex, James - not Bond)
6. Cost per person: 21,250 sum

**Result:** Mole, Alex, and James each owe Jack 21,250 sum

---

### Wednesday - Internet Bill

**Mole pays the internet:**
- Monthly bill: 150,000 sum
- Everyone uses it

**Mole's actions:**
1. Add Expense
2. Enters: `150 000` (with space - bot accepts this)
3. Selects: `1 2 3 4 5` (everyone)
4. Cost per person: 30,000 sum

**Result:** Each person owes Mole 30,000 sum

---

### Thursday - Pizza Night

**Alex orders pizza:**
- Pizza for 3 people: 45,000 sum
- Only Alex, Jack, and James eating

**Alex's actions:**
1. Add Expense
2. Enters: `45000`
3. Selects: `1 3 5` (Jack, Alex, James)
4. Cost per person: 15,000 sum

**Result:** Jack and James each owe Alex 15,000 sum

---

### Friday - Cleaning Supplies

**Bond buys cleaning supplies:**
- Detergent, mop, etc: 35,000 sum
- Shared by everyone

**Bond's actions:**
1. Add Expense
2. Enters: `35000`
3. Selects: `1 2 3 4 5` (everyone)
4. Cost per person: 7,000 sum

**Result:** Each person owes Bond 7,000 sum

---

### Saturday - Breakfast Items

**James buys breakfast:**
- Bread, eggs, milk: 28,000 sum
- Bond doesn't eat breakfast with the group

**James's actions:**
1. Add Expense
2. Enters: `28000`
3. Selects: `1 2 3 5` (Jack, Mole, Alex, James)
4. Cost per person: 7,000 sum

**Result:** Jack, Mole, and Alex each owe James 7,000 sum

---

## Scenario 3: Weekly Settlement

### Sunday - Calculating Who Pays Whom

**Jack (Admin) runs calculations:**
1. Taps "Get Calculations (Refresh)"
2. Bot sends the following to each person:

---

#### Jack Receives:
```
📊 Week 6 Settlement
==============================

💰 You receive money from:
  • Mole: 21,250 sum
  • Alex: 6,250 sum
  • James: 21,250 sum

💸 You give money to:
  (none)
```

**Explanation:** Jack paid 85,000 for groceries that 4 people shared. He gets back his share from the other 3.

---

#### Mole Receives:
```
📊 Week 6 Settlement
==============================

💰 You receive money from:
  • Jack: 8,750 sum
  • Alex: 15,000 sum
  • Bond: 23,000 sum
  • James: 23,000 sum

💸 You give money to:
  (none)
```

**Explanation:** Mole paid the big internet bill (150,000) that everyone shared.

---

#### Alex Receives:
```
📊 Week 6 Settlement
==============================

💰 You receive money from:
  • Jack: 15,000 sum
  • James: 15,000 sum

💸 You give money to:
  • Mole: 15,000 sum
  • Jack: 6,250 sum
  • Bond: 7,000 sum
```

**Explanation:** Alex paid for pizza but also consumed from other purchases.

---

#### Bond Receives:
```
📊 Week 6 Settlement
==============================

💰 You receive money from:
  • Jack: 7,000 sum
  • Alex: 7,000 sum
  • James: 7,000 sum

💸 You give money to:
  • Mole: 23,000 sum
```

**Explanation:** Bond paid for cleaning supplies but didn't share in groceries or breakfast.

---

#### James Receives:
```
📊 Week 6 Settlement
==============================

💰 You receive money from:
  • Jack: 7,000 sum
  • Mole: 7,000 sum
  • Alex: 8,000 sum

💸 You give money to:
  • Jack: 21,250 sum
  • Mole: 23,000 sum
```

**Explanation:** James paid for breakfast items but consumed from multiple other purchases.

---

## Scenario 4: Transaction Optimization Example

### Before Optimization:
- Jack owes Mole: 15,000 sum
- Mole owes Jack: 12,000 sum

### After Optimization (What the bot shows):
- Jack pays Mole: 3,000 sum (net balance)

This minimizes the number of transactions and the amount of cash that needs to change hands.

---

## Scenario 5: Mid-Week Check

### Wednesday - Checking Status Without Clearing

**Alex wants to know where they stand:**
1. Taps "Get Calculations" (without refresh)
2. Sees current balance
3. Transactions are NOT cleared
4. Can continue adding expenses

This is useful for checking your status mid-week without affecting the ongoing tracking.

---

## Scenario 6: Managing Members

### New Roommate Moves In

**Jack (Admin):**
1. Tells new roommate Sarah to:
   - Open the bot
   - Send `/start`
   - Enter her name
   - Choose "Join Home"
   - Enter: "Apartment 8A"
   - Enter password: "roommates2026"

Sarah is now part of the home and can add expenses.

---

### Someone Moves Out

**Bond is moving out:**

**Jack (Admin):**
1. First settles all pending amounts with Bond
2. Taps "Manage Home"
3. Taps "Delete Member"
4. Selects Bond's number
5. Bond receives notification that he was removed

Bond can no longer access the home's expenses.

---

## Scenario 7: Changing Credentials

### Security Update

**Jack notices the password was shared too widely:**

**Jack (Admin):**
1. Taps "Manage Home"
2. Taps "Edit Password"
3. Enters new password: "newpass2026"
4. Informs all current members of new password

New joiners will need the new password.

---

## Tips from Real Usage

1. **End-of-day routine:** Add all your expenses for the day in one session
2. **Save receipts:** Keep photos of receipts until settlement is done
3. **Weekly rhythm:** Settle up every Sunday evening
4. **Communication:** Use a Telegram group to discuss large purchases before making them
5. **Fair sharing:** Be honest about consumption - the system only works with trust

---

## Common Patterns

### Pattern 1: Recurring Bills
```
Internet (monthly): One person pays, everyone splits
Cleaning service: One person pays, everyone splits
```

### Pattern 2: Personal Groceries
```
If someone buys something only they eat:
- Add expense
- Select only themselves
- No one else owes anything
```

### Pattern 3: Group Meals
```
Dinner for 3 people:
- Whoever pays adds the expense
- Selects only those who ate
- Equal split among participants
```

---

## Troubleshooting Examples

### Problem: "I entered the wrong amount"
**Solution:** Unfortunately, you can't edit. Ask admin to note the correction when doing settlement.

### Problem: "I forgot to add an expense"
**Solution:** Add it before the weekly refresh. After refresh, it goes to next week.

### Problem: "The settlement seems wrong"
**Solution:** 
1. Check if all expenses were entered correctly
2. Remember the bot optimizes (shows net balance)
3. Ask admin to show calculations before refresh

---

## Best Practices

1. **Add expenses immediately** - Don't wait days to enter them
2. **Be specific** - If unclear who consumed, ask in group chat first
3. **Round numbers** - Use whole numbers, easier to split
4. **Weekly rhythm** - Pick a consistent day for settlement
5. **Communicate** - Discuss any disagreements openly before settling
