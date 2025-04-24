"""Command-line interface for EnginML."""
import argparse
import pathlib
from typing import Optional

import numpy as np
import pandas as pd

from . import fit_regression, fit_classification, fit_clustering, load_csv_or_excel, save_report


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="EnginML - Simple ML workflows for engineers and data scientists"
    )
    
    parser.add_argument(
        "file", 
        type=str,
        help="Path to CSV or Excel file containing the data"
    )
    
    parser.add_argument(
        "--task", 
        type=str, 
        choices=["regression", "classification", "clustering"],
        default="regression",
        help="Type of machine learning task to perform"
    )
    
    parser.add_argument(
        "--model", 
        type=str,
        help="Model to use (regression: random_forest, knn; classification: random_forest, knn; clustering: kmeans, birch, gmm)"
    )
    
    parser.add_argument(
        "--target", 
        type=str,
        help="Name of the target column (not needed for clustering)"
    )
    
    parser.add_argument(
        "--n-clusters", 
        type=int, 
        default=3,
        help="Number of clusters for clustering tasks"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="enginml_report_v2.html",
        help="Path to save the HTML report"
    )
    
    parser.add_argument(
        "--no-explain", 
        action="store_true",
        help="Disable SHAP explanations"
    )
    
    args = parser.parse_args()
    
    # Load data
    try:
        df = load_csv_or_excel(args.file)
        print(f"Loaded data with {df.shape[0]} rows and {df.shape[1]} columns")
    except Exception as e:
        print(f"Error loading data: {e}")
        return 1
    
    # Prepare data
    if args.task in ["regression", "classification"] and args.target is None:
        print(f"Error: --target is required for {args.task} tasks")
        return 1
    
    # For clustering, all columns are features
    if args.task == "clustering":
        X = df.values
        y = None
        feature_names = df.columns.tolist()
        target_name = None
    else:
        # For supervised learning, separate features and target
        if args.target not in df.columns:
            print(f"Error: Target column '{args.target}' not found in data")
            return 1
        
        y = df[args.target].values
        X = df.drop(columns=[args.target]).values
        feature_names = df.drop(columns=[args.target]).columns.tolist()
        target_name = args.target
    
    # Set default model based on task
    model = args.model
    if model is None:
        if args.task == "regression":
            model = "random_forest"
        elif args.task == "classification":
            model = "random_forest"
        elif args.task == "clustering":
            model = "kmeans"
    
    # Validate model choice
    valid_models = {
        "regression": ["random_forest", "knn"],
        "classification": ["random_forest", "knn"],
        "clustering": ["kmeans", "birch", "gmm"]
    }
    
    if model not in valid_models[args.task]:
        print(f"Error: Invalid model '{model}' for {args.task}. Valid options are: {', '.join(valid_models[args.task])}")
        return 1
    
    # Fit model based on task
    try:
        print(f"Fitting {model} model for {args.task}...")
        
        if args.task == "regression":
            result = fit_regression(X, y, model=model, explain=not args.no_explain)
        elif args.task == "classification":
            result = fit_classification(X, y, model=model, explain=not args.no_explain)
        elif args.task == "clustering":
            result = fit_clustering(X, model=model, n_clusters=args.n_clusters)
        
        # Print metrics
        print("\nModel Performance:")
        for name, value in result["metrics"].items():
            print(f"  {name}: {value:.4f}")
        
        # Generate report
        report_path = save_report(
            result, 
            X, 
            y, 
            task_type=args.task,
            feature_names=feature_names,
            target_name=target_name,
            output_path=args.output
        )
        
        if report_path:
            print(f"\nReport saved to: {report_path}")
        
    except Exception as e:
        print(f"Error during model fitting: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())