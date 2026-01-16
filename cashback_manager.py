import json
import os


class ConsoleCashbackApp:
    def __init__(self, filename: str):
        self.filename = f"{filename}.json"
        self.cashbacks: dict = self.load_data()
        self.confirmations: list[str] = ["yes", "y"]

    def load_data(self) -> dict:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except OSError:
                return {}
        return {}

    def save_data(self) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.cashbacks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(
                f"Error saving to file {self.filename}: {type(e).__name__} - {str(e)}"
            )
            try:
                self.filename = "my_cashbacks.json"
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump(self.cashbacks, f, indent=2, ensure_ascii=False)
                print(
                    f"Name changed to my_cashbacks.json due to an error {type(e).__name__}"
                )
            except Exception as backup_error:
                print(f"Error! Failed to save data: {type(backup_error).__name__}")
                return

    def bank_exists(self, bank_name: str, cashback_name: str) -> bool:
        if bank_name not in self.cashbacks:
            return False

        return any(
            cb.lower() == cashback_name.lower() for cb in self.cashbacks[bank_name]
        )

    def get_valid_input(self, prompt: str) -> float:
        while True:
            try:
                value: float = float(input(prompt))
                if value < 0.01:
                    raise ValueError
                return value

            except ValueError:
                print("Error! Please enter a positive number.")

    def add_cashback(self) -> None:
        print("\n" + "=" * 40)
        print("ADD NEW CASHBACK")
        print("=" * 40)

        while True:
            bank: str = input("Bank name: ").strip()
            if not bank:
                print("The bank name cannot be empty.")
                continue
            break

        while True:
            cashback: str = input("Cashback: ").strip()

            if not cashback:
                print("The cashback cannot be empty.")
                continue

            # Check if such a cashback already exists
            if self.bank_exists(bank, cashback):
                print(f"Cashback '{cashback}' is already in the {bank}")

                overwrite: str = input("Replace existing cashback? (yes/no): ").lower()
                if overwrite in self.confirmations:
                    self.cashbacks[bank] = {
                        k: v
                        for k, v in self.cashbacks.get(bank, {}).items()
                        if k.lower() != cashback.lower()
                    }
                    break
                else:
                    continue
            else:
                break

        percent: float = self.get_valid_input("Percent (%): ")

        if bank not in self.cashbacks:
            self.cashbacks[bank] = {}

        self.cashbacks[bank][cashback] = percent
        self.save_data()
        print(f"\nAdded cashback: {cashback} with percent {percent}% in {bank}")

    def edit_cashback(self) -> None:
        is_changed: bool = False
        self.show_all()

        if not self.cashbacks:
            return

        while True:
            try:
                while True:
                    bank: str = input("\nBank name to edit: ")

                    if bank not in self.cashbacks:
                        print("Invalid name")
                    else:
                        break

                while True:
                    category: str = input("\nCashback name to edit: ")

                    if category not in self.cashbacks[bank]:
                        print("Invalid cashback")
                    else:
                        break

                cashback = self.cashbacks[bank]
                print(f"\nEditing cashback: {category} in {bank}")
                print(f"Current percent: {cashback[category]}%")
                print("-" * 40)

                # Change rate
                change_percent: str = input("Change rate? (yes/no): ").lower()
                if change_percent in self.confirmations:
                    is_changed = True
                    new_percent: float = self.get_valid_input(
                        f"New percent (current {cashback[category]}%): "
                    )
                    cashback[category] = new_percent

                self.save_data()
                if is_changed:
                    print("\nCashback updated!")
                    print(f"New percent: {cashback[category]}")
                else:
                    print("\nCashback remains unchanged!")
                return

            except ValueError:
                print("Error! Enter a string")

    def show_all(self) -> None:
        if not self.cashbacks:
            print("\nNo saved cashbacks")
            return

        print("\n" + "=" * 40)
        print("YOUR CASHBACKS")
        print("=" * 40)

        for bank, cashbacks in self.cashbacks.items():
            print(bank)
            for cashback, percent in cashbacks.items():
                print(f"   {cashback}: {percent}%")
            print()

        print("=" * 40)
        print(
            f"Total cashbacks: {sum(len(cashbacks) for cashbacks in self.cashbacks.values())}"
        )

    def find_cashback(self):
        cashbacks_category: list = []
        while True:
            data: str = input("Cashback: ").strip()

            if not data:
                print("The cashback cannot be empty.")
                continue

            if any(
                cb.lower() == data.lower()
                for bank in self.cashbacks
                for cb in self.cashbacks[bank]
            ):
                for bank, cashbacks in self.cashbacks.items():
                    for cashback, percent in cashbacks.items():
                        if cashback == data:
                            cashbacks_category.append((bank, cashback, percent))
                print(
                    *(
                        f"{item[0]}  {item[1]}  {item[2]}"
                        for item in sorted(
                            cashbacks_category, key=lambda item: item[2], reverse=True
                        )
                    ),
                    sep="\n",
                )
                break
            else:
                print(f"Cashback '{data}' not found")
                break

    def delete_cashback(self) -> None:
        self.show_all()

        if not self.cashbacks:
            return

        while True:
            try:
                while True:
                    bank: str = input("Bank name: ").strip()
                    if bank in self.cashbacks:
                        while True:
                            category: str = input("Cashback name: ").strip()
                            if category in self.cashbacks[bank]:
                                confirm: str = (
                                    input("\nAre you sure? (yes/no): ").strip().lower()
                                )
                                if confirm not in self.confirmations:
                                    print("Deletion canceled")
                                    return
                                del self.cashbacks[bank][category]
                                if not self.cashbacks[bank]:
                                    del self.cashbacks[bank]
                                self.save_data()
                                if not self.cashbacks:
                                    try:
                                        os.remove(self.filename)
                                    except OSError as e:
                                        print(f"Failed to delete file {self.filename}: {e}")
                                        return
                                print(f"\nDeleted cashback: {category} in {bank}")
                                print(f"Remaining cashbacks: {sum(len(c) for c in self.cashbacks.values())}")
                                return
                            else:
                                print("Invalid category")
                    else:
                        print("Invalid bank")
            except ValueError:
                print("Error! Enter a str")

    def delete_bank(self) -> None:
        self.show_all()

        if not self.cashbacks:
            return

        while True:
            try:
                while True:
                    bank: str = input("Bank name: ").strip()
                    if bank in self.cashbacks:
                        confirm: str = (
                            input("\nAre you sure? (yes/no): ").strip().lower()
                        )
                        if confirm not in self.confirmations:
                            print("Deletion canceled")
                            return
                        del self.cashbacks[bank]
                        self.save_data()
                        if not self.cashbacks:
                            try:
                                os.remove(self.filename)
                            except OSError as e:
                                print(f"Failed to delete file {self.filename}: {e}")
                                return
                        print(f"\nDeleted bank: {bank}")
                        print(f"Remaining bank: {len(self.cashbacks)}")
                        return
                    else:
                        print("Invalid bank")
            except ValueError:
                print("Error! Enter a str")

    def clear_all(self) -> None:
        if not self.cashbacks and not os.path.exists(self.filename):
            print("\nNo saved cashbacks")
            return

        print("\n" + "=" * 50)
        print("DELETING ALL CASHBACKS")
        print("=" * 50)
        print(f"Number of cashbacks: {sum(len(cashbacks) for cashbacks in self.cashbacks.values())}")
        print("\nList of banks for deletion:")

        for bank, cashbacks in self.cashbacks.items():
            print(f"  {bank}")
            for cashback in cashbacks:
                print(f"    {cashback}")

        print("\n" + "=" * 50)
        print("This action is IRREVERSIBLE!")
        print("All data will be deleted without the possibility of recovery!")
        print("=" * 50)

        confirm: str = input("\nAre you sure? (yes/no): ").strip().lower()
        if confirm not in self.confirmations:
            print("Deletion canceled")
            return

        self.cashbacks = {}

        print("\n" + "✖" * 50)
        print("ALL CASHBACKS DELETED")
        print("✖" * 50)
        try:
            os.remove(self.filename)
            print(f"Data file deleted: {self.filename}")
        except OSError as e:
            print(f"Failed to delete file {self.filename}: {e}")
        print("✖" * 50)

    def run(self) -> None:
        menu_actions = {
            "1": ("Add cashback", self.add_cashback),
            "2": ("Show all cashbacks", self.show_all),
            "3": ("Edit cashback", self.edit_cashback),
            "4": ("Find cashback", self.find_cashback),
            "5": ("Delete cashback", self.delete_cashback),
            "6": ("Delete bank", self.delete_bank),
            "7": ("Delete ALL", self.clear_all),
            "8": ("Exit", None),
        }

        while True:
            print("\n" + "=" * 40)
            print("CASHBACK MANAGER")
            print("=" * 40)

            for key, (text, _) in menu_actions.items():
                print(f"{key}. {text}")

            print("=" * 40)

            choice: str = input("Select (1-8): ").strip()

            if choice == "8":
                print("\nData saved.")
                print("Goodbye!")
                break

            if choice in menu_actions:
                _, action = menu_actions[choice]
                if action:
                    action()

            else:
                print("Error! Select a number from 1 to 8")


if __name__ == "__main__":
    app = ConsoleCashbackApp(input("Enter the name for the file: "))
    app.run()
