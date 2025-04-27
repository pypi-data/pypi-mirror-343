"""
Cross-validation functionality for machine learning models.
"""

import numpy as np
from typing import Any, Dict, List, Optional, Union, Tuple
from collections import Counter

def _calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate classification metrics without using scikit-learn.
    
    Parameters
    ----------
    y_true : np.ndarray
        True labels
    y_pred : np.ndarray
        Predicted labels
        
    Returns
    -------
    Dict[str, float]
        Dictionary containing metric scores
    """
    # Convert inputs to numpy arrays if they aren't already
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    # Calculate true positives, false positives, false negatives
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    # Calculate metrics
    accuracy = np.mean(y_true == y_pred)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

def _create_folds(y: np.ndarray, n_splits: int, stratify: bool = True) -> List[np.ndarray]:
    """
    Create fold indices for cross-validation.
    
    Parameters
    ----------
    y : np.ndarray
        Target values
    n_splits : int
        Number of folds
    stratify : bool
        Whether to stratify the folds
        
    Returns
    -------
    List[np.ndarray]
        List of fold indices
    """
    n_samples = len(y)
    indices = np.arange(n_samples)
    
    if stratify:
        # Get unique classes and their counts
        classes, counts = np.unique(y, return_counts=True)
        
        # Create stratified folds
        fold_indices = []
        for _ in range(n_splits):
            fold = np.array([], dtype=int)
            for cls, count in zip(classes, counts):
                cls_indices = indices[y == cls]
                # Shuffle class indices
                np.random.shuffle(cls_indices)
                # Take proportional number of samples for this fold
                n_samples_per_fold = count // n_splits
                fold = np.concatenate([fold, cls_indices[:n_samples_per_fold]])
            fold_indices.append(fold)
    else:
        # Simple random split
        np.random.shuffle(indices)
        fold_size = n_samples // n_splits
        fold_indices = [indices[i:i + fold_size] for i in range(0, n_samples, fold_size)]
    
    return fold_indices

def leave_one_out_cv(
    model: Any,
    X: np.ndarray,
    y: np.ndarray,
    scoring: Optional[Union[str, List[str]]] = None
) -> Dict[str, List[float]]:
    """
    Perform Leave-One-Out Cross-Validation.
    
    Parameters
    ----------
    model : Any
        The machine learning model to validate
    X : np.ndarray
        Training data
    y : np.ndarray
        Target values
    scoring : Optional[Union[str, List[str]]], optional
        Metric(s) to compute
        
    Returns
    -------
    Dict[str, List[float]]
        Dictionary containing lists of scores for each metric
    """
    if scoring is None:
        scoring = ['accuracy', 'precision', 'recall', 'f1']
    elif isinstance(scoring, str):
        scoring = [scoring]
        
    n_samples = len(X)
    results = {metric: [] for metric in scoring}
    
    for i in range(n_samples):
        # Create train and test indices
        train_indices = np.concatenate([np.arange(i), np.arange(i + 1, n_samples)])
        test_indices = np.array([i])
        
        # Split data
        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]
        
        # Fit and predict
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        fold_scores = _calculate_metrics(y_test, y_pred)
        for metric in scoring:
            results[metric].append(fold_scores[metric])
            
    return results

def time_series_cv(
    model: Any,
    X: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5,
    scoring: Optional[Union[str, List[str]]] = None
) -> Dict[str, List[float]]:
    """
    Perform Time Series Cross-Validation.
    
    Parameters
    ----------
    model : Any
        The machine learning model to validate
    X : np.ndarray
        Training data
    y : np.ndarray
        Target values
    n_splits : int, optional
        Number of splits
    scoring : Optional[Union[str, List[str]]], optional
        Metric(s) to compute
        
    Returns
    -------
    Dict[str, List[float]]
        Dictionary containing lists of scores for each metric
    """
    if scoring is None:
        scoring = ['accuracy', 'precision', 'recall', 'f1']
    elif isinstance(scoring, str):
        scoring = [scoring]
        
    n_samples = len(X)
    fold_size = n_samples // (n_splits + 1)
    results = {metric: [] for metric in scoring}
    
    for i in range(n_splits):
        # Calculate indices for this fold
        train_end = (i + 1) * fold_size
        test_end = train_end + fold_size
        
        # Split data
        X_train = X[:train_end]
        y_train = y[:train_end]
        X_test = X[train_end:test_end]
        y_test = y[train_end:test_end]
        
        # Fit and predict
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        fold_scores = _calculate_metrics(y_test, y_pred)
        for metric in scoring:
            results[metric].append(fold_scores[metric])
            
    return results

def bootstrap_cv(
    model: Any,
    X: np.ndarray,
    y: np.ndarray,
    n_iterations: int = 100,
    sample_size: Optional[float] = None,
    scoring: Optional[Union[str, List[str]]] = None
) -> Dict[str, List[float]]:
    """
    Perform Bootstrap Cross-Validation.
    
    Parameters
    ----------
    model : Any
        The machine learning model to validate
    X : np.ndarray
        Training data
    y : np.ndarray
        Target values
    n_iterations : int, optional
        Number of bootstrap iterations
    sample_size : Optional[float], optional
        Size of bootstrap samples as a fraction of the dataset
    scoring : Optional[Union[str, List[str]]], optional
        Metric(s) to compute
        
    Returns
    -------
    Dict[str, List[float]]
        Dictionary containing lists of scores for each metric
    """
    if scoring is None:
        scoring = ['accuracy', 'precision', 'recall', 'f1']
    elif isinstance(scoring, str):
        scoring = [scoring]
        
    n_samples = len(X)
    if sample_size is None:
        sample_size = 0.63  # Default bootstrap sample size
        
    n_bootstrap_samples = int(n_samples * sample_size)
    results = {metric: [] for metric in scoring}
    
    for _ in range(n_iterations):
        # Generate bootstrap sample
        indices = np.random.choice(n_samples, size=n_bootstrap_samples, replace=True)
        X_boot = X[indices]
        y_boot = y[indices]
        
        # Get out-of-bag samples
        oob_indices = np.setdiff1d(np.arange(n_samples), indices)
        X_oob = X[oob_indices]
        y_oob = y[oob_indices]
        
        if len(oob_indices) > 0:  # Only evaluate if we have OOB samples
            # Fit and predict
            model.fit(X_boot, y_boot)
            y_pred = model.predict(X_oob)
            
            # Calculate metrics
            fold_scores = _calculate_metrics(y_oob, y_pred)
            for metric in scoring:
                results[metric].append(fold_scores[metric])
                
    return results

def cross_validate(
    model: Any,
    X: np.ndarray,
    y: np.ndarray,
    cv: int = 5,
    scoring: Optional[Union[str, List[str]]] = None,
    random_state: Optional[int] = None,
    stratify: bool = True
) -> Dict[str, List[float]]:
    """
    Perform k-fold cross-validation on a machine learning model.

    Parameters
    ----------
    model : Any
        The machine learning model to validate. Must implement fit() and predict() methods.
    X : np.ndarray
        Training data of shape (n_samples, n_features).
    y : np.ndarray
        Target values of shape (n_samples,).
    cv : int, optional
        Number of folds for cross-validation, by default 5.
    scoring : Optional[Union[str, List[str]]], optional
        Metric(s) to compute. If None, uses ['accuracy', 'precision', 'recall', 'f1'].
        By default None.
    random_state : Optional[int], optional
        Random state for reproducibility, by default None.
    stratify : bool, optional
        Whether to use stratified k-fold cross-validation, by default True.

    Returns
    -------
    Dict[str, List[float]]
        Dictionary containing lists of scores for each metric.
        Each list contains scores for each fold.

    Raises
    ------
    ValueError
        If the input data is invalid or if scoring metrics are not supported.
    """
    if random_state is not None:
        np.random.seed(random_state)
        
    if scoring is None:
        scoring = ['accuracy', 'precision', 'recall', 'f1']
    elif isinstance(scoring, str):
        scoring = [scoring]

    # Validate scoring metrics
    valid_metrics = ['accuracy', 'precision', 'recall', 'f1']
    for metric in scoring:
        if metric not in valid_metrics:
            raise ValueError(f"Unsupported scoring metric: {metric}")

    # Create folds
    fold_indices = _create_folds(y, cv, stratify)
    
    # Initialize results dictionary
    results = {metric: [] for metric in scoring}

    # Perform cross-validation
    for fold_idx in range(cv):
        # Create validation indices for this fold
        val_indices = fold_indices[fold_idx]
        # Create training indices (all folds except current)
        train_indices = np.concatenate([fold_indices[i] for i in range(cv) if i != fold_idx])
        
        # Split data
        X_train, X_val = X[train_indices], X[val_indices]
        y_train, y_val = y[train_indices], y[val_indices]

        # Fit model and make predictions
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        # Calculate scores for each metric
        fold_scores = _calculate_metrics(y_val, y_pred)
        for metric in scoring:
            results[metric].append(fold_scores[metric])

    return results 