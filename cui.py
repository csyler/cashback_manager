import sys
from .manager import CashbackManager
from .models import Cashback
from .storage import DataStorage

class CLI:
    def __init__(self, manager):
        self.manager = manager
        self.confirmations = ["yes", "y"]
        self.storage = self.manager.storage

    def prompt_float(self, message):
        while True:
            try:
                value = float(input(message))
                if value <= 0:
                    raise ValueError
                return value
            except ValueError:
                print("Enter a positive number.")

    def main_menu(self):
        options = {
            "1": ("Add cashback", self.add_cashback),
            "2": ("Show all cashbacks", self.show_all),
            "3": ("Find cashback", self.find_cashback),
            "4": ("Delete cashback", self.delete_cashback),
            "5": ("Delete bank", self.delete_bank),
            "6": ("Clear all", self.clear_all),
            "7": ("Exit", self.exit)
        }

        while True:
            print("\n" + "-"*30)
            print("Cashback Manager")
            print("-"*30)
            for key, (desc, _) in options.items():
                print(f"{key}. {desc}")
            choice = input("Select an option: ").strip()
            action = options.get(choice)
            if action:
                action[1]()
            else:
                print("Invalid choice, try again.")

    def add_cashback(self):
        bank = input("Bank name: ").strip()
        cashback_name = input("Cashback name: ").strip()
        existing = self.storage.data.get(bank, {}).get(cashback_name)
        if existing:
            confirm = input(f"Cashback '{cashback_name}' exists in '{bank}'. Replace? (yes/no): ").lower()
            if confirm not in self.confirmations:
                return
        percent = self.prompt_float("Percent: ")
        self.manager.add_cashback(bank, Cashback(cashback_name, percent))
        print(f"Added cashback '{cashback_name}' in '{bank}' with {percent}%.")

    def show_all(self):
        data = self.storage.data
        if not data:
            print("No data.")
            return
        for bank, cashbacks in data.items():
            print(f"\n{bank}")
            for name, percent in cashbacks.items():
                print(f"  {name}: {percent}%")
        total = sum(len(c) for c in data.values())
        print(f"\nTotal cashbacks: {total}")

    def find_cashback(self):
        name = input("Cashback name to search: ").strip()
        results = self.manager.find_cashback(name)
        if results:
            print(f"Results ({len(results)}):")
            for bank, name, percent in results:
                print(f"{bank}: {name} - {percent}%")
        else:
            print("Cashback not found.")

    def delete_cashback(self):
        bank = input("Bank name: ").strip()
        name = input("Cashback name: ").strip()
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm in self.confirmations:
            self.manager.delete_cashback(bank, name)

    def delete_bank(self):
        bank = input("Bank name: ").strip()
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm in self.confirmations:
            self.manager.delete_bank(bank)

    def clear_all(self):
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm in self.confirmations:
            self.manager.clear_all()

    def exit(self):
        print("Goodbye!")
        sys.exit()

if __name__ == "__main__":
    filename = input("Enter filename for data storage: ").strip()
    storage = DataStorage(filename)
    manager = CashbackManager(storage)
    cli = CLI(manager)
    cli.main_menu()
