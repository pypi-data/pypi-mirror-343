"""
Adaptive Momentum Gradient Descent (AMGD) optimizer implementation.
"""

import numpy as np
import time
from .utils import clip, poisson_log_likelihood

class AMGD:
    """
    Adaptive Momentum Gradient Descent (AMGD) optimizer for Poisson regression
    with L1 or Elastic Net regularization.
    
    Parameters:
    -----------
    alpha : float, default=0.001
        Initial learning rate
    beta1 : float, default=0.8
        Exponential decay rate for the first moment estimates
    beta2 : float, default=0.999
        Exponential decay rate for the second moment estimates
    lambda1 : float, default=0.1
        L1 regularization strength
    lambda2 : float, default=0.0
        L2 regularization strength (used only with elastic net)
    penalty : str, default='l1'
        Penalty type. Can be 'l1' or 'elasticnet'
    T : float, default=20.0
        Gradient clipping threshold
    tol : float, default=1e-6
        Tolerance for convergence
    max_iter : int, default=1000
        Maximum number of iterations
    eta : float, default=0.0001
        Learning rate decay parameter
    epsilon : float, default=1e-8
        Small constant for numerical stability
    verbose : bool, default=False
        Whether to print progress information
    return_iters : bool, default=False
        Whether to return beta values at each iteration
    """
    
    def __init__(self, alpha=0.001, beta1=0.8, beta2=0.999, 
                 lambda1=0.1, lambda2=0.0, penalty='l1',
                 T=20.0, tol=1e-6, max_iter=1000, eta=0.0001, 
                 epsilon=1e-8, verbose=False, return_iters=False):
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.penalty = penalty
        self.T = T
        self.tol = tol
        self.max_iter = max_iter
        self.eta = eta
        self.epsilon = epsilon
        self.verbose = verbose
        self.return_iters = return_iters
        
        # State variables
        self.m = None
        self.v = None
        self.beta = None
        self.t = 0
        self.loss_history = []
        self.nonzero_history = []
        self.beta_history = []
        self.runtime = None
        
    def fit(self, X, y, objective_fn=None):
        """
        Fit the model to the data using AMGD.
        
        Parameters:
        -----------
        X : ndarray, shape (n_samples, n_features)
            Feature matrix
        y : ndarray, shape (n_samples,)
            Target vector
        objective_fn : function, default=None
            Custom objective function. If None, uses Poisson log-likelihood
            
        Returns:
        --------
        self : object
            Returns self with fitted coefficients
        """
        if objective_fn is None:
            objective_fn = poisson_log_likelihood
            
        n_samples, n_features = X.shape
        
        # Initializing coefficient vector
        self.beta = np.random.normal(0, 0.1, n_features)
        
        # Initializing momentum variables
        self.m = np.zeros(n_features)
        self.v = np.zeros(n_features)
        
        prev_loss = float('inf')
        self.loss_history = []
        self.nonzero_history = []
        self.beta_history = []
        start_time = time.time()
        self.t = 0
        
        for t in range(1, self.max_iter + 1):
            self.t = t
            alpha_t = self.alpha / (1 + self.eta * t)
            
            # Computing predictions and gradient
            linear_pred = X @ self.beta
            linear_pred = np.clip(linear_pred, -20, 20)
            mu = np.exp(linear_pred)
            
            # Gradient of negative log-likelihood
            grad_ll = X.T @ (mu - y)
            
            # Adding regularization gradient
            if self.penalty == 'l1':
                # Pure L1: no gradient term (handled in soft thresholding step)
                grad = grad_ll
            elif self.penalty == 'elasticnet':
                # Elastic Net: add gradient of L2 component
                grad = grad_ll + self.lambda2 * self.beta
            else:
                raise ValueError(f"Unknown penalty: {self.penalty}")
            
            grad = clip(grad, self.T)
            
            # Update the parameters
            self._update_params(grad)
            
            # Compute loss
            ll = objective_fn(self.beta, X, y)
            
            # Add regularization component to loss
            reg_pen = self._compute_regularization()
            
            total_loss = ll + reg_pen
            self.loss_history.append(total_loss)
            
            # Tracking non-zero coefficients
            non_zeros = np.sum(np.abs(self.beta) > 1e-6)
            self.nonzero_history.append(non_zeros)
            
            # Tracking beta values 
            if self.return_iters:
                self.beta_history.append(self.beta.copy())
            
            if self.verbose and t % 100 == 0:
                print(f"Iteration {t}, Loss: {total_loss:.4f}, Log-likelihood: {ll:.4f}, Penalty: {reg_pen:.4f}")
                print(f"Non-zero coefficients: {non_zeros}/{n_features}, Sparsity: {1-non_zeros/n_features:.4f}")
            
            # Checking convergence
            if abs(prev_loss - total_loss) < self.tol:
                if self.verbose:
                    print(f"Converged at iteration {t}")
                break
                
            prev_loss = total_loss
        
        self.runtime = time.time() - start_time
        return self
    
    def _update_params(self, grad):
        """Update parameters using AMGD update rule."""
        # Momentum updates
        self.m = self.beta1 * self.m + (1 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grad ** 2)
        
        # Bias correction
        m_hat = self.m / (1 - self.beta1 ** self.t)
        v_hat = self.v / (1 - self.beta2 ** self.t)
        
        # Parameter update
        alpha_t = self.alpha / (1 + self.eta * self.t)
        self.beta = self.beta - alpha_t * m_hat / (np.sqrt(v_hat) + self.epsilon)
        
        # Apply appropriate regularization
        if self.penalty == 'l1' or self.penalty == 'elasticnet':
            # Adaptive soft-thresholding for L1 component
            denom = np.abs(self.beta) + 0.1
            self.beta = np.sign(self.beta) * np.maximum(np.abs(self.beta) - alpha_t * self.lambda1 / denom, 0)
    
    def _compute_regularization(self):
        """Compute the regularization penalty."""
        if self.penalty == 'l1':
            return self.lambda1 * np.sum(np.abs(self.beta))
        elif self.penalty == 'elasticnet':
            return self.lambda1 * np.sum(np.abs(self.beta)) + (self.lambda2 / 2) * np.sum(self.beta**2)
        else:
            return 0.0
    
    def get_params(self):
        """Return the fitted parameters."""
        return self.beta
    
    def get_results(self):
        """Return the optimization results."""
        results = {
            'coefficients': self.beta,
            'loss_history': self.loss_history,
            'runtime': self.runtime,
            'nonzero_history': self.nonzero_history
        }
        
        if self.return_iters:
            results['beta_history'] = self.beta_history
            
        return results