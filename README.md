# Expense Tracker (CLI)

A simple object-oriented (OOP) command-line interface expense tracker written in Python. Track your incomes and expenses, view summaries, and save/load transactions in JSON format.

## Features

- Add, edit, and delete transactions
- Search transactions by category or note
- Filter transactions by type, category, amount, or date
- Sort transactions by type, amount, or date
- Show summary: total incomes, total expenses, balance, and category breakdown
- Save and load transactions to/from a CSV file
- Clear all transactions

## Installation

1. Clone the repository:

```bash
git clone https://github.com/KaramiZahra/Expense-Tracker
cd Expense-Tracker
```

2. Make sure you have Python 3 installed.

3. Install required dependencies (only `tabulate`):

```bash
pip install tabulate
```

## Usage

Run the main script:

```bash
python app.py
```

The menu options:

1. Show transactions
2. Add a transaction
3. Delete a transaction
4. Edit a transaction
5. Search a transaction
6. Filter transactions
7. Sort transactions
8. Show summary
9. Clear transactions
10. Save and exit

Follow the prompts to manage your transactions.

## File Structure

- `app.py` – main program
- `expenses.json` – saved transactions (created automatically)

## Notes

- Transaction fields include: `ID` (unique), `Type` (Income/Expense), `Category`, `Amount`, `Date`, and `Note`.
- Date format: `YYYY-MM-DD`.
- Duplicate transactions (same type, category, amount, date) are not allowed.
