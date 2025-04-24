"""
Utility functions for AMGD optimization and model evaluation.
"""

import numpy as np
from scipy import special

def clip(x, threshold=None):
    """
    Clip values to within a specified threshold.
    
    Parameters:
    -----------
    x : ndarray
        Values to clip
    threshold : float, default=None
        Threshold value. If None, no clipping is applied.
        
    Returns:
    --------
    ndarray
        Clipped values
    """
    if threshold is None:
        return x
    return np.clip(x, -threshold, threshold)

def poisson_log_likelihood(beta, X, y):
    """
    Calculate the negative Poisson log-likelihood.
    
    Parameters:
    -----------
    beta : ndarray
        Coefficient vector
    X : ndarray
        Feature matrix
    y : ndarray
        Target vector
        
    Returns:
    --------
    float
        Negative Poisson log-likelihood
    """
    linear_pred = X @ beta
    linear_pred = np.clip(linear_pred, -20, 20)  # Prevent numerical overflow
    mu = np.exp(linear_pred)
    
    log_likelihood = np.sum(y * linear_pred - mu - special.gammaln(y + 1))
    
    return -log_likelihood  # Negative because we want to minimize the function

def evaluate_model(beta, X, y):
    """
    Evaluate model performance using various metrics.
    
    Parameters:
    -----------
    beta : ndarray
        Coefficient vector
    X : ndarray
        Feature matrix
    y : ndarray
        Target vector
        
    Returns:
    --------
    dict
        Dictionary of evaluation metrics
    """
    linear_pred = X @ beta
    linear_pred = np.clip(linear_pred, -20, 20)
    y_pred = np.exp(linear_pred)
    
    # Mean Absolute Error
    mae = np.mean(np.abs(y - y_pred))
    
    # Root Mean Squared Error
    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    
    # Mean Poisson Deviance
    eps = 1e-10  # To avoid log(0)
    deviance = 2 * np.sum(y * np.log((y + eps) / (y_pred + eps)) - (y - y_pred))
    mean_deviance = deviance / len(y)
    
    # Coefficient analysis
    results = {
        'MAE': mae,
        'RMSE': rmse,
        'Mean Deviance': mean_deviance,
        'Non-zero coeffs': np.sum(np.abs(beta) > 1e-6),
        'Sparsity': 1.0 - (np.sum(np.abs(beta) > 1e-6) / len(beta))
    }
    
    return results