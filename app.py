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
        return {'ID': self.id, 'Type': self.type, 'Category': self.category, 'Amount': self.amount, 'Date': self.date.strftime("%Y-%m-%d") if hasattr(self.date, "strftime") else str(self.date), 'Note': self.note}

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

    def delete_transaction(self):
        if not self.transactions:
            print("\nNo transactions to delete.")
            return

        self.show_transactions()
        user_input = input("Enter transaction ID: ").strip().lower()

        for index, t in enumerate(self.transactions):
            if user_input == t.id.lower():
                del self.transactions[index]
                print("\nTransaction successfully deleted.")
                return

        print("\nTransaction doesn't exist.")

    def edit_transaction(self):
        if not self.transactions:
            print("\nNo transactions to edit.")
            return

        self.show_transactions()
        user_input = input("Enter transaction ID: ").strip().lower()

        for t in self.transactions:
            if user_input == t.id.lower():

                print("Editing transaction (leave blank to keep current value):\n")

                new_category = input(
                    f"Category [{t.category}]: ").strip() or t.category
                new_amount = input(f"Amount [{t.amount}]: ").strip()
                new_date = input(f"Date [{t.date}]: ").strip() or t.date
                new_note = input(f"Note [{t.note}]: ").strip() or t.note

                t.category = new_category
                t.amount = float(new_amount) if new_amount else t.amount
                t.date = new_date
                t.note = new_note

                print("\nTransaction successfully edited.")
                return

        print("\nTransaction doesn't exist.")

    def search_transaction(self):
        if not self.transactions:
            print("\nNo transactions to search.")
            return

        query = input("Search in category/note: ").strip().lower()
        if not query:
            print("\nSearch query can't be empty.")
            return

        search_results = [t for t in self.transactions
                          if query in t.category.lower() or query in t.note.lower()]

        if search_results:
            print("\nTransaction(s) found:")
            print(tabulate([r.to_dict() for r in search_results],
                  headers="keys", tablefmt="fancy_grid"))
        else:
            print("\nNo transaction found.")

    def filter_transactions(self):
        if not self.transactions:
            print("\nNo transactions to filter.")
            return

        filter_input = input(
            "Filter by 1)Type 2)Category 3)Amount 4)Date: ").strip()
        results = []

        if filter_input == "1":
            filter_type = input(
                "Enter 1 for Income or 2 for Expense: ").strip()
            type_map = {"1": "Income", "2": "Expense"}
            if filter_type not in type_map:
                print("Enter a valid type.")
                return
            results = [t for t in self.transactions if t.type
                       == type_map[filter_type]]

        elif filter_input == "2":
            filter_category = input("Enter category name: ").strip()
            if not filter_category:
                print("Category can't be empty.")
                return
            results = [t for t in self.transactions if t.category.lower()
                       == filter_category.lower()]

        elif filter_input == "3":
            try:
                min_amount = float(input("Enter min amount: ").strip())
                max_amount = float(input("Enter max amount: ").strip())
                results = [t for t in self.transactions if min_amount <=
                           t.amount <= max_amount]
            except ValueError:
                print("Enter valid numbers.")
                return

        elif filter_input == "4":
            try:
                from_date = datetime.strptime(
                    input("From date (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
                to_date = datetime.strptime(
                    input("To date (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
                results = [
                    t for t in self.transactions if from_date <= t.date <= to_date]
            except Exception:
                print("Enter valid dates in YYYY-MM-DD format.")
                return

        else:
            print("Invalid input. Enter a valid filter number.")
            return

        if results:
            print(tabulate([r.to_dict() for r in results],
                  headers="keys", tablefmt="fancy_grid"))
        else:
            print("\nNo transactions match your filter.")

    def sort_transactions(self):
        if not self.transactions:
            print("\nNo transactions to sort.")
            return

        sort_input = input("Sort by 1)Type 2)Amount 3)Date: ").strip()
        sort_map = {"1": "Type", "2": "Amount", "3": "Date"}
        if sort_input not in sort_map:
            print("Enter a valid number.")
            return

        sorted_transactions = sorted(
            self.transactions, key=lambda t: getattr(t, sort_map[sort_input].lower()))

        print(tabulate([s.to_dict() for s in sorted_transactions],
              headers="keys", tablefmt="fancy_grid"))

    def show_summary(self):
        if not self.transactions:
            print("\nNo transactions to summarize.")
            return

        income_amount = [t.amount
                         for t in self.transactions if t.type == "Income"]
        expense_amount = [t.amount
                          for t in self.transactions if t.type == "Expense"]
        print(f"\nTotal income: {sum(income_amount)}")
        print(f"Total expense: {sum(expense_amount)}")
        print(f"Balance: {sum(income_amount) - sum(expense_amount)}")
        print("-"*30)

        print(f"Total number of incomes: {len(income_amount)}")
        print(f"Total number of expenses: {len(expense_amount)}")
        print("-"*30)

        income_category = {}
        expense_category = {}
        for t in self.transactions:
            if t.type == "Income":
                income_category[t.category] = income_category.get(
                    t.category, 0) + t.amount
            else:
                expense_category[t.category] = expense_category.get(
                    t.category, 0) + t.amount
        print("Income by category")
        for category, amount in income_category.items():
            print(f"{category:15} {amount}")
        print("\nExpense by category")
        for category, amount in expense_category.items():
            print(f"{category:15} {amount}")

    def save_transactions(self):
        transactions_data = [t.to_dict() for t in self.transactions]
        with open(self.file_path, "w") as ef:
            json.dump(transactions_data, ef, indent=4)

    def clear_transactions(self):
        if not self.transactions:
            print("\nNo transactions to clear.")
            return

        while True:
            confirm = input(
                "\nDo you want to clear all transactions?(y|n): ").strip().lower()
            if confirm == "y":
                self.transactions.clear()
                print("All transactions successfully cleared.")
                break
            elif confirm == "n":
                print("Action cancelled.")
                break
            else:
                print("Invalid input. Enter 'y' or 'n'.")

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
