"""Core fitting functions – thin, explicit and transparent."""
from __future__ import annotations

import pathlib
from typing import Literal, Tuple, Optional, Dict, Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    accuracy_score,
    f1_score,
    silhouette_score,
    davies_bouldin_score,
)
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.cluster import KMeans, Birch
from sklearn.mixture import GaussianMixture

from .explain import shap_summary

# -------------------------------------------------
# Utility helpers
# -------------------------------------------------

def load_csv_or_excel(path: str | pathlib.Path) -> pd.DataFrame:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    if p.suffix.lower() in {".csv"}:
        return pd.read_csv(p)
    if p.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(p)
    raise ValueError("Unsupported file type; need .csv or .xlsx")


def _split_supervised(X: np.ndarray, y: np.ndarray, test_size: float = 0.2):
    return train_test_split(X, y, test_size=test_size, random_state=42)


# -------------------------------------------------
# Regression
# -------------------------------------------------

def fit_regression(
    X: np.ndarray,
    y: np.ndarray,
    model: Literal["random_forest", "knn"] = "random_forest",
    explain: bool = True,
) -> Dict[str, Any]:
    if model == "random_forest":
        clf = RandomForestRegressor(n_estimators=200, random_state=42)
    elif model == "knn":
        clf = KNeighborsRegressor(n_neighbors=5)
    else:
        raise ValueError(model)

    X_train, X_test, y_train, y_test = _split_supervised(X, y)
    y_cv = cross_val_predict(clf, X_train, y_train, cv=5)
    clf.fit(X_train, y_train)

    result = {
        "estimator": clf,
        "metrics": {
            "train_r2": r2_score(y_train, clf.predict(X_train)),
            "cv_r2": r2_score(y_train, y_cv),
            "test_r2": r2_score(y_test, clf.predict(X_test)),
            "test_mae": mean_absolute_error(y_test, clf.predict(X_test)),
        },
    }

    if explain:
        result["shap_fig"] = shap_summary(clf, X_train)
    return result


# -------------------------------------------------
# Classification
# -------------------------------------------------

def fit_classification(
    X: np.ndarray,
    y: np.ndarray,
    model: Literal["random_forest", "knn"] = "random_forest",
    explain: bool = True,
) -> Dict[str, Any]:
    if model == "random_forest":
        clf = RandomForestClassifier(n_estimators=200, random_state=42)
    elif model == "knn":
        clf = KNeighborsClassifier(n_neighbors=5)
    else:
        raise ValueError(model)

    X_train, X_test, y_train, y_test = _split_supervised(X, y)
    y_cv = cross_val_predict(clf, X_train, y_train, cv=5)
    clf.fit(X_train, y_train)

    result = {
        "estimator": clf,
        "metrics": {
            "train_acc": accuracy_score(y_train, clf.predict(X_train)),
            "cv_acc": accuracy_score(y_train, y_cv),
            "test_acc": accuracy_score(y_test, clf.predict(X_test)),
            "test_f1": f1_score(y_test, clf.predict(X_test), average="weighted"),
        },
    }

    if explain:
        result["shap_fig"] = shap_summary(clf, X_train)
    return result


# -------------------------------------------------
# Clustering
# -------------------------------------------------

def fit_clustering(
    X: np.ndarray,
    model: Literal["kmeans", "birch", "gmm"] = "kmeans",
    n_clusters: int = 3,
) -> Dict[str, Any]:
    """Fit a clustering model to the data.
    
    Parameters
    ----------
    X : np.ndarray
        The input features
    model : str, optional
        The clustering algorithm to use, by default "kmeans"
    n_clusters : int, optional
        Number of clusters to find, by default 3
        
    Returns
    -------
    Dict[str, Any]
        Dictionary containing the fitted estimator and evaluation metrics
    """
    if model == "kmeans":
        clf = KMeans(n_clusters=n_clusters, random_state=42)
    elif model == "birch":
        clf = Birch(n_clusters=n_clusters)
    elif model == "gmm":
        clf = GaussianMixture(n_components=n_clusters, random_state=42)
    else:
        raise ValueError(model)

    # Fit the model
    clf.fit(X)
    
    # Get cluster assignments
    if model == "gmm":
        labels = clf.predict(X)
    else:
        labels = clf.labels_
    
    # Calculate metrics if we have enough clusters
    metrics = {}
    if n_clusters > 1 and n_clusters < len(X) - 1:
        try:
            metrics["silhouette"] = silhouette_score(X, labels)
        except:
            metrics["silhouette"] = float('nan')
            
        try:
            metrics["davies_bouldin"] = davies_bouldin_score(X, labels)
        except:
            metrics["davies_bouldin"] = float('nan')
    
    return {
        "estimator": clf,
        "labels": labels,
        "metrics": metrics
    }