from pathlib import Path


class Transaction:
    def __init__(self, t_id, t_type, t_category, t_amount, t_date, t_note):
        self.id = t_id
        self.type = t_type
        self.category = t_category
        self.amount = t_amount
        self.date = t_date
        self.note = t_note

    def to_dict(self):
        return {'ID': self.id, 'Type': self.type, 'Category': self.category, 'Amount': self.amount, 'Date': self.date, 'Note': self.note}

    @classmethod
    def from_dict(cls, data):
        return cls(data['ID'], data['Type'], data['Category'], data['Amount'], data['Date'], data['Note'])


class ExpenseTracker:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.transactions = []

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
    expenses = ExpenseTracker("expenses.json")
    expenses.menu()
