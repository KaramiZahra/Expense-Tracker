import uuid
from datetime import datetime

transactions = []


def save_transactions():
    pass


def add_transaction():

    while True:
        transaction_type = input(
            "Enter transaction type 1)Income 2)Expense: ").strip()
        if transaction_type == "1":
            transaction_type = "Income"
            break
        elif transaction_type == "2":
            transaction_type = "Expense"
            break
        else:
            print("Invalid type.")

    transaction_category = input(
        "Enter transaction category: ").strip().capitalize()

    while True:
        try:
            transaction_amount = float(
                input("Enter transaction amount: ").strip())
            break
        except ValueError:
            print("Invalid amount. Enter a number.")

    while True:
        date_input = input("Enter transaction date(YYYY-MM-DD): ").strip()
        try:
            transaction_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")

    transaction_note = input("Enter transaction note: ").strip()

    new_transaction = {
        'id': str(uuid.uuid4()),
        'type': transaction_type,
        'category': transaction_category,
        'amount': transaction_amount,
        'date': transaction_date,
        'note': transaction_note
    }
    transactions.append(new_transaction)

    print(transactions)


def menu():
    print("\n---Expense Tracker---\n")
    print("1.Add a transaction")
    print("2.Save and exit")

    user_input = input("Choose an option: ")

    if user_input == '1':
        add_transaction()
    elif user_input == '2':
        save_transactions()
    else:
        print("Invalid input.")


menu()
