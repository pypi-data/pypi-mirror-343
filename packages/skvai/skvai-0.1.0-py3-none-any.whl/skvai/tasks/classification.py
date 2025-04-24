from skvai.utils.data_loader import DataLoader
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import pandas as pd

class Task:
    def __init__(self):
        self.loader      = DataLoader()
        self.model       = None
        self.data        = None
        self.target      = None
        self.user_target = None

    def load_data(self, path):
        print(f"📄 Loading classification data from {path}")
        df = self.loader.load_csv(path)
        if df is None:
            raise ValueError("Failed to load data.")

        print(f"Initial DataFrame shape: {df.shape}")  # Print initial shape

        # Optional: Check if there's any filter being applied, like age range or other conditions.
        # Example: Check if there's a filter for age between 8 and 80
        if 'age' in df.columns:
            df = df[(df['age'] >= 8) & (df['age'] <= 80)]  # Add this line if you're filtering by age range
        else:
            print("[!] Skipping 'age' filtering — column not found.")
        print(f"DataFrame shape after filtering: {df.shape}")  # Print shape after filtering
        
        if getattr(self, 'user_target', None):
            if self.user_target not in df.columns:
                raise ValueError(f"Target column '{self.user_target}' not found.")
            self.target = self.user_target
        else:
            self.target = df.columns[-1]

        # 1) drop rows where target is NaN
        df = df[df[self.target].notnull()]

        # 2) separate features & target
        X = df.drop(columns=[self.target])
        y = df[self.target].reset_index(drop=True)

        # 3) fill other NaNs in features with a placeholder
        X = X.fillna('missing')

        # 4) one-hot encode categorical & combine
        X_encoded = pd.get_dummies(X, drop_first=True)
        self.data = pd.concat([X_encoded, y], axis=1)

    def train_and_output(self, format="graph"):
        X = self.data.drop(columns=[self.target])
        y = self.data[self.target]

        # 🔧 Encode categorical features
        X = pd.get_dummies(X, drop_first=True)

        # 🧪 Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # 🤖 Train model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X_train, y_train)

        # 🎯 Evaluate
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"✅ Accuracy: {acc:.4f}")

        # 📤 Output options
        if "metrics" in format:
            self._display_metrics(y_test, y_pred, acc)
        
        if "plot" in format:
            self._plot_cm(y_test, y_pred)

        if "csv" in format:
            # Make sure to re-encode the full dataset
            full_X = pd.get_dummies(self.data.drop(columns=[self.target]), drop_first=True)
            self.data["prediction"] = self.model.predict(full_X)
            self.data.to_csv("predictions.csv", index=False)
            print("📂 Saved predictions.csv")

        if "save" in format:
            joblib.dump(self.model, "classification_model.pkl")
            print("💾 Saved classification_model.pkl")

        if not any(opt in format for opt in ["metrics", "plot", "csv", "save"]):
            print("❌ Unsupported format")

    def set_target(self, col_name):
        """
        Call this *before* load_data() to override the default target column.
        """
        self.user_target = col_name

    def _plot_cm(self, y_true, y_pred):
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=self.data[self.target].unique(),
                    yticklabels=self.data[self.target].unique())
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

    def _display_metrics(self, y_true, y_pred, acc):
        cm = confusion_matrix(y_true, y_pred)
        print(f"Accuracy: {acc:.4f}")
        print("Confusion Matrix:")
        print(cm)
