"""
Test edge cases for expense splitting algorithm
"""
from collections import defaultdict

def calculate_settlements(transactions, members):
    """Calculate optimized settlements using net balance method"""
    balances = defaultdict(float)
    member_dict = {m[0]: m[1] for m in members}

    for trans_id, payer_id, amount, consumers_str in transactions:
        consumer_ids = [int(x) for x in consumers_str.split(',')]
        share = amount / len(consumer_ids)
        balances[payer_id] += amount
        for consumer_id in consumer_ids:
            balances[consumer_id] -= share

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

    return settlements, member_dict, balances

# Edge Case 1: Payer is NOT a consumer
print("="*60)
print("EDGE CASE 1: Payer pays but doesn't consume")
print("Nuriddin pays 100 for Muxammadamin & Muhammadqodir only")
print("="*60)

members = [(1, "Muxammadamin"), (2, "Muhammadqodir"), (3, "Nuriddin"), (4, "Abduxalim")]
transactions = [
    (1, 3, 100, "1,2")  # Nuriddin pays 100, but only Muxammadamin and Muhammadqodir consume
]

settlements, member_dict, balances = calculate_settlements(transactions, members)
print("\nBalances:")
for uid, bal in balances.items():
    print(f"  {member_dict[uid]}: {bal:+.2f}")
print("\nExpected: Nuriddin +100, Muxammadamin -50, Muhammadqodir -50, Abduxalim 0")
print("\nSettlements:")
for from_id, to_id, amount in settlements:
    print(f"  {member_dict[from_id]} pays {member_dict[to_id]}: {amount:.2f}")

# Edge Case 2: Everyone pays equal amounts for everyone
print("\n" + "="*60)
print("EDGE CASE 2: Everyone pays 100 for all 4 people")
print("="*60)

transactions = [
    (1, 1, 100, "1,2,3,4"),  # Muxammadamin pays 100
    (2, 2, 100, "1,2,3,4"),  # Muhammadqodir pays 100
    (3, 3, 100, "1,2,3,4"),  # Nuriddin pays 100
    (4, 4, 100, "1,2,3,4"),  # Abduxalim pays 100
]

settlements, member_dict, balances = calculate_settlements(transactions, members)
print("\nBalances:")
for uid, bal in balances.items():
    print(f"  {member_dict[uid]}: {bal:+.2f}")
print("\nExpected: Everyone should have 0 balance")
print("\nSettlements:")
if not settlements:
    print("  No settlements needed - everyone is even!")
for from_id, to_id, amount in settlements:
    print(f"  {member_dict[from_id]} pays {member_dict[to_id]}: {amount:.2f}")

# Edge Case 3: Complex scenario
print("\n" + "="*60)
print("EDGE CASE 3: Complex real-world scenario")
print("Muxammadamin pays 50 for himself and Muhammadqodir")
print("Nuriddin pays 120 for all 4")
print("Abduxalim pays 80 for Nuriddin and himself")
print("="*60)

transactions = [
    (1, 1, 50, "1,2"),      # Muxammadamin: 50 for 2 people
    (2, 3, 120, "1,2,3,4"), # Nuriddin: 120 for 4 people
    (3, 4, 80, "3,4"),      # Abduxalim: 80 for 2 people
]

settlements, member_dict, balances = calculate_settlements(transactions, members)
print("\nBalances:")
total = 0
for uid, bal in balances.items():
    print(f"  {member_dict[uid]}: {bal:+.2f}")
    total += bal
print(f"\nTotal balance (should be ~0): {total:.2f}")

print("\nSettlements:")
for from_id, to_id, amount in settlements:
    print(f"  {member_dict[from_id]} pays {member_dict[to_id]}: {amount:.2f}")

# Manual verification:
print("\n--- Manual Verification ---")
print("Total paid: 50 + 120 + 80 = 250")
print("Each person's share: 250 / 4 = 62.5")
print("Muxammadamin: paid 50, owes 62.5, balance = 50 - 62.5 = -12.5")
print("Muhammadqodir: paid 0, owes 62.5, balance = 0 - 62.5 = -62.5")
print("Nuriddin: paid 120, owes 62.5, balance = 120 - 62.5 = +57.5")
print("Abduxalim: paid 80, owes 62.5, balance = 80 - 62.5 = +17.5")

# Wait, this is wrong! Let me recalculate based on who consumed what...
print("\n--- Corrected Manual Verification ---")
print("Muxammadamin consumed in: [Trans1: 25, Trans2: 30] = 55, paid: 50, balance = 50-55 = -5")
print("Muhammadqodir consumed in: [Trans1: 25, Trans2: 30] = 55, paid: 0, balance = 0-55 = -55")
print("Nuriddin consumed in: [Trans2: 30, Trans3: 40] = 70, paid: 120, balance = 120-70 = +50")
print("Abduxalim consumed in: [Trans2: 30, Trans3: 40] = 70, paid: 80, balance = 80-70 = +10")
