"""End-to-end tests for EnginML package.

This module contains tests that verify the package works correctly in real-world scenarios.
It uses the sample data files and runs through complete workflows.
"""
import os
import subprocess
import sys
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
def sample_data_path():
    """Return the path to the sample data file."""
    return os.path.join(os.path.dirname(__file__), "sample_data.csv")


def test_end_to_end_regression(sample_data_path, tmp_path):
    """Test a complete end-to-end regression workflow with sample data."""
    # Load the sample data
    df = load_csv_or_excel(sample_data_path)
    
    # Prepare data
    X = df.drop(columns=["target"]).values
    y = df["target"].values
    feature_names = df.drop(columns=["target"]).columns.tolist()
    
    # Test both model types
    for model_type in ["random_forest", "knn"]:
        # Fit model
        result = fit_regression(X, y, model=model_type)
        
        # Check result structure
        assert "estimator" in result
        assert "metrics" in result
        assert "shap_fig" in result
        
        # Check metrics
        metrics = result["metrics"]
        assert "train_r2" in metrics
        assert "cv_r2" in metrics
        assert "test_r2" in metrics
        assert "test_mae" in metrics
        
        # Generate report
        report_path = os.path.join(tmp_path, f"regression_{model_type}_report.html")
        saved_path = save_report(
            result, X, y,
            task_type="regression",
            feature_names=feature_names,
            output_path=report_path
        )
        
        # Check report was generated
        assert os.path.exists(saved_path)
        assert os.path.getsize(saved_path) > 0


def test_cli_execution(sample_data_path, tmp_path):
    """Test that the CLI can be executed with sample data."""
    # Create output paths
    regression_output = os.path.join(tmp_path, "cli_regression_report.html")
    clustering_output = os.path.join(tmp_path, "cli_clustering_report.html")
    
    # Run regression via CLI
    regression_cmd = [
        sys.executable, "-m", "EnginML.cli",
        sample_data_path,
        "--task", "regression",
        "--target", "target",
        "--model", "random_forest",
        "--output", regression_output,
        "--no-explain"  # Speed up test by skipping SHAP
    ]
    
    regression_result = subprocess.run(regression_cmd, capture_output=True, text=True)
    assert regression_result.returncode == 0, f"CLI regression failed: {regression_result.stderr}"
    assert os.path.exists(regression_output)
    
    # Run clustering via CLI
    clustering_cmd = [
        sys.executable, "-m", "EnginML.cli",
        sample_data_path,
        "--task", "clustering",
        "--n-clusters", "2",
        "--model", "kmeans",
        "--output", clustering_output
    ]
    
    clustering_result = subprocess.run(clustering_cmd, capture_output=True, text=True)
    assert clustering_result.returncode == 0, f"CLI clustering failed: {clustering_result.stderr}"
    assert os.path.exists(clustering_output)


def test_real_world_workflow():
    """Test a complete workflow with a realistic dataset."""
    # Create a more complex synthetic dataset
    np.random.seed(42)
    n_samples = 100
    
    # Create features with some correlation
    X1 = np.random.normal(0, 1, n_samples)
    X2 = X1 * 0.5 + np.random.normal(0, 0.5, n_samples)  # Correlated with X1
    X3 = np.random.normal(0, 1, n_samples)  # Independent
    X4 = X3 * -0.3 + np.random.normal(0, 0.7, n_samples)  # Correlated with X3
    
    # Create target with non-linear relationship
    y = 2 * X1**2 - 1.5 * X2 + 0.5 * X3 * X4 + np.random.normal(0, 0.2, n_samples)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        # Create DataFrame
        df = pd.DataFrame({
            "feature1": X1,
            "feature2": X2,
            "feature3": X3,
            "feature4": X4,
            "target": y
        })
        
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    try:
        # Load data
        df = load_csv_or_excel(tmp_path)
        
        # Prepare data
        X = df.drop(columns=["target"]).values
        y = df["target"].values
        feature_names = df.drop(columns=["target"]).columns.tolist()
        
        # Fit regression model
        result = fit_regression(X, y, model="random_forest")
        
        # Check metrics - should be reasonably good for this dataset
        metrics = result["metrics"]
        assert metrics["test_r2"] > 0.7, "Model performance is lower than expected"
        
        # Check SHAP values
        assert "shap_fig" in result, "SHAP explanation missing"
        
        # Create a temporary file for the report
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as report_file:
            report_path = report_file.name
        
        # Generate report
        saved_path = save_report(
            result, X, y,
            task_type="regression",
            feature_names=feature_names,
            output_path=report_path
        )
        
        # Check report was generated
        assert os.path.exists(saved_path)
        assert os.path.getsize(saved_path) > 0
        
        # Clean up report file
        os.unlink(saved_path)
        
    finally:
        # Clean up data file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)