"""Generate HTML reports with model results and visualizations."""
from __future__ import annotations

import os
import pathlib
from typing import Dict, Any, Optional, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Try to import optional dependencies
try:
    import jinja2
    JINJA_AVAILABLE = True
except ImportError:
    JINJA_AVAILABLE = False


def _create_regression_plots(X: np.ndarray, y: np.ndarray, model: Any, feature_names: Optional[list[str]] = None) -> Dict[str, Figure]:
    """Create standard plots for regression models."""
    figs = {}
    
    # Actual vs Predicted plot
    fig = plt.figure(figsize=(8, 6))
    y_pred = model.predict(X)
    plt.scatter(y, y_pred, alpha=0.5)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs Predicted Values')
    plt.grid(True, alpha=0.3)
    figs['actual_vs_predicted'] = fig
    
    # Residuals plot
    fig = plt.figure(figsize=(8, 6))
    residuals = y - y_pred
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='k', linestyle='--', lw=2)
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residuals Plot')
    plt.grid(True, alpha=0.3)
    figs['residuals'] = fig
    
    # Feature importance if available
    if hasattr(model, 'feature_importances_'):
        fig = plt.figure(figsize=(10, 6))
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # Use feature names if provided, otherwise use indices
        if feature_names is not None:
            names = [feature_names[i] for i in indices]
        else:
            names = [f'Feature {i}' for i in indices]
        
        plt.barh(range(len(indices)), importances[indices])
        plt.yticks(range(len(indices)), names)
        plt.xlabel('Feature Importance')
        plt.title('Feature Importance')
        figs['feature_importance'] = fig
    
    return figs


def _create_classification_plots(X: np.ndarray, y: np.ndarray, model: Any, feature_names: Optional[list[str]] = None) -> Dict[str, Figure]:
    """Create standard plots for classification models."""
    figs = {}
    
    # Feature importance if available
    if hasattr(model, 'feature_importances_'):
        fig = plt.figure(figsize=(10, 6))
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # Use feature names if provided, otherwise use indices
        if feature_names is not None:
            names = [feature_names[i] for i in indices]
        else:
            names = [f'Feature {i}' for i in indices]
        
        plt.barh(range(len(indices)), importances[indices])
        plt.yticks(range(len(indices)), names)
        plt.xlabel('Feature Importance')
        plt.title('Feature Importance')
        figs['feature_importance'] = fig
    
    return figs


def _create_clustering_plots(X: np.ndarray, labels: np.ndarray, feature_names: Optional[list[str]] = None) -> Dict[str, Figure]:
    """Create standard plots for clustering models."""
    figs = {}
    
    # Only create 2D scatter plot if we have 2 or more features
    if X.shape[1] >= 2:
        # Select first two features for visualization
        fig = plt.figure(figsize=(8, 6))
        plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.7)
        
        # Use feature names if provided
        if feature_names is not None and len(feature_names) >= 2:
            plt.xlabel(feature_names[0])
            plt.ylabel(feature_names[1])
        else:
            plt.xlabel('Feature 1')
            plt.ylabel('Feature 2')
            
        plt.title('Cluster Assignments')
        plt.colorbar(label='Cluster')
        figs['cluster_scatter'] = fig
    
    return figs


def _fig_to_base64(fig: Figure) -> str:
    """Convert matplotlib figure to base64 string for embedding in HTML."""
    from io import BytesIO
    import base64
    
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)  # Close the figure to free memory
    return img_str


def save_report(
    result: Dict[str, Any],
    X: np.ndarray,
    y: Optional[np.ndarray] = None,
    task_type: str = 'regression',
    feature_names: Optional[list[str]] = None,
    target_name: Optional[str] = None,
    output_path: Union[str, pathlib.Path] = 'easyml_report.html'
) -> str:
    """Generate and save an HTML report with model results and visualizations.
    
    Parameters
    ----------
    result : Dict[str, Any]
        The result dictionary from one of the fit_* functions
    X : np.ndarray
        The input features
    y : Optional[np.ndarray], optional
        The target values (not needed for clustering), by default None
    task_type : str, optional
        The type of machine learning task, by default 'regression'
    feature_names : Optional[list[str]], optional
        Names of the features, by default None
    target_name : Optional[str], optional
        Name of the target variable, by default None
    output_path : Union[str, pathlib.Path], optional
        Path to save the HTML report, by default 'easyml_report.html'
        
    Returns
    -------
    str
        Path to the saved HTML report
    """
    if not JINJA_AVAILABLE:
        print("Jinja2 not available. Install with 'pip install jinja2' for HTML reports.")
        return ""
    
    # Create output directory if it doesn't exist
    output_path = pathlib.Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get model and metrics
    model = result.get('estimator')
    metrics = result.get('metrics', {})
    
    # Create plots based on task type
    plots = {}
    if task_type == 'regression' and y is not None:
        plots = _create_regression_plots(X, y, model, feature_names)
    elif task_type == 'classification' and y is not None:
        plots = _create_classification_plots(X, y, model, feature_names)
    elif task_type == 'clustering':
        labels = result.get('labels', np.zeros(len(X)))
        plots = _create_clustering_plots(X, labels, feature_names)
    
    # Add SHAP plot if available
    if 'shap_fig' in result and result['shap_fig'] is not None:
        plots['shap'] = result['shap_fig']
    
    # Convert plots to base64 for embedding in HTML
    plot_images = {name: _fig_to_base64(fig) for name, fig in plots.items()}
    
    # Create HTML template
    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EasyML Engineer Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .metrics { margin-bottom: 30px; }
            .metrics table { width: 100%; border-collapse: collapse; }
            .metrics th, .metrics td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            .metrics th { background-color: #f2f2f2; }
            .plots { display: flex; flex-wrap: wrap; justify-content: center; }
            .plot { margin: 10px; text-align: center; }
            .plot img { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>EasyML Engineer Report</h1>
                <p>Task Type: {{ task_type }}</p>
            </div>
            
            <div class="metrics">
                <h2>Model Performance Metrics</h2>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                    {% for name, value in metrics.items() %}
                    <tr>
                        <td>{{ name }}</td>
                        <td>{{ "%.4f"|format(value) }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
            
            <div class="plots">
                {% for name, img_data in plot_images.items() %}
                <div class="plot">
                    <h3>{{ name|replace('_', ' ')|title }}</h3>
                    <img src="data:image/png;base64,{{ img_data }}" alt="{{ name }}">
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    
    # Render template
    template = jinja2.Template(template_str)
    html = template.render(
        task_type=task_type.title(),
        metrics=metrics,
        plot_images=plot_images
    )
    
    # Save HTML report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(output_path)