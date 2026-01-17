import sys
from .manager import CashbackManager
from .models import Cashback
from .storage import DataStorage


class CUI:
    def __init__(self, manager):
        self.manager = manager
        self.confirmations = ["yes", "y"]
        self.storage = self.manager.storage

    def prompt_float(self, message):
        while True:
            try:
                value = float(input(message))
                if value <= 0:
                    print("Enter a positive number ")
                    continue
                return value
            except ValueError:
                print("Please enter a number ")

    def main_menu(self):
        options = {
            "1": ("Add cashback", self.add_cashback),
            "2": ("Show all cashbacks", self.show_all),
            "3": ("Edit cashback", self.edit_cashback),
            "4": ("Find cashback", self.find_cashback),
            "5": ("Delete cashback", self.delete_cashback),
            "6": ("Delete bank", self.delete_bank),
            "7": ("Clear all", self.clear_all),
            "8": ("Exit", self.exit),
        }

        while True:
            print("\n" + "-" * 30)
            print("Cashback Manager")
            print("-" * 30)
            for key, (desc, _) in options.items():
                print(f"{key}. {desc}")
            choice = input("Select num 1-8 ").strip()
            action = options.get(choice)
            if action:
                try:
                    action[1]()
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Enter num 1-8 ")

    def add_cashback(self):
        try:
            bank = input("Bank name: ").strip()
            cashback_name = input("Cashback name: ").strip()
            existing = self.storage.data.get(bank, {}).get(cashback_name)
            if existing:
                confirm = input(
                    f"Cashback '{cashback_name}' exists in '{bank}'. Replace? (yes/no): "
                ).lower()
                if confirm not in self.confirmations:
                    return
            percent = self.prompt_float("Percent: ")
            self.manager.add_cashback(bank, Cashback(cashback_name, percent))
            print(f"Added cashback '{cashback_name}' in '{bank}' with {percent}%")
        except Exception as e:
            print(f"Failed: {e}")

    def show_all(self):
        try:
            data = self.storage.data
            if not data:
                print("No data")
                return
            for bank, cashbacks in data.items():
                print(f"\n{bank}")
                for name, percent in cashbacks.items():
                    print(f"  {name}: {percent}%")
            total = sum(len(c) for c in data.values())
            print(f"\nTotal cashbacks: {total}")
        except Exception as e:
            print(f"Error: {e}")

    def find_cashback(self):
        try:
            name = input("Cashback name to search: ").strip()
            results = self.manager.find_cashback(name)
            if results:
                print(f"Results ({len(results)}):")
                for bank, name, percent in results:
                    print(f"{bank}: {name} - {percent}%")
            else:
                print("Cashback not found")
        except Exception as e:
            print(f"Error: {e}")

    def edit_cashback(self):
        try:
            bank = input("Bank name: ").strip()
            cashback_name = input("Cashback name: ").strip()
            if (
                bank not in self.storage.data
                or cashback_name not in self.storage.data[bank]
            ):
                print("Cashback not found")
                return
            new_percent = self.prompt_float("New percent: ")
            self.manager.edit_cashback(bank, cashback_name, new_percent)
            print(f"Cashback '{cashback_name}' in '{bank}' updated to {new_percent}%")
        except Exception as e:
            print(f"Error: {e}")

    def delete_cashback(self):
        try:
            bank = input("Bank name: ").strip()
            name = input("Cashback name: ").strip()
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm in self.confirmations:
                self.manager.delete_cashback(bank, name)
                print("Cashback deleted")
        except Exception as e:
            print(f"Error: {e}")

    def delete_bank(self):
        try:
            bank = input("Bank name: ").strip()
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm in self.confirmations:
                self.manager.delete_bank(bank)
                print("Bank deleted")
        except Exception as e:
            print(f"Error: {e}")

    def clear_all(self):
        try:
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm in self.confirmations:
                self.manager.clear_all()
                print("Cleared")
        except Exception as e:
            print(f"Error: {e}")

    def exit(self):
        print("Bye!")
        sys.exit()


if __name__ == "__main__":
    filename = input("Enter filename: ").strip()
    try:
        storage = DataStorage(filename)
        manager = CashbackManager(storage)
        cui = CUI(manager)
        cui.main_menu()
    except Exception as e:
        print(f"Failed to start: {e}")
