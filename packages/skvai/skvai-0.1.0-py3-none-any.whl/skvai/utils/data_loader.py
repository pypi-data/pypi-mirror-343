import pandas as pd

class DataLoader:
    def __init__(self):
        self.data = None

    def load_csv(self, file_path):
        try:
            self.data = pd.read_csv(file_path)
            print("[✔] CSV data loaded successfully.")
            return self.data
        except Exception as e:
            print(f"[✘] Failed to load CSV: {e}")
            return None

    def preview(self, rows=5):
        if self.data is not None:
            return self.data.head(rows)
        else:
            print("[!] No data loaded yet.")
            return None
def load_data(file_path):
    loader = DataLoader()
    return loader.load_csv(file_path)
