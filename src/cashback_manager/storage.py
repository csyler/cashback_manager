import json
import os

class DataStorage:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Invalid JSON in {self.filename}: {e}")
            except OSError as e:
                raise RuntimeError(f"Error opening {self.filename}: {e}")
        return {}

    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except OSError as e:
            raise RuntimeError(f"Error saving {self.filename}: {e}")

    def delete_file(self):
        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except OSError as e:
            raise RuntimeError(f"Error deleting {self.filename}: {e}")
