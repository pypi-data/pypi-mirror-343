"""
Bootstrap validation techniques for ThinkML.
"""

import numpy as np
from sklearn.base import BaseEstimator, clone
from sklearn.metrics import make_scorer
from sklearn.utils import resample

class BootstrapValidator:
    """Bootstrap validation with out-of-bag error estimation."""
    
    def __init__(self, n_bootstraps=100, random_state=None,
                 scoring='accuracy'):
        """
        Initialize bootstrap validator.
        
        Parameters:
        -----------
        n_bootstraps : int, default=100
            Number of bootstrap samples
        random_state : int or None, default=None
            Random state for reproducibility
        scoring : string, callable, or None, default='accuracy'
            Scoring metric to use
        """
        self.n_bootstraps = n_bootstraps
        self.random_state = random_state
        self.scoring = scoring
        
    def validate(self, estimator, X, y):
        """
        Validate estimator using bootstrap validation.
        
        Parameters:
        -----------
        estimator : estimator object
            Estimator to validate
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target values
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        n_samples = len(X)
        scores = []
        oob_scores = []
        predictions = np.zeros((self.n_bootstraps, n_samples))
        
        rng = np.random.RandomState(self.random_state)
        
        for i in range(self.n_bootstraps):
            # Generate bootstrap sample
            bootstrap_idx = resample(np.arange(n_samples),
                                  replace=True,
                                  n_samples=n_samples,
                                  random_state=rng)
            
            # Get out-of-bag indices
            oob_mask = np.ones(n_samples, dtype=bool)
            oob_mask[bootstrap_idx] = False
            oob_idx = np.arange(n_samples)[oob_mask]
            
            # Get bootstrap and out-of-bag samples
            X_boot = X[bootstrap_idx]
            y_boot = y[bootstrap_idx]
            X_oob = X[oob_idx]
            y_oob = y[oob_idx]
            
            # Fit and evaluate
            estimator_clone = clone(estimator)
            estimator_clone.fit(X_boot, y_boot)
            
            # Score on bootstrap sample
            score = self._score(estimator_clone, X_boot, y_boot)
            scores.append(score)
            
            # Score on out-of-bag sample
            if len(oob_idx) > 0:
                oob_score = self._score(estimator_clone, X_oob, y_oob)
                oob_scores.append(oob_score)
                
            # Store predictions
            predictions[i] = estimator_clone.predict(X)
            
        # Compute final predictions as mode of bootstrap predictions
        final_predictions = np.apply_along_axis(
            lambda x: np.bincount(x.astype(int)).argmax(),
            axis=0,
            arr=predictions
        )
        
        return {
            'scores': np.array(scores),
            'mean_score': np.mean(scores),
            'std_score': np.std(scores),
            'oob_scores': np.array(oob_scores),
            'mean_oob_score': np.mean(oob_scores),
            'std_oob_score': np.std(oob_scores),
            'predictions': final_predictions
        }
        
    def _score(self, estimator, X, y):
        """Compute score for estimator."""
        if callable(self.scoring):
            return self.scoring(estimator, X, y)
        elif isinstance(self.scoring, str):
            scorer = make_scorer(self.scoring)
            return scorer(estimator, X, y)
        else:
            raise ValueError("scoring must be callable or string") 