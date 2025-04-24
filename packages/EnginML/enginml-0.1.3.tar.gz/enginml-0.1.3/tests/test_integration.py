"""Integration tests for EnginML package."""
import os
import tempfile
import numpy as np
import pandas as pd
import pytest

from EnginML import (
    load_csv_or_excel,
    fit_regression,
    fit_classification,
    fit_clustering,
    save_report
)


@pytest.fixture
def sample_regression_data_file():
    """Create a temporary CSV file with regression data for testing."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        # Create synthetic data
        np.random.seed(42)
        n_samples = 50
        X1 = np.random.rand(n_samples)
        X2 = np.random.rand(n_samples)
        X3 = np.random.rand(n_samples)
        
        # Create target with some noise
        y = 3*X1 - 2*X2 + 0.5*X3 + np.random.normal(0, 0.1, n_samples)
        
        # Create DataFrame
        df = pd.DataFrame({
            "feature1": X1,
            "feature2": X2,
            "feature3": X3,
            "target": y
        })
        
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Clean up
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


@pytest.fixture
def sample_classification_data_file():
    """Create a temporary CSV file with classification data for testing."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        # Create synthetic data
        np.random.seed(42)
        n_samples = 60
        
        # Create two clusters
        X1_class0 = np.random.normal(0, 1, n_samples // 3)
        X2_class0 = np.random.normal(0, 1, n_samples // 3)
        
        X1_class1 = np.random.normal(3, 1, n_samples // 3)
        X2_class1 = np.random.normal(3, 1, n_samples // 3)
        
        X1_class2 = np.random.normal(0, 1, n_samples // 3)
        X2_class2 = np.random.normal(3, 1, n_samples // 3)
        
        # Combine features
        X1 = np.concatenate([X1_class0, X1_class1, X1_class2])
        X2 = np.concatenate([X2_class0, X2_class1, X2_class2])
        
        # Create labels
        y = np.array([0] * (n_samples // 3) + [1] * (n_samples // 3) + [2] * (n_samples // 3))
        
        # Create DataFrame
        df = pd.DataFrame({
            "feature1": X1,
            "feature2": X2,
            "target": y
        })
        
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Clean up
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


@pytest.fixture
def sample_clustering_data_file():
    """Create a temporary CSV file with clustering data for testing."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        # Create synthetic data
        np.random.seed(42)
        n_samples_per_cluster = 20
        
        # Create three clusters
        X1_cluster1 = np.random.normal(0, 0.5, n_samples_per_cluster)
        X2_cluster1 = np.random.normal(0, 0.5, n_samples_per_cluster)
        
        X1_cluster2 = np.random.normal(4, 0.5, n_samples_per_cluster)
        X2_cluster2 = np.random.normal(0, 0.5, n_samples_per_cluster)
        
        X1_cluster3 = np.random.normal(2, 0.5, n_samples_per_cluster)
        X2_cluster3 = np.random.normal(4, 0.5, n_samples_per_cluster)
        
        # Combine features
        X1 = np.concatenate([X1_cluster1, X1_cluster2, X1_cluster3])
        X2 = np.concatenate([X2_cluster1, X2_cluster2, X2_cluster3])
        
        # Create DataFrame
        df = pd.DataFrame({
            "feature1": X1,
            "feature2": X2
        })
        
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Clean up
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


def test_regression_workflow(sample_regression_data_file, tmp_path):
    """Test the complete regression workflow from data loading to report generation."""
    # Load data
    df = load_csv_or_excel(sample_regression_data_file)
    
    # Prepare data
    X = df.drop(columns=["target"]).values
    y = df["target"].values
    feature_names = df.drop(columns=["target"]).columns.tolist()
    
    # Fit model
    result = fit_regression(X, y, model="random_forest")
    
    # Check result structure
    assert "estimator" in result
    assert "metrics" in result
    
    # Generate report
    report_path = os.path.join(tmp_path, "regression_report.html")
    saved_path = save_report(
        result, X, y,
        task_type="regression",
        feature_names=feature_names,
        output_path=report_path
    )
    
    # Check report was generated
    assert os.path.exists(saved_path)
    assert os.path.getsize(saved_path) > 0


def test_classification_workflow(sample_classification_data_file, tmp_path):
    """Test the complete classification workflow from data loading to report generation."""
    # Load data
    df = load_csv_or_excel(sample_classification_data_file)
    
    # Prepare data
    X = df.drop(columns=["target"]).values
    y = df["target"].values
    feature_names = df.drop(columns=["target"]).columns.tolist()
    
    # Fit model
    result = fit_classification(X, y, model="random_forest")
    
    # Check result structure
    assert "estimator" in result
    assert "metrics" in result
    
    # Generate report
    report_path = os.path.join(tmp_path, "classification_report.html")
    saved_path = save_report(
        result, X, y,
        task_type="classification",
        feature_names=feature_names,
        output_path=report_path
    )
    
    # Check report was generated
    assert os.path.exists(saved_path)
    assert os.path.getsize(saved_path) > 0


def test_clustering_workflow(sample_clustering_data_file, tmp_path):
    """Test the complete clustering workflow from data loading to report generation."""
    # Load data
    df = load_csv_or_excel(sample_clustering_data_file)
    
    # Prepare data
    X = df.values
    feature_names = df.columns.tolist()
    
    # Fit model
    result = fit_clustering(X, model="kmeans", n_clusters=3)
    
    # Check result structure
    assert "estimator" in result
    assert "labels" in result
    assert "metrics" in result
    
    # Generate report
    report_path = os.path.join(tmp_path, "clustering_report.html")
    saved_path = save_report(
        result, X,
        task_type="clustering",
        feature_names=feature_names,
        output_path=report_path
    )
    
    # Check report was generated
    assert os.path.exists(saved_path)
    assert os.path.getsize(saved_path) > 0