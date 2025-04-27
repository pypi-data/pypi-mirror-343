from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import HuberRegressor, RANSACRegressor
from typing import Union, Optional
import numpy as np
import pandas as pd

class RobustRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, method: str = 'huber', 
                 epsilon: float = 1.35,
                 max_iter: int = 100,
                 random_state: Optional[int] = None):
        """Initialize the robust regressor.
        
        Args:
            method: Method to use for robust regression ('huber' or 'ransac')
            epsilon: Threshold for Huber regression
            max_iter: Maximum number of iterations
            random_state: Random state for reproducibility
        """
        self.method = method
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.random_state = random_state
        
        if method == 'huber':
            self.estimator = HuberRegressor(
                epsilon=epsilon,
                max_iter=max_iter,
                random_state=random_state
            )
        elif method == 'ransac':
            self.estimator = RANSACRegressor(
                max_iter=max_iter,
                random_state=random_state
            )
        else:
            raise ValueError("Method must be either 'huber' or 'ransac'")
            
    def fit(self, X: Union[pd.DataFrame, np.ndarray], 
            y: Union[pd.Series, np.ndarray]) -> 'RobustRegressor':
        """Fit the robust regressor.
        
        Args:
            X: Training data
            y: Target values
            
        Returns:
            self
        """
        self.estimator.fit(X, y)
        return self
        
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Make predictions.
        
        Args:
            X: Input data
            
        Returns:
            Predicted values
        """
        return self.estimator.predict(X)
        
    def score(self, X: Union[pd.DataFrame, np.ndarray], 
              y: Union[pd.Series, np.ndarray]) -> float:
        """Return the R² score.
        
        Args:
            X: Input data
            y: True values
            
        Returns:
            R² score
        """
        return self.estimator.score(X, y) 