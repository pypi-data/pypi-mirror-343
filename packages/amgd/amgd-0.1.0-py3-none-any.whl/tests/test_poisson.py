"""
Unit tests for Penalized Poisson Regression model.
"""

import unittest
import numpy as np
from amgd.models.poisson import PenalizedPoissonRegression

class TestPenalizedPoissonRegression(unittest.TestCase):
    """Tests for the PenalizedPoissonRegression model."""
    
    def setUp(self):
        """Set up test data."""
        np.random.seed(42)
        self.n_samples = 100
        self.n_features = 5
        
        # Generate synthetic data
        self.X = np.random.randn(self.n_samples, self.n_features)
        true_coef = np.array([0.5, -0.2, 0.3, 0.0, 0.1])
        linear_pred = self.X @ true_coef
        self.y = np.random.poisson(np.exp(linear_pred))
        
        # Initialize model with test parameters
        self.model = PenalizedPoissonRegression(
            alpha=0.01,
            lambda1=0.1,
            penalty='l1',
            max_iter=100,
            verbose=False,
            random_state=42
        )
    
    def test_fit_predict(self):
        """Test fitting and prediction."""
        # Fit the model
        self.model.fit(self.X, self.y)
        
        # Check that coefficients have been learned
        self.assertIsNotNone(self.model.coef_)
        self.assertEqual(len(self.model.coef_), self.n_features)
        
        # Test prediction
        y_pred = self.model.predict(self.X)
        self.assertEqual(len(y_pred), self.n_samples)
        self.assertTrue(np.all(y_pred >= 0))  # Predictions should be non-negative
    
    def test_predict_log(self):
        """Test log prediction."""
        # Fit the model
        self.model.fit(self.X, self.y)
        
        # Test log prediction
        log_pred = self.model.predict_log(self.X)
        self.assertEqual(len(log_pred), self.n_samples)
        
        # Regular predictions should be exp of log predictions
        y_pred = self.model.predict(self.X)
        np.testing.assert_allclose(y_pred, np.exp(log_pred))
    
    def test_evaluation(self):
        """Test model evaluation."""
        # Fit the model
        self.model.fit(self.X, self.y)
        
        # Evaluate the model
        metrics = self.model.evaluate(self.X, self.y)
        
        # Check that metrics dictionary contains expected keys
        self.assertIn('MAE', metrics)
        self.assertIn('RMSE', metrics)
        self.assertIn('Mean Deviance', metrics)
        self.assertIn('Non-zero coeffs', metrics)
        self.assertIn('Sparsity', metrics)
        
        # Check that metrics have reasonable values
        self.assertGreaterEqual(metrics['MAE'], 0)
        self.assertGreaterEqual(metrics['RMSE'], 0)
        self.assertGreaterEqual(metrics['Non-zero coeffs'], 0)
        self.assertLessEqual(metrics['Non-zero coeffs'], self.n_features)
        self.assertGreaterEqual(metrics['Sparsity'], 0)
        self.assertLessEqual(metrics['Sparsity'], 1)
    
    def test_optimization_stats(self):
        """Test getting optimization statistics."""
        # Fit the model
        self.model.fit(self.X, self.y)
        
        # Get optimization stats
        stats = self.model.get_optimization_stats()
        
        # Check that stats dictionary contains expected keys
        self.assertIn('loss_history', stats)
        self.assertIn('runtime', stats)
        self.assertIn('nonzero_history', stats)
        self.assertIn('sparsity', stats)
        
        # Check that loss history is decreasing
        self.assertGreater(len(stats['loss_history']), 1)
        self.assertLess(stats['loss_history'][-1], stats['loss_history'][0])

if __name__ == "__main__":
    unittest.main()