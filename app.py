transactions = []


def save_transactions():
    pass


def add_transaction():
    pass


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
