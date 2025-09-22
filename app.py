from pathlib import Path
import uuid
from datetime import datetime
from tabulate import tabulate
import json


class Transaction:
    def __init__(self, t_id, t_type, t_category, t_amount, t_date, t_note):
        self.id = t_id
        self.type = t_type
        self.category = t_category
        self.amount = t_amount
        self.date = t_date
        self.note = t_note

    def to_dict(self):
        return {'ID': self.id, 'Type': self.type, 'Category': self.category, 'Amount': self.amount, 'Date': self.date.strftime("%Y-%m-%d"), 'Note': self.note}

    @classmethod
    def from_dict(cls, data):
        return cls(data['ID'], data['Type'], data['Category'], data['Amount'], datetime.strptime(data['Date'], "%Y-%m-%d").date(), data['Note'])


class ExpenseTracker:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.transactions = []

    def load_transactions(self):
        self.transactions.clear()

        if self.file_path.exists():
            with open(self.file_path, "r") as ef:
                try:
                    data = json.load(ef)
                    self.transactions = [
                        Transaction.from_dict(d) for d in data]
                except json.JSONDecodeError:
                    self.transactions.clear()
        else:
            self.file_path.touch()

    def show_transactions(self):
        if self.transactions:
            transaction_data = [t.to_dict() for t in self.transactions]
            print(tabulate(transaction_data, headers="keys", tablefmt="fancy_grid"))
        else:
            print("\nYou have no transactions.")

    def add_transaction(self):
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
                transaction_date = datetime.strptime(
                    date_input, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date. Use YYYY-MM-DD format.")

        transaction_note = input("Enter transaction note: ").strip()

        new_transaction = Transaction(
            t_id=str(uuid.uuid4())[:8],
            t_type=transaction_type,
            t_category=transaction_category,
            t_amount=transaction_amount,
            t_date=transaction_date,
            t_note=transaction_note
        )

        def normalize(transaction):
            return (
                transaction.type.strip().lower(),
                transaction.category.strip().lower(),
                round(float(transaction.amount), 2),
                str(transaction.date)
            )

        if any(normalize(t) == normalize(new_transaction) for t in self.transactions):
            print("\nTransaction already exists.")
        else:
            self.transactions.append(new_transaction)
            print("\nTransaction successfully added.")

    def save_transactions(self):
        transactions_data = [t.to_dict() for t in self.transactions]
        with open(self.file_path, "w") as ef:
            json.dump(transactions_data, ef, indent=4)

    def menu(self):
        while True:
            print("\n---Expense Tracker---\n")
            print("1.Show transactions")
            print("2.Add a transaction")
            print("3.Delete a transaction")
            print("4.Edit a transaction")
            print("5.Search a transaction")
            print("6.Filter transactions")
            print("7.Sort transactions")
            print("8.Show summary")
            print("9.Clear transactions")
            print("10.Save and exit")

            user_input = input("Choose an option(1-10): ")

            if user_input == "1":
                self.show_transactions()
            elif user_input == "2":
                self.add_transaction()
            elif user_input == "3":
                self.delete_transaction()
            elif user_input == "4":
                self.edit_transaction()
            elif user_input == "5":
                self.search_transaction()
            elif user_input == "6":
                self.filter_transactions()
            elif user_input == "7":
                self.sort_transactions()
            elif user_input == "8":
                self.show_summary()
            elif user_input == "9":
                self.clear_transactions()
            elif user_input == "10":
                self.save_transactions()
                break
            else:
                print("Invalid input.")


if __name__ == "__main__":
    tracker = ExpenseTracker("expenses.json")
    tracker.load_transactions()
    tracker.menu()
