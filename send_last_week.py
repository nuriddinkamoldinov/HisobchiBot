"""
One-off script: send week 13 (last week) calculations to all members and clear data.
Run once from the project directory: python3 send_last_week.py
"""
import sqlite3
import asyncio
from collections import defaultdict
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEEK_NUMBER = 18  # Last week's ISO week number


def get_home_members(home_id):
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('SELECT user_id, name, is_admin FROM users WHERE home_id = ?', (home_id,))
    members = c.fetchall()
    conn.close()
    return members


def get_week_transactions(home_id, week_number):
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('''SELECT transaction_id, payer_id, amount, consumers
                 FROM transactions
                 WHERE home_id = ? AND week_number = ?''',
              (home_id, week_number))
    transactions = c.fetchall()
    conn.close()
    return transactions


def get_egg_debts_for_week(home_id, week_number):
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('''SELECT debtor_id, creditor_id, SUM(amount)
                 FROM egg_debts
                 WHERE home_id = ? AND week_number = ?
                 GROUP BY debtor_id, creditor_id''',
              (home_id, week_number))
    result = c.fetchall()
    conn.close()
    return result


def get_bank_card(user_id):
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('SELECT bank_card FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] else None


def calculate_settlements(transactions, members, egg_debts=None):
    balances = defaultdict(float)
    member_dict = {m[0]: m[1] for m in members}

    for trans_id, payer_id, amount, consumers_str in transactions:
        consumer_ids = [int(x) for x in consumers_str.split(',')]
        share = amount / len(consumer_ids)
        balances[payer_id] += amount
        for consumer_id in consumer_ids:
            balances[consumer_id] -= share

    if egg_debts:
        for debtor_id, creditor_id, amount in egg_debts:
            balances[debtor_id] -= amount
            balances[creditor_id] += amount

    creditors = [(uid, bal) for uid, bal in balances.items() if bal > 0.01]
    debtors = [(uid, -bal) for uid, bal in balances.items() if bal < -0.01]
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    settlements = []
    i, j = 0, 0
    while i < len(creditors) and j < len(debtors):
        creditor_id, credit = creditors[i]
        debtor_id, debt = debtors[j]
        amount = min(credit, debt)
        settlements.append((debtor_id, creditor_id, amount))
        creditors[i] = (creditor_id, credit - amount)
        debtors[j] = (debtor_id, debt - amount)
        if creditors[i][1] < 0.01:
            i += 1
        if debtors[j][1] < 0.01:
            j += 1

    return settlements


def clear_data(home_id, week_number):
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE home_id = ? AND week_number = ?', (home_id, week_number))
    c.execute('DELETE FROM egg_debts WHERE home_id = ? AND week_number = ?', (home_id, week_number))
    conn.commit()
    conn.close()


async def main():
    from telegram import Bot
    bot = Bot(token=BOT_TOKEN)

    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('SELECT home_id FROM homes')
    home_ids = [row[0] for row in c.fetchall()]
    conn.close()

    for home_id in home_ids:
        transactions = get_week_transactions(home_id, WEEK_NUMBER)
        if not transactions:
            print(f"Home {home_id}: no transactions for week {WEEK_NUMBER}, skipping.")
            continue

        members = get_home_members(home_id)
        if not members:
            continue

        member_dict = {m[0]: m[1] for m in members}
        egg_debts = get_egg_debts_for_week(home_id, WEEK_NUMBER)
        settlements = calculate_settlements(transactions, members, egg_debts)

        for member_id, member_name, is_admin in members:
            receives = [(member_dict[from_id], amount)
                        for from_id, to_id, amount in settlements
                        if to_id == member_id and from_id in member_dict]
            gives = [(to_id, member_dict[to_id], amount)
                     for from_id, to_id, amount in settlements
                     if from_id == member_id and to_id in member_dict]

            message = f"📊 <b>{WEEK_NUMBER}-hafta yakuniy hisob-kitoblari</b>\n"
            message += "=" * 30 + "\n\n"

            if receives:
                message += "💰 <b>Sizga pul beradigan kishilar:</b>\n"
                for name, amount in receives:
                    message += f"  • <b>{name}</b>: {amount:,.0f} so'm\n"
                message += "\n"

            if gives:
                message += "💸 <b>Siz pul beradigan kishilar:</b>\n"
                for to_id, name, amount in gives:
                    card = get_bank_card(to_id)
                    card_str = f"\n    💳 <code>{card}</code>" if card else ""
                    message += f"  • <b>{name}</b>: <b>{amount:,.0f} so'm</b>{card_str}\n"
                message += "\n"

            if not receives and not gives:
                message += "✅ Sizda hech qanday qarz yo'q!\n\n"

            try:
                await bot.send_message(chat_id=member_id, text=message, parse_mode='HTML')
                print(f"  Sent to {member_name} ({member_id})")
            except Exception as e:
                print(f"  Could not send to {member_name} ({member_id}): {e}")

        print(f"Home {home_id}: week {WEEK_NUMBER} done (data kept).")


if __name__ == '__main__':
    asyncio.run(main())
