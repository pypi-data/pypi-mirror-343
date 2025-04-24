"""
Clustering task module for skvai.
"""
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from skvai.core import CSVData


def cluster(
    data: CSVData,
    model: str = "KMeans",
    n_clusters: int = 3,
    output: list = ["labels"],
    save_path: str = "clusterer.pkl",
    labels_csv: str = "labels.csv",
    random_state: int = 42
):
    """
    Fit and apply a clustering model on CSVData.

    Args:
        data (CSVData): Loaded dataset with attribute X and df.
        model (str): Which clusterer: 'KMeans' or 'DBSCAN'.
        n_clusters (int): Number of clusters for KMeans.
        output (list): What to output: 'metrics', 'plot', 'csv', 'save'.
        save_path (str): Path to save the clusterer (.pkl).
        labels_csv (str): Path to save full-data labels (.csv).
        random_state (int): Random seed for reproducibility.

    Returns:
        dict: {'labels', 'model'}
    """
    # Select model
    if model == "KMeans":
        clusterer = KMeans(n_clusters=n_clusters, random_state=random_state)
    elif model == "DBSCAN":
        clusterer = DBSCAN()
    else:
        raise ValueError(f"Model '{model}' not supported.")

    # Train the model
    clusterer.fit(data.X)
    labels = clusterer.labels_

    results = {"labels": labels, "model": clusterer}

    if model == "KMeans" and "metrics" in output:
        print(f"Inertia: {clusterer.inertia_:.4f}")

    if "plot" in output:
        # Only plot when data is 2D
        if data.X.shape[1] == 2:
            X = data.X.to_numpy()
            plt.scatter(X[:, 0], X[:, 1], c=labels)
            plt.title(f"{model} Clustering")
            plt.show()
        else:
            print("Plot unavailable: data not 2D.")

    if "csv" in output:
        df_labels = data.df.copy()
        df_labels["cluster"] = labels
        df_labels.to_csv(labels_csv, index=False)
        print(f"Cluster labels saved to {labels_csv}")

    if "save" in output:
        with open(save_path, "wb") as f:
            pickle.dump(clusterer, f)
        print(f"Clusterer saved to {save_path}")

    return results
