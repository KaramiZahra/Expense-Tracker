from pathlib import Path


class Transaction:
    def __init__(self, t_id, t_type, t_category, t_amount, t_date, t_note):
        self.id = t_id
        self.type = t_type
        self.category = t_category
        self.amount = t_amount
        self.date = t_date
        self.note = t_note


class ExpenseTracker:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.transactions = []
