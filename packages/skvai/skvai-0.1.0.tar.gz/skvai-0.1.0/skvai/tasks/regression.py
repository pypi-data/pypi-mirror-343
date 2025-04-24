# skvai/tasks/regression.py

import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from skvai.core import CSVData

def regress(
    data: CSVData,
    model: str = "LinearRegression",
    output: list = ["metrics"],
    save_path: str = "regressor.pkl",
    prediction_csv: str = "predictions.csv",
    test_size: float = 0.2,
    random_state: int = 42
):
    """
    Train and evaluate a regression model on CSVData.

    Args:
        data (CSVData): Loaded dataset with X, y, df.
        model (str): 'LinearRegression' or 'RandomForestRegressor'.
        output (list): Options: 'metrics', 'plot', 'csv', 'save'.
        save_path (str): Save path for model.
        prediction_csv (str): Save path for predictions.
        test_size (float): Split size for testing.
        random_state (int): Seed for reproducibility.

    Returns:
        dict: mse, r2, predictions, model
    """
    if not hasattr(data, "X") or not hasattr(data, "y"):
        raise AttributeError("CSVData must have attributes 'X' and 'y'.")

    # Select model
    if model == "LinearRegression":
        reg = LinearRegression()
    elif model == "RandomForestRegressor":
        reg = RandomForestRegressor(random_state=random_state)
    else:
        raise ValueError(f"Unsupported model: {model}")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        data.X, data.y, test_size=test_size, random_state=random_state
    )

    # Fit model
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    # Evaluation
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    if "metrics" in output:
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"R^2 Score: {r2:.4f}")

    if "plot" in output:
        plt.figure(figsize=(8, 6))
        plt.scatter(y_test, y_pred, alpha=0.6, edgecolors='k')
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        plt.xlabel("Actual")
        plt.ylabel("Predicted")
        plt.title(f"{model} Prediction Plot")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    if "csv" in output:
        df_pred = data.df.copy()
        df_pred["prediction"] = reg.predict(data.X)
        df_pred.to_csv(prediction_csv, index=False)
        print(f"Predictions saved to: {prediction_csv}")

    if "save" in output:
        with open(save_path, "wb") as f:
            pickle.dump(reg, f)
        print(f"Model saved to: {save_path}")

    return {
        "mse": mse,
        "r2": r2,
        "predictions": y_pred,
        "model": reg,
    }
