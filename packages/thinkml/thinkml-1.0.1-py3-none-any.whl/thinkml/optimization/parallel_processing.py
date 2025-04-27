"""
Parallel processing techniques for ThinkML.
"""

import numpy as np
from sklearn.base import BaseEstimator
from joblib import Parallel, delayed
import multiprocessing

class ParallelProcessor:
    """Parallel processing for model training and inference."""
    
    def __init__(self, n_jobs=None, backend='loky', prefer='processes',
                 require='sharedmem', verbose=0):
        """
        Initialize parallel processor.
        
        Parameters:
        -----------
        n_jobs : int or None, default=None
            Number of jobs to run in parallel. None means using all processors
        backend : str, default='loky'
            Backend to use for parallel processing
        prefer : str, default='processes'
            Soft hint for choosing between processes and threads
        require : str, default='sharedmem'
            Hard constraint for choosing between processes and threads
        verbose : int, default=0
            Verbosity level
        """
        self.n_jobs = n_jobs or multiprocessing.cpu_count()
        self.backend = backend
        self.prefer = prefer
        self.require = require
        self.verbose = verbose
        
    def map(self, func, iterable):
        """
        Apply function to every item of iterable in parallel.
        
        Parameters:
        -----------
        func : callable
            Function to apply to each item
        iterable : iterable
            Items to process
        """
        return Parallel(n_jobs=self.n_jobs,
                      backend=self.backend,
                      prefer=self.prefer,
                      require=self.require,
                      verbose=self.verbose)(
            delayed(func)(item) for item in iterable
        )
        
    def starmap(self, func, iterable):
        """
        Apply function to every tuple of items from iterable in parallel.
        
        Parameters:
        -----------
        func : callable
            Function to apply to each tuple of items
        iterable : iterable
            Tuples of items to process
        """
        return Parallel(n_jobs=self.n_jobs,
                      backend=self.backend,
                      prefer=self.prefer,
                      require=self.require,
                      verbose=self.verbose)(
            delayed(func)(*items) for items in iterable
        )
        
    def batch_process(self, func, data, batch_size=None):
        """
        Process data in parallel batches.
        
        Parameters:
        -----------
        func : callable
            Function to apply to each batch
        data : array-like
            Data to process
        batch_size : int or None, default=None
            Size of each batch. None means automatic batch sizing
        """
        data = np.asarray(data)
        n_samples = len(data)
        
        if batch_size is None:
            batch_size = max(1, n_samples // (self.n_jobs * 4))
            
        batches = [
            data[i:i + batch_size]
            for i in range(0, n_samples, batch_size)
        ]
        
        results = self.map(func, batches)
        
        if isinstance(results[0], np.ndarray):
            return np.concatenate(results)
        return results
        
    def parallel_cross_validate(self, estimator, X, y, cv):
        """
        Perform cross-validation in parallel.
        
        Parameters:
        -----------
        estimator : estimator object
            Estimator to validate
        X : array-like
            Training data
        y : array-like
            Target values
        cv : cross-validation generator
            Cross-validation strategy
        """
        def _fit_and_score(train_idx, test_idx):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            estimator_clone = clone(estimator)
            estimator_clone.fit(X_train, y_train)
            return estimator_clone.score(X_test, y_test)
            
        # Generate train/test splits
        splits = list(cv.split(X, y))
        
        # Process splits in parallel
        scores = self.starmap(_fit_and_score,
                            [(train_idx, test_idx) for train_idx, test_idx in splits])
        
        return np.array(scores)
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass 