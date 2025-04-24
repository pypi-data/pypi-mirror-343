"""
AMGD: Adaptive Momentum Gradient Descent for Penalized Poisson Regression.

A Python package implementing the Adaptive Momentum Gradient Descent optimizer
for Poisson regression with L1 and elastic net regularization.
"""

from amgd.core.optimizer import AMGD
from amgd.models.poisson import PenalizedPoissonRegression

__version__ = "0.1.0"


