"""Model explanation utilities using SHAP."""
from typing import Any, Optional, Union

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Import SHAP conditionally to make it an optional dependency
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False


def shap_summary(
    model: Any, 
    X: np.ndarray, 
    feature_names: Optional[list[str]] = None,
    max_display: int = 10
) -> Union[Figure, None]:
    """Generate a SHAP summary plot for feature importance visualization.
    
    Parameters
    ----------
    model : Any
        The fitted model to explain
    X : np.ndarray
        The input features used to train the model
    feature_names : Optional[list[str]], optional
        Names of the features, by default None
    max_display : int, optional
        Maximum number of features to display, by default 10
        
    Returns
    -------
    Union[Figure, None]
        Matplotlib figure with the SHAP summary plot, or None if SHAP is not available
    """
    if not SHAP_AVAILABLE:
        print("SHAP not available. Install with 'pip install shap' for model explanations.")
        return None
    
    # Create a sample of data if X is large
    if len(X) > 100:
        np.random.seed(42)
        sample_indices = np.random.choice(len(X), 100, replace=False)
        X_sample = X[sample_indices]
    else:
        X_sample = X
    
    # Create SHAP explainer based on model type
    try:
        if hasattr(model, 'predict_proba'):
            explainer = shap.TreeExplainer(model) if hasattr(model, 'estimators_') else shap.KernelExplainer(model.predict_proba, X_sample)
        else:
            explainer = shap.TreeExplainer(model) if hasattr(model, 'estimators_') else shap.KernelExplainer(model.predict, X_sample)
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(X_sample)
        
        # Handle multi-class output
        if isinstance(shap_values, list) and len(shap_values) > 1:
            shap_values = np.abs(np.array(shap_values)).mean(0)
        
        # Create figure
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        # Plot SHAP values
        shap.summary_plot(
            shap_values, 
            X_sample, 
            feature_names=feature_names,
            max_display=max_display,
            show=False,
            plot_size=(10, 6)
        )
        
        plt.tight_layout()
        return fig
    
    except Exception as e:
        print(f"Error generating SHAP explanation: {e}")
        return None