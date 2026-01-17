from .models import Cashback
from .storage import DataStorage

class CashbackManager:
    def __init__(self, storage):
        self.storage = storage

    def add_cashback(self, bank, cashback: Cashback):
        if not isinstance(cashback, Cashback):
            raise TypeError("cashback must be an instance of Cashback")
        if bank not in self.storage.data:
            self.storage.data[bank] = {}
        self.storage.data[bank][cashback.name] = cashback.percent
        self.storage.save()

    def find_cashback(self, cashback_name):
        results = []
        for bank, cashbacks in self.storage.data.items():
            for name, percent in cashbacks.items():
                if name.lower() == cashback_name.lower():
                    results.append((bank, name, percent))
        return sorted(results, key=lambda x: x[2], reverse=True)

    def edit_cashback(self, bank, cashback_name, new_percent):
        if bank not in self.storage.data:
            raise ValueError(f"Bank '{bank}' does not exist")
        if cashback_name not in self.storage.data[bank]:
            raise ValueError(f"Cashback '{cashback_name}' not found in '{bank}'.")
        self.storage.data[bank][cashback_name] = new_percent
        self.storage.save()

    def delete_cashback(self, bank, cashback_name):
        if bank not in self.storage.data:
            raise ValueError(f"Bank '{bank}' does not exist")
        if cashback_name not in self.storage.data[bank]:
            raise ValueError(f"Cashback '{cashback_name}' not found in '{bank}'")
        del self.storage.data[bank][cashback_name]
        if not self.storage.data[bank]:
            del self.storage.data[bank]
        self.storage.save()
        if not self.storage.data:
            self.storage.delete_file()

    def delete_bank(self, bank):
        if bank not in self.storage.data:
            raise ValueError(f"Bank '{bank}' does not exist")
        del self.storage.data[bank]
        self.storage.save()
        if not self.storage.data:
            self.storage.delete_file()

    def clear_all(self):
        self.storage.data.clear()
        self.storage.delete_file()
