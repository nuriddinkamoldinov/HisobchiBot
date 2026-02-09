"""
Test script for expense splitting algorithm
"""
from collections import defaultdict

def calculate_settlements(transactions, members):
    """
    Calculate optimized settlements using net balance method
    Returns list of (from_user, to_user, amount) tuples
    """
    # Calculate net balance for each member
    balances = defaultdict(float)
    member_dict = {m[0]: m[1] for m in members}

    print("\n=== Processing Transactions ===")
    for trans_id, payer_id, amount, consumers_str in transactions:
        consumer_ids = [int(x) for x in consumers_str.split(',')]
        share = amount / len(consumer_ids)

        print(f"\nTransaction {trans_id}:")
        print(f"  Payer: {member_dict[payer_id]} (ID: {payer_id}) paid {amount}")
        print(f"  Consumers: {[member_dict[cid] for cid in consumer_ids]}")
        print(f"  Share per person: {share:.2f}")

        # Payer paid the full amount
        balances[payer_id] += amount

        # Each consumer owes their share
        for consumer_id in consumer_ids:
            balances[consumer_id] -= share

    print("\n=== Net Balances ===")
    for uid, bal in balances.items():
        print(f"{member_dict[uid]}: {bal:+.2f}")

    # Separate creditors and debtors
    creditors = [(uid, bal) for uid, bal in balances.items() if bal > 0.01]
    debtors = [(uid, -bal) for uid, bal in balances.items() if bal < -0.01]

    # Sort by amount
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    print(f"\nCreditors: {[(member_dict[uid], bal) for uid, bal in creditors]}")
    print(f"Debtors: {[(member_dict[uid], bal) for uid, bal in debtors]}")

    # Calculate settlements
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

    return settlements, member_dict

# Test case 1: Simple split
print("="*50)
print("TEST 1: Alice pays 90 for Alice, Bob, Charlie")
print("="*50)

members = [(1, "Alice"), (2, "Bob"), (3, "Charlie")]
transactions = [
    (1, 1, 90, "1,2,3")  # Alice pays 90 for all three
]

settlements, member_dict = calculate_settlements(transactions, members)
print("\n=== Settlements ===")
for from_id, to_id, amount in settlements:
    print(f"{member_dict[from_id]} pays {member_dict[to_id]}: {amount:.2f}")

# Test case 2: Multiple transactions
print("\n" + "="*50)
print("TEST 2: Alice pays 90 for all, Bob pays 60 for Alice & Bob")
print("="*50)

transactions = [
    (1, 1, 90, "1,2,3"),  # Alice pays 90 for all three
    (2, 2, 60, "1,2")     # Bob pays 60 for Alice and Bob
]

settlements, member_dict = calculate_settlements(transactions, members)
print("\n=== Settlements ===")
for from_id, to_id, amount in settlements:
    print(f"{member_dict[from_id]} pays {member_dict[to_id]}: {amount:.2f}")

# Test case 3: Payer not in consumers
print("\n" + "="*50)
print("TEST 3: Alice pays 100 for Bob & Charlie only")
print("="*50)

transactions = [
    (1, 1, 100, "2,3")  # Alice pays 100 for Bob and Charlie
]

settlements, member_dict = calculate_settlements(transactions, members)
print("\n=== Settlements ===")
for from_id, to_id, amount in settlements:
    print(f"{member_dict[from_id]} pays {member_dict[to_id]}: {amount:.2f}")
