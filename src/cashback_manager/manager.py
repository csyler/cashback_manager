from .models import Cashback
from .storage import DataStorage

class CashbackManager:
    def __init__(self, storage):
        self.storage = storage

    def add_cashback(self, bank, cashback: Cashback):
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

    def delete_cashback(self, bank, cashback_name):
        if bank in self.storage.data:
            if cashback_name in self.storage.data[bank]:
                del self.storage.data[bank][cashback_name]
                if not self.storage.data[bank]:
                    del self.storage.data[bank]
                self.storage.save()
                if not self.storage.data:
                    self.storage.delete_file()
            else:
                print(f"Cashback '{cashback_name}' not found in '{bank}'")
        else:
            print(f"Bank '{bank}' does not exist")

    def delete_bank(self, bank):
        if bank in self.storage.data:
            del self.storage.data[bank]
            self.storage.save()
            if not self.storage.data:
                self.storage.delete_file()
        else:
            print("Bank does not exist.")

    def clear_all(self):
        self.storage.data.clear()
        self.storage.delete_file()
