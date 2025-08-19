import uuid
from datetime import datetime
from pathlib import Path
import csv

EXPENSES_FILE = Path("expenses.csv")
transactions = []


def load_transactions():
    with open(EXPENSES_FILE, "r") as ef:
        reader = csv.DictReader(ef)
        for t in reader:
            prev_transactions = {
                "ID": t["ID"],
                "Type": t["Type"],
                "Category": t["Category"],
                "Amount": float(t["Amount"]),
                "Date": t["Date"],
                "Note": t["Note"]
            }
            transactions.append(prev_transactions)


load_transactions()


def save_transactions():
    with open(EXPENSES_FILE, "w", newline="") as ef:
        field_names = ["ID", "Type", "Category", "Amount", "Date", "Note"]
        writer = csv.DictWriter(ef, fieldnames=field_names)
        writer.writeheader()
        for t in transactions:
            writer.writerow({"ID": t["ID"], "Type": t["Type"], "Category": t["Category"],
                            "Amount": t["Amount"], "Date": t["Date"], "Note": t["Note"]})


def show_transactions():
    if transactions:
        for index, t in enumerate(transactions):
            print(
                f"{index + 1} | {t['Date']} | {t['Type']} | {t['Category']} | {t['Amount']} | {t['Note']}")
    else:
        print("\nYou have no transactions.")


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
        "ID": str(uuid.uuid4()),
        "Type": transaction_type,
        "Category": transaction_category,
        "Amount": transaction_amount,
        "Date": transaction_date,
        "Note": transaction_note
    }
    transactions.append(new_transaction)


def menu():
    while True:
        print("\n---Expense Tracker---\n")
        print("1.Show transactions")
        print("2.Add a transaction")
        print("3.Save and exit")

        user_input = input("Choose an option(1-3): ")

        if user_input == "1":
            show_transactions()
        elif user_input == "2":
            add_transaction()
        elif user_input == "3":
            save_transactions()
            break
        else:
            print("Invalid input.")


menu()
