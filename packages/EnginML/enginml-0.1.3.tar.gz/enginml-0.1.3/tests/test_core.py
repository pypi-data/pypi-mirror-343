"""Unit tests for EnginML core functionality."""
import os
import tempfile
import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import make_regression, make_classification, make_blobs

from EnginML import (
    fit_regression,
    fit_classification,
    fit_clustering,
    load_csv_or_excel,
    save_report
)


# Fixtures for test data
@pytest.fixture
def regression_data():
    """Create synthetic regression data for testing."""
    X, y = make_regression(
        n_samples=100,
        n_features=5,
        n_informative=3,
        random_state=42
    )
    return X, y


@pytest.fixture
def classification_data():
    """Create synthetic classification data for testing."""
    X, y = make_classification(
        n_samples=100,
        n_features=5,
        n_informative=3,
        n_redundant=0,
        n_classes=3,
        random_state=42
    )
    return X, y


@pytest.fixture
def clustering_data():
    """Create synthetic clustering data for testing."""
    X, _ = make_blobs(
        n_samples=100,
        n_features=2,
        centers=3,
        random_state=42
    )
    return X


# Test regression functionality
def test_fit_regression_random_forest(regression_data):
    """Test random forest regression model fitting."""
    X, y = regression_data
    result = fit_regression(X, y, model="random_forest")
    
    # Check that the result contains expected keys
    assert "estimator" in result
    assert "metrics" in result
    
    # Check that metrics contain expected values
    metrics = result["metrics"]
    assert "train_r2" in metrics
    assert "cv_r2" in metrics
    assert "test_r2" in metrics
    assert "test_mae" in metrics
    
    # Check that metrics are within reasonable ranges
    assert 0 <= metrics["test_r2"] <= 1
    assert metrics["test_mae"] >= 0


def test_fit_regression_knn(regression_data):
    """Test KNN regression model fitting."""
    X, y = regression_data
    result = fit_regression(X, y, model="knn")
    
    # Check that the result contains expected keys
    assert "estimator" in result
    assert "metrics" in result
    
    # Check that metrics are within reasonable ranges
    metrics = result["metrics"]
    assert 0 <= metrics["test_r2"] <= 1
    assert metrics["test_mae"] >= 0


# Test classification functionality
def test_fit_classification_random_forest(classification_data):
    """Test random forest classification model fitting."""
    X, y = classification_data
    result = fit_classification(X, y, model="random_forest")
    
    # Check that the result contains expected keys
    assert "estimator" in result
    assert "metrics" in result
    
    # Check that metrics contain expected values
    metrics = result["metrics"]
    assert "train_acc" in metrics
    assert "cv_acc" in metrics
    assert "test_acc" in metrics
    assert "test_f1" in metrics
    
    # Check that metrics are within reasonable ranges
    assert 0 <= metrics["test_acc"] <= 1
    assert 0 <= metrics["test_f1"] <= 1


def test_fit_classification_knn(classification_data):
    """Test KNN classification model fitting."""
    X, y = classification_data
    result = fit_classification(X, y, model="knn")
    
    # Check that the result contains expected keys
    assert "estimator" in result
    assert "metrics" in result
    
    # Check that metrics are within reasonable ranges
    metrics = result["metrics"]
    assert 0 <= metrics["test_acc"] <= 1
    assert 0 <= metrics["test_f1"] <= 1


# Test clustering functionality
def test_fit_clustering_kmeans(clustering_data):
    """Test KMeans clustering model fitting."""
    X = clustering_data
    result = fit_clustering(X, model="kmeans", n_clusters=3)
    
    # Check that the result contains expected keys
    assert "estimator" in result
    assert "labels" in result
    assert "metrics" in result
    
    # Check that metrics contain expected values
    metrics = result["metrics"]
    assert "silhouette" in metrics
    assert "davies_bouldin" in metrics
    
    # Check that labels are as expected
    labels = result["labels"]
    assert len(labels) == len(X)
    assert set(labels) <= {0, 1, 2}  # Should have 3 clusters (0, 1, 2)


def test_fit_clustering_birch(clustering_data):
    """Test Birch clustering model fitting."""
    X = clustering_data
    result = fit_clustering(X, model="birch", n_clusters=3)
    
    # Check that the result contains expected keys
    assert "estimator" in result
    assert "labels" in result
    assert "metrics" in result
    
    # Check that labels are as expected
    labels = result["labels"]
    assert len(labels) == len(X)
    assert set(labels) <= {0, 1, 2}  # Should have 3 clusters (0, 1, 2)


def test_fit_clustering_gmm(clustering_data):
    """Test Gaussian Mixture Model clustering."""
    X = clustering_data
    result = fit_clustering(X, model="gmm", n_clusters=3)
    
    # Check that the result contains expected keys
    assert "estimator" in result
    assert "labels" in result
    assert "metrics" in result
    
    # Check that labels are as expected
    labels = result["labels"]
    assert len(labels) == len(X)
    assert set(labels) <= {0, 1, 2}  # Should have 3 clusters (0, 1, 2)


# Test data loading functionality
def test_load_csv_or_excel():
    """Test loading data from CSV and Excel files."""
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df = pd.DataFrame({
            "feature1": [1, 2, 3, 4, 5],
            "feature2": [5, 4, 3, 2, 1],
            "target": [10, 20, 30, 40, 50]
        })
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    try:
        # Test loading CSV
        loaded_df = load_csv_or_excel(tmp_path)
        assert isinstance(loaded_df, pd.DataFrame)
        assert loaded_df.shape == (5, 3)
        assert list(loaded_df.columns) == ["feature1", "feature2", "target"]
    finally:
        # Clean up
        os.unlink(tmp_path)


# Test report generation
def test_save_report(regression_data, tmp_path):
    """Test saving a report to HTML."""
    X, y = regression_data
    result = fit_regression(X, y, model="random_forest")
    
    # Create a temporary file path for the report
    report_path = os.path.join(tmp_path, "test_report.html")
    
    # Save the report
    saved_path = save_report(
        result, X, y,
        task_type="regression",
        feature_names=[f"feature_{i}" for i in range(X.shape[1])],
        output_path=report_path
    )
    
    # Check that the report was saved
    assert os.path.exists(saved_path)
    assert os.path.getsize(saved_path) > 0