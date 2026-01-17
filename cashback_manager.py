from dataclasses import dataclass
import json
import os


@dataclass
class Cashback:
    name: str
    percent: float


class DataStorage:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except OSError:
            pass

    def delete_file(self):
        try:
            os.remove(self.filename)
        except OSError:
            pass


class CashbackManager:
    def __init__(self, storage: DataStorage):
        self.storage = storage

    def _clear_storage(self):
        self.storage.data.clear()
        self.storage.delete_file()

    def add_cashback(self, bank: str, cashback: Cashback):
        if bank not in self.storage.data:
            self.storage.data[bank] = {}
        self.storage.data[bank][cashback.name] = cashback.percent
        self.storage.save()

    def find_cashback(self, cashback_name: str):
        results = []
        for bank, cashbacks in self.storage.data.items():
            for name, percent in cashbacks.items():
                if name.lower() == cashback_name.lower():
                    results.append((bank, name, percent))
        return sorted(results, key=lambda x: x[2], reverse=True)

    def delete_cashback(self, bank: str, cashback_name: str):
        if bank in self.storage.data:
            if cashback_name in self.storage.data[bank]:
                del self.storage.data[bank][cashback_name]
                if not self.storage.data[bank]:
                    del self.storage.data[bank]
                self.storage.save()
                if not self.storage.data:
                    self._clear_storage()
                    print(
                        f"Cashback '{cashback_name}' deleted from '{bank}' and cleared"
                    )
                else:
                    print(f"Cashback '{cashback_name}' deleted from '{bank}'")
            else:
                print(f"Cashback '{cashback_name}' not found in '{bank}'")
                return
        else:
            print(f"Bank '{bank}' does not exist")
            return

    def delete_bank(self, bank: str):
        if bank not in self.storage.data:
            print(f"Not exist")
            return
        del self.storage.data[bank]
        self.storage.save()
        if not self.storage.data:
            self._clear_storage()
            print("Cleared")
        else:
            print(f"Bank '{bank}' deleted")

    def clear_all(self):
        if not self.storage.data:
            print("Nothing to clear")
        else:
            self._clear_storage()
            print("Cleared")


class CUI:
    def __init__(self, manager: CashbackManager):
        self.manager = manager
        self.confirmations = ["yes", "y"]

    def prompt_float(self, message: str) -> float:
        while True:
            try:
                value = float(input(message))
                if value <= 0:
                    raise ValueError
                return value
            except ValueError:
                print("Enter a positive number")

    def main_menu(self):
        menu_actions = {
            "1": ("Add cashback", self.add_cashback),
            "2": ("Show all cashbacks", self.show_all),
            "3": ("Edit cashback", self.edit_cashback),
            "4": ("Find cashback", self.find_cashback),
            "5": ("Delete cashback", self.delete_cashback),
            "6": ("Delete bank", self.delete_bank),
            "7": ("Delete ALL", self.clear_all),
            "8": ("Exit", self.exit_program),
        }

        while True:
            print("\n" + "-" * 40)
            print("CASHBACK MANAGER")
            print("-" * 40)

            for key, (text, _) in menu_actions.items():
                print(f"{key}. {text}")

            print("-" * 40)

            choice = input("Select an option (1-8): ").strip()
            action = menu_actions.get(choice)
            if action:
                action[1]()
            else:
                print("Enter a number from 1 to 8")

    def add_cashback(self):
        bank = input("Bank name: ").strip()
        cashback_name = input("Cashback name: ").strip()
        existing = self.manager.storage.data.get(bank, {}).get(cashback_name)
        if existing:
            confirm = input(
                f"Cashback '{cashback_name}' already exists in {bank}. Replace? (yes/no): "
            ).lower()
            if confirm not in self.confirmations:
                return
        percent = self.prompt_float("percent (%): ")
        self.manager.add_cashback(bank, Cashback(cashback_name, percent))
        print(f"Cashback '{cashback_name}' in '{bank}' added with {percent}%.")

    def show_all(self):
        data = self.manager.storage.data
        if not data:
            print("No data")
            return
        for bank, cashbacks in data.items():
            print(f"\n{bank}")
            for name, percent in cashbacks.items():
                print(f"  {name}: {percent}%")
        print(f"\nTotal cashbacks: {sum(len(c) for c in data.values())}")

    def find_cashback(self):
        name = input("Enter cashback name to search: ").strip()
        results = self.manager.find_cashback(name)
        if results:
            print(f"Results ({len(results)}):")
            for bank, name, percent in results:
                print(f"{bank}   {name}: {percent}%")
        else:
            print("Cashback not found")

    def delete_cashback(self):
        bank = input("Bank name: ").strip()
        cashback_name = input("Cashback name: ").strip()
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm in self.confirmations:
            self.manager.delete_cashback(bank, cashback_name)

    def delete_bank(self):
        bank = input("Bank name: ").strip()
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm in self.confirmations:
            self.manager.delete_bank(bank)

    def clear_all(self):
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm in self.confirmations:
            self.manager.clear_all()

    def edit_cashback(self):
        data = self.manager.storage.data
        if not data:
            print("No data")
            return

        self.show_all()

        bank = input("\nEnter the bank name to edit: ").strip()
        if bank not in data:
            print(f"Bank '{bank}' not found.")
            return

        category = input("\nEnter the cashback name to edit: ").strip()
        if category not in data[bank]:
            print(f"Cashback '{category}' not found in '{bank}'.")
            return

        current_percent = data[bank][category]
        print(f"\nEditing cashback '{category}' in '{bank}'")
        print(f"Current percent: {current_percent}%")
        print("-" * 40)

        if input("Change the rate? (yes/no): ").strip().lower() in self.confirmations:
            new_percent = self.prompt_float(f"Enter percent: ")
            data[bank][category] = new_percent
            self.manager.storage.save()
            print(f"\n'{category}' in '{bank}' updated to {new_percent}%.")
        else:
            print("Canceled")

    def exit_program(self):
        print("Bye")
        exit()


if __name__ == "__main__":
    storage = DataStorage(input("Enter filename: ").strip())
    manager = CashbackManager(storage)
    ui = CUI(manager)
    ui.main_menu()
