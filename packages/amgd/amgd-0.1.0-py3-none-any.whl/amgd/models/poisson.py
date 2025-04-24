"""
Penalized Poisson regression model using AMGD optimizer.
"""

import numpy as np
from .base import BaseModel
from ..core.optimizer import AMGD
from ..core.utils import poisson_log_likelihood, evaluate_model

class PenalizedPoissonRegression(BaseModel):
    """
    Penalized Poisson Regression model using AMGD for optimization.
    
    This model fits a Poisson regression with L1 or elastic net regularization
    using Adaptive Momentum Gradient Descent.
    
    Parameters:
    -----------
    alpha : float, default=0.001
        Learning rate for AMGD optimizer
    beta1 : float, default=0.8
        Exponential decay rate for first moment in AMGD
    beta2 : float, default=0.999
        Exponential decay rate for second moment in AMGD
    lambda1 : float, default=0.1
        L1 regularization strength
    lambda2 : float, default=0.0
        L2 regularization strength (for elastic net)
    penalty : str, default='l1'
        Type of regularization: 'l1' or 'elasticnet'
    max_iter : int, default=1000
        Maximum number of iterations
    tol : float, default=1e-6
        Convergence tolerance
    T : float, default=20.0
        Gradient clipping threshold
    eta : float, default=0.0001
        Learning rate decay parameter
    verbose : bool, default=False
        Whether to print progress information
    random_state : int, default=None
        Random seed for reproducibility
    """
    
    def __init__(self, alpha=0.001, beta1=0.8, beta2=0.999, 
                 lambda1=0.1, lambda2=0.0, penalty='l1',
                 max_iter=1000, tol=1e-6, T=20.0, eta=0.0001, 
                 verbose=False, random_state=None):
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.penalty = penalty
        self.max_iter = max_iter
        self.tol = tol
        self.T = T
        self.eta = eta
        self.verbose = verbose
        self.random_state = random_state
        
        # Model parameters
        self.coef_ = None
        self.optimizer_results_ = None
        
        # Set random seed if provided
        if random_state is not None:
            np.random.seed(random_state)
    
    def fit(self, X, y):
        """
        Fit the Poisson regression model using AMGD.
        
        Parameters:
        -----------
        X : ndarray, shape (n_samples, n_features)
            Feature matrix
        y : ndarray, shape (n_samples,)
            Target vector
            
        Returns:
        --------
        self : object
            Returns self
        """
        # Create the optimizer
        optimizer = AMGD(
            alpha=self.alpha,
            beta1=self.beta1,
            beta2=self.beta2,
            lambda1=self.lambda1,
            lambda2=self.lambda2,
            penalty=self.penalty,
            T=self.T,
            tol=self.tol,
            max_iter=self.max_iter,
            eta=self.eta,
            verbose=self.verbose,
            return_iters=True
        )
        
        # Fit the model
        optimizer.fit(X, y, objective_fn=poisson_log_likelihood)
        
        # Save the results
        self.coef_ = optimizer.get_params()
        self.optimizer_results_ = optimizer.get_results()
        
        return self
    
    def predict(self, X):
        """
        Predict counts using the fitted Poisson regression model.
        
        Parameters:
        -----------
        X : ndarray, shape (n_samples, n_features)
            Feature matrix
            
        Returns:
        --------
        y_pred : ndarray, shape (n_samples,)
            Predicted counts
        """
        if self.coef_ is None:
            raise ValueError("Model has not been fitted yet. Call 'fit' first.")
        
        linear_pred = X @ self.coef_
        linear_pred = np.clip(linear_pred, -20, 20)  # Prevent numerical overflow
        return np.exp(linear_pred)
    
    def predict_log(self, X):
        """
        Predict log counts using the fitted Poisson regression model.
        
        Parameters:
        -----------
        X : ndarray, shape (n_samples, n_features)
            Feature matrix
            
        Returns:
        --------
        y_pred_log : ndarray, shape (n_samples,)
            Predicted log counts (i.e., the linear predictor)
        """
        if self.coef_ is None:
            raise ValueError("Model has not been fitted yet. Call 'fit' first.")
        
        linear_pred = X @ self.coef_
        return np.clip(linear_pred, -20, 20)  # Prevent numerical overflow
    
    def evaluate(self, X, y):
        """
        Evaluate the model on test data.
        
        Parameters:
        -----------
        X : ndarray, shape (n_samples, n_features)
            Feature matrix
        y : ndarray, shape (n_samples,)
            Target vector
            
        Returns:
        --------
        metrics : dict
            Dictionary of evaluation metrics
        """
        if self.coef_ is None:
            raise ValueError("Model has not been fitted yet. Call 'fit' first.")
        
        return evaluate_model(self.coef_, X, y)
    
    def get_optimization_stats(self):
        """
        Get information about the optimization process.
        
        Returns:
        --------
        dict
            Dictionary with optimization statistics
        """
        if self.optimizer_results_ is None:
            raise ValueError("Model has not been fitted yet. Call 'fit' first.")
        
        return {
            'loss_history': self.optimizer_results_['loss_history'],
            'runtime': self.optimizer_results_['runtime'],
            'nonzero_history': self.optimizer_results_['nonzero_history'],
            'sparsity': 1.0 - (np.sum(np.abs(self.coef_) > 1e-6) / len(self.coef_))
        }