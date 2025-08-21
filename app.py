import uuid
from datetime import datetime
from pathlib import Path
import csv
from tabulate import tabulate

EXPENSES_FILE = Path("expenses.csv")
transactions = []


def load_transactions():
    transactions.clear()

    if EXPENSES_FILE.exists():
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
    else:
        EXPENSES_FILE.touch()


load_transactions()


def show_transactions():
    if transactions:
        print(tabulate(transactions, headers="keys", tablefmt="fancy_grid"))
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
        "ID": str(uuid.uuid4())[:8],
        "Type": transaction_type,
        "Category": transaction_category,
        "Amount": transaction_amount,
        "Date": transaction_date,
        "Note": transaction_note
    }

    def normalize(transaction):
        return (
            transaction["Type"].strip().lower(),
            transaction["Category"].strip().lower(),
            round(float(transaction["Amount"]), 2),
            str(transaction["Date"])
        )

    if any(normalize(t) == normalize(new_transaction) for t in transactions):
        print("\nTransaction already exists.")
    else:
        transactions.append(new_transaction)
        print("\nTransaction successfully added.")


def delete_transaction():
    if not transactions:
        print("\nNo transactions to delete.")
        return

    show_transactions()
    user_input = input("Enter transaction ID: ").strip().lower()

    for index, t in enumerate(transactions):
        if user_input == t["ID"].lower():
            del transactions[index]
            print("\nTransaction successfully deleted.")
            return

    print("\nTransaction doesn't exist.")


def edit_transaction():
    if not transactions:
        print("\nNo transactions to edit.")
        return

    show_transactions()
    user_input = input("Enter transaction ID: ").strip().lower()

    for t in transactions:
        if user_input == t["ID"].lower():

            print("Editing transaction (leave blank to keep current value):\n")

            new_category = input(
                f"Category [{t["Category"]}]: ").strip() or t["Category"]
            new_amount = input(f"Amount [{t["Amount"]}]: ").strip()
            new_date = input(f"Date [{t["Date"]}]: ").strip() or t["Date"]
            new_note = input(f"Note [{t["Note"]}]: ").strip() or t["Note"]

            t["Category"] = new_category
            t["Amount"] = float(new_amount) if new_amount else t["Amount"]
            t["Date"] = new_date
            t["Note"] = new_note

            print("\nTransaction successfully edited.")
            return

    print("\nTransaction doesn't exist.")


def search_transaction():
    if not transactions:
        print("\nNo transactions to search.")
        return

    query = input("Search in category/note: ").strip().lower()
    if not query:
        print("\nSearch query can't be empty.")
        return

    search_results = [t for t in transactions
                      if query in t["Category"].lower() or query in t["Note"].lower()]

    if search_results:
        print("\nTransaction(s) found:")
        print(tabulate(search_results, headers="keys", tablefmt="fancy_grid"))
    else:
        print("\nNo transaction found.")


def filter_transactions():
    if not transactions:
        print("\nNo transactions to filter.")
        return

    filter_input = input(
        "Filter by 1)Type 2)Category 3)Amount 4)Date: ").strip()
    results = []

    if filter_input == "1":
        filter_type = input("Enter 1 for Income or 2 for Expense: ").strip()
        type_map = {"1": "Income", "2": "Expense"}
        if filter_type not in type_map:
            print("Enter a valid type.")
            return
        results = [t for t in transactions if t["Type"]
                   == type_map[filter_type]]

    elif filter_input == "2":
        filter_category = input("Enter category name: ").strip()
        if not filter_category:
            print("Category can't be empty.")
            return
        results = [t for t in transactions if t["Category"].lower()
                   == filter_category.lower()]

    elif filter_input == "3":
        try:
            min_amount = float(input("Enter min amount: ").strip())
            max_amount = float(input("Enter max amount: ").strip())
            results = [t for t in transactions if min_amount <=
                       t["Amount"] <= max_amount]
        except ValueError:
            print("Enter valid numbers.")
            return

    elif filter_input == "4":
        try:
            from_date = datetime.strptime(
                input("From date (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
            to_date = datetime.strptime(
                input("To date (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
            results = [t for t in transactions if from_date <= datetime.strptime(
                t["Date"], "%Y-%m-%d").date() <= to_date]
        except Exception:
            print("Enter valid dates in YYYY-MM-DD format.")
            return

    else:
        print("Invalid input. Enter a valid filter number.")
        return

    if results:
        print(tabulate(results, headers="keys", tablefmt="fancy_grid"))
    else:
        print("\nNo transactions match your filter.")


def sort_transactions():
    sort_input = input("Sort by 1)Type 2)Amount 3)Date: ").strip()
    sort_map = {"1": "Type", "2": "Amount", "3": "Date"}
    if sort_input not in sort_map:
        print("Enter a valid number.")
        return

    sorted_transactions = sorted(
        transactions, key=lambda t: t[sort_map[sort_input]])

    print(tabulate(sorted_transactions, headers="keys", tablefmt="fancy_grid"))


def save_transactions():
    with open(EXPENSES_FILE, "w", newline="") as ef:
        field_names = ["ID", "Type", "Category", "Amount", "Date", "Note"]
        writer = csv.DictWriter(ef, fieldnames=field_names)
        writer.writeheader()
        for t in transactions:
            writer.writerow({"ID": t["ID"], "Type": t["Type"], "Category": t["Category"],
                            "Amount": t["Amount"], "Date": t["Date"], "Note": t["Note"]})


def menu():
    while True:
        print("\n---Expense Tracker---\n")
        print("1.Show transactions")
        print("2.Add a transaction")
        print("3.Delete a transaction")
        print("4.Edit a transaction")
        print("5.Search a transaction")
        print("6.Filter transactions")
        print("7.Sort transactions")
        print("8.Save and exit")

        user_input = input("Choose an option(1-8): ")

        if user_input == "1":
            show_transactions()
        elif user_input == "2":
            add_transaction()
        elif user_input == "3":
            delete_transaction()
        elif user_input == "4":
            edit_transaction()
        elif user_input == "5":
            search_transaction()
        elif user_input == "6":
            filter_transactions()
        elif user_input == "7":
            sort_transactions()
        elif user_input == "8":
            save_transactions()
            break
        else:
            print("Invalid input.")


menu()
