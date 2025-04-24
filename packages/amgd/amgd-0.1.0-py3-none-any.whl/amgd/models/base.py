"""
Base model class for AMGD implementations.
"""

from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Abstract base class for models that can be optimized with AMGD.
    """
    
    @abstractmethod
    def fit(self, X, y):
        """
        Fit the model to the data.
        
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
        pass
        
    @abstractmethod
    def predict(self, X):
        """
        Make predictions using the fitted model.
        
        Parameters:
        -----------
        X : ndarray, shape (n_samples, n_features)
            Feature matrix
            
        Returns:
        --------
        y_pred : ndarray, shape (n_samples,)
            Predicted values
        """
        pass
    
    @abstractmethod
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
        pass