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
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except OSError:
            pass
