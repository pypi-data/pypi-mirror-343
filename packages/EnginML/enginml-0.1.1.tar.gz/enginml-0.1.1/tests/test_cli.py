"""Unit tests for EnginML CLI functionality."""
import os
import tempfile
import pandas as pd
import pytest
from unittest.mock import patch

from EnginML.cli import main


@pytest.fixture
def sample_data_file():
    """Create a temporary CSV file with sample data for testing."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df = pd.DataFrame({
            "feature1": [1, 2, 3, 4, 5],
            "feature2": [5, 4, 3, 2, 1],
            "target": [10, 20, 30, 40, 50]
        })
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Clean up
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


@pytest.fixture
def sample_classification_file():
    """Create a temporary CSV file with classification data for testing."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        df = pd.DataFrame({
            "feature1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "feature2": [5, 4, 3, 2, 1, 5, 4, 3, 2, 1],
            "target": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        })
        df.to_csv(tmp.name, index=False)
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Clean up
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


# Test CLI regression functionality
@patch('sys.argv')
def test_cli_regression(mock_argv, sample_data_file, tmp_path):
    """Test CLI regression functionality."""
    output_path = os.path.join(tmp_path, "regression_report.html")
    
    # Set up command line arguments
    mock_argv.__getitem__.side_effect = [
        "enginml",
        sample_data_file,
        "--task", "regression",
        "--target", "target",
        "--model", "random_forest",
        "--output", output_path
    ].__getitem__
    
    # Run the CLI
    with patch('EnginML.cli.argparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = type('Args', (), {
            'file': sample_data_file,
            'task': 'regression',
            'target': 'target',
            'model': 'random_forest',
            'output': output_path,
            'no_explain': True,
            'n_clusters': 3
        })
        
        result = main()
        
        # Check that the function completed successfully
        assert result == 0
        
        # Check that the output file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0


# Test CLI classification functionality
@patch('sys.argv')
def test_cli_classification(mock_argv, sample_classification_file, tmp_path):
    """Test CLI classification functionality."""
    output_path = os.path.join(tmp_path, "classification_report.html")
    
    # Set up command line arguments
    mock_argv.__getitem__.side_effect = [
        "enginml",
        sample_classification_file,
        "--task", "classification",
        "--target", "target",
        "--model", "random_forest",
        "--output", output_path
    ].__getitem__
    
    # Run the CLI
    with patch('EnginML.cli.argparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = type('Args', (), {
            'file': sample_classification_file,
            'task': 'classification',
            'target': 'target',
            'model': 'random_forest',
            'output': output_path,
            'no_explain': True,
            'n_clusters': 3
        })
        
        result = main()
        
        # Check that the function completed successfully
        assert result == 0
        
        # Check that the output file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0


# Test CLI clustering functionality
@patch('sys.argv')
def test_cli_clustering(mock_argv, sample_data_file, tmp_path):
    """Test CLI clustering functionality."""
    output_path = os.path.join(tmp_path, "clustering_report.html")
    
    # Set up command line arguments
    mock_argv.__getitem__.side_effect = [
        "enginml",
        sample_data_file,
        "--task", "clustering",
        "--n-clusters", "2",
        "--model", "kmeans",
        "--output", output_path
    ].__getitem__
    
    # Run the CLI
    with patch('EnginML.cli.argparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = type('Args', (), {
            'file': sample_data_file,
            'task': 'clustering',
            'target': None,
            'model': 'kmeans',
            'output': output_path,
            'no_explain': True,
            'n_clusters': 2
        })
        
        result = main()
        
        # Check that the function completed successfully
        assert result == 0
        
        # Check that the output file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0


# Test CLI error handling
@patch('sys.argv')
def test_cli_missing_target(mock_argv, sample_data_file):
    """Test CLI error handling for missing target."""
    # Set up command line arguments
    mock_argv.__getitem__.side_effect = [
        "enginml",
        sample_data_file,
        "--task", "regression",
        "--model", "random_forest"
    ].__getitem__
    
    # Run the CLI
    with patch('EnginML.cli.argparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = type('Args', (), {
            'file': sample_data_file,
            'task': 'regression',
            'target': None,
            'model': 'random_forest',
            'output': 'report.html',
            'no_explain': False,
            'n_clusters': 3
        })
        
        result = main()
        
        # Check that the function returned an error code
        assert result == 1


@patch('sys.argv')
def test_cli_invalid_model(mock_argv, sample_data_file):
    """Test CLI error handling for invalid model."""
    # Set up command line arguments
    mock_argv.__getitem__.side_effect = [
        "enginml",
        sample_data_file,
        "--task", "regression",
        "--target", "target",
        "--model", "invalid_model"
    ].__getitem__
    
    # Run the CLI
    with patch('EnginML.cli.argparse.ArgumentParser.parse_args') as mock_parse_args:
        mock_parse_args.return_value = type('Args', (), {
            'file': sample_data_file,
            'task': 'regression',
            'target': 'target',
            'model': 'invalid_model',
            'output': 'report.html',
            'no_explain': False,
            'n_clusters': 3
        })
        
        result = main()
        
        # Check that the function returned an error code
        assert result == 1