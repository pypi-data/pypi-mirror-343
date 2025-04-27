"""
Outlier detection functions for ThinkML.

This module provides functions for detecting outliers in datasets using various methods
including Z-score, IQR, and Isolation Forest.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Union, Optional, Tuple
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats


class IsolationForest:
    """
    A simple implementation of Isolation Forest for outlier detection.
    
    This is a simplified version of the Isolation Forest algorithm that
    uses random subspaces and random splits to isolate outliers.
    """
    
    def __init__(self, n_estimators=100, max_samples='auto', contamination=0.1, random_state=None):
        """
        Initialize the Isolation Forest.
        
        Args:
            n_estimators: Number of trees in the forest
            max_samples: Number of samples to draw to train each tree
            contamination: Expected proportion of outliers in the data
            random_state: Random seed for reproducibility
        """
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.contamination = contamination
        self.random_state = random_state
        self.trees = []
        
        if random_state is not None:
            np.random.seed(random_state)
    
    def fit(self, X):
        """
        Fit the Isolation Forest to the data.
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            self: The fitted model
        """
        # Convert to numpy array if needed
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        n_samples, n_features = X.shape
        
        # Set max_samples if 'auto'
        if self.max_samples == 'auto':
            self.max_samples = min(256, n_samples)
        
        # Create trees
        self.trees = []
        for _ in range(self.n_estimators):
            # Sample data points
            if self.max_samples < n_samples:
                indices = np.random.choice(n_samples, self.max_samples, replace=False)
                X_sample = X[indices]
            else:
                X_sample = X
            
            # Create a tree
            tree = self._create_tree(X_sample, 0, n_features)
            self.trees.append(tree)
        
        return self
    
    def predict(self, X):
        """
        Predict outlier labels for samples in X.
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            Array of shape (n_samples,) with -1 for outliers and 1 for inliers
        """
        # Convert to numpy array if needed
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        # Calculate anomaly scores
        scores = self.score_samples(X)
        
        # Determine threshold based on contamination
        threshold = np.percentile(scores, 100 * (1 - self.contamination))
        
        # Predict labels
        labels = np.ones(X.shape[0])
        labels[scores > threshold] = -1
        
        return labels
    
    def score_samples(self, X):
        """
        Calculate anomaly scores for samples in X.
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            Array of shape (n_samples,) with anomaly scores
        """
        # Convert to numpy array if needed
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        n_samples = X.shape[0]
        scores = np.zeros(n_samples)
        
        # Calculate average path length for each sample
        for tree in self.trees:
            scores += self._path_length(X, tree)
        
        scores /= self.n_estimators
        
        # Convert to anomaly scores
        # The formula is: -2^(-avg_path_length / c(n_samples))
        # where c(n) is the average path length of an unsuccessful search in a binary search tree
        c = 2 * (np.log(n_samples - 1) + 0.5772156649) - 2 * (n_samples - 1) / n_samples
        scores = -2 ** (-scores / c)
        
        return scores
    
    def _create_tree(self, X, depth, n_features, max_depth=10):
        """
        Create a random tree for isolation.
        
        Args:
            X: Input data
            depth: Current depth in the tree
            n_features: Number of features
            max_depth: Maximum depth of the tree
            
        Returns:
            A tree node or leaf
        """
        n_samples = X.shape[0]
        
        # Stop if we've reached max depth or have too few samples
        if depth >= max_depth or n_samples <= 1:
            return {'type': 'leaf', 'size': n_samples}
        
        # Randomly select a feature and split point
        feature_idx = np.random.randint(0, n_features)
        feature_values = X[:, feature_idx]
        
        # Skip if all values are the same
        if np.all(feature_values == feature_values[0]):
            return {'type': 'leaf', 'size': n_samples}
        
        # Find a random split point
        min_val, max_val = np.min(feature_values), np.max(feature_values)
        split_val = np.random.uniform(min_val, max_val)
        
        # Split the data
        left_mask = feature_values <= split_val
        right_mask = ~left_mask
        
        # Skip if split doesn't divide the data
        if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
            return {'type': 'leaf', 'size': n_samples}
        
        # Create child nodes
        left_child = self._create_tree(X[left_mask], depth + 1, n_features, max_depth)
        right_child = self._create_tree(X[right_mask], depth + 1, n_features, max_depth)
        
        return {
            'type': 'node',
            'feature': feature_idx,
            'threshold': split_val,
            'left': left_child,
            'right': right_child
        }
    
    def _path_length(self, X, tree):
        """
        Calculate the path length for each sample in X.
        
        Args:
            X: Input data
            tree: A tree node
            
        Returns:
            Array of path lengths
        """
        n_samples = X.shape[0]
        path_lengths = np.zeros(n_samples)
        
        for i in range(n_samples):
            path_lengths[i] = self._path_length_sample(X[i], tree)
        
        return path_lengths
    
    def _path_length_sample(self, x, tree):
        """
        Calculate the path length for a single sample.
        
        Args:
            x: A single sample
            tree: A tree node
            
        Returns:
            Path length
        """
        if tree['type'] == 'leaf':
            # Adjust path length for leaf nodes
            return self._c(tree['size'])
        
        # Traverse the tree
        if x[tree['feature']] <= tree['threshold']:
            return 1 + self._path_length_sample(x, tree['left'])
        else:
            return 1 + self._path_length_sample(x, tree['right'])
    
    def _c(self, n):
        """
        Calculate the average path length of an unsuccessful search in a binary search tree.
        
        Args:
            n: Number of samples
            
        Returns:
            Average path length
        """
        if n <= 1:
            return 0
        elif n == 2:
            return 1
        else:
            return 2 * (np.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n


def detect_outliers(
    X: pd.DataFrame,
    method: str = 'zscore',
    threshold: float = 3.0,
    contamination: Optional[float] = None,
    report: bool = True,
    visualize: bool = True,
    chunk_size: int = 100000,
    return_mask: bool = True
) -> Union[pd.DataFrame, Dict]:
    """
    Detect outliers in a dataset using various methods.

    Args:
        X: Input features DataFrame (numerical features only).
        method: Method for outlier detection. Options:
            - 'zscore': Identify outliers with |z| > threshold
            - 'iqr': Identify outliers outside Q1 - threshold*IQR and Q3 + threshold*IQR
            - 'isolation_forest': Use Isolation Forest to detect outliers
        threshold: Threshold for outlier detection. For z-score: number of standard deviations.
                  For IQR: multiplier for IQR. Default is 3.0.
        contamination: Contamination parameter for isolation_forest method.
                      If None and method is 'isolation_forest', uses threshold value.
                      Default is None.
        report: If True, print summary report.
        visualize: If True, show boxplots with highlighted outliers.
        chunk_size: Size of chunks for processing large datasets.
        return_mask: If True, returns a DataFrame with boolean masks; if False, returns a dictionary with detailed results.

    Returns:
        If return_mask is True:
            DataFrame with boolean mask indicating outliers
        If return_mask is False:
            Dictionary containing:
            - 'outlier_counts': Number of outliers per feature
            - 'outlier_percentage': Percentage of affected rows
            - 'outlier_indices': Index list of rows with at least one outlier
            - 'feature_outliers': Dictionary of outlier indices for each feature

    Raises:
        ValueError: If method is invalid or if non-numerical columns are present.
    """
    # Validate input
    if X.empty:
        raise ValueError("Empty dataset provided")
    
    # Get numerical columns
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
    if len(numerical_cols) == 0:
        raise ValueError("No numeric columns found in the dataset")
    
    # Validate method
    if method not in ['zscore', 'iqr', 'isolation_forest']:
        raise ValueError("Method must be one of: zscore, iqr, isolation_forest")
    
    # Validate threshold and contamination
    if method in ['zscore', 'iqr']:
        if threshold <= 0:
            raise ValueError("Threshold must be positive")
    else:  # isolation_forest
        if contamination is not None:
            if contamination <= 0 or contamination >= 1:
                raise ValueError("Contamination must be between 0 and 1")
            threshold = contamination
        elif threshold <= 0 or threshold >= 1:
            raise ValueError("For isolation_forest method, threshold must be between 0 and 1")
    
    # Handle large datasets
    if len(X) > 1_000_000:
        X_dask = dd.from_pandas(X, chunksize=chunk_size)
        is_dask = True
    else:
        X_dask = X
        is_dask = False
    
    # Initialize result DataFrame with False values if return_mask is True
    if return_mask:
        result_df = pd.DataFrame(False, index=X.index, columns=numerical_cols)
    
    # Detect outliers based on method
    if method == 'zscore':
        result_dict = _detect_zscore_outliers(X_dask, numerical_cols, is_dask, threshold)
    elif method == 'iqr':
        result_dict = _detect_iqr_outliers(X_dask, numerical_cols, is_dask, threshold)
    elif method == 'isolation_forest':
        result_dict = _detect_isolation_forest_outliers(X_dask, numerical_cols, is_dask, threshold)
    
    # Generate report if requested
    if report:
        _print_outlier_report(result_dict)
    
    # Visualize outliers if requested
    if visualize:
        _visualize_outliers(X, result_dict, numerical_cols, is_dask)
    
    # If return_mask is True, convert dictionary to DataFrame
    if return_mask:
        # Create a DataFrame with boolean masks
        for col in numerical_cols:
            outlier_indices = result_dict['feature_outliers'][col]
            result_df.loc[outlier_indices, col] = True
        
        return result_df
    
    return result_dict


def _detect_zscore_outliers(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index, is_dask: bool, threshold: float = 3.0) -> Dict:
    """
    Detect outliers using Z-score method.
    
    Args:
        X: Input DataFrame
        numerical_cols: List of numerical column names
        is_dask: Whether X is a Dask DataFrame
        threshold: Number of standard deviations for outlier detection
        
    Returns:
        Dictionary with outlier information
    """
    # Initialize result dictionary
    result = {
        'outlier_counts': {},
        'outlier_percentage': 0.0,
        'outlier_indices': [],
        'feature_outliers': {}
    }
    
    # Process each column
    for col in numerical_cols:
        if is_dask:
            # Calculate mean and std for the column
            mean = X[col].mean().compute()
            std = X[col].std().compute()
            
            # Identify outliers
            z_scores = ((X[col] - mean) / std).compute()
            outliers = (abs(z_scores) > threshold).compute()
            
            # Get outlier indices
            outlier_indices = X.index[outliers].compute().tolist()
        else:
            # Calculate mean and std for the column
            mean = X[col].mean()
            std = X[col].std()
            
            # Identify outliers
            z_scores = (X[col] - mean) / std
            outliers = abs(z_scores) > threshold
            
            # Get outlier indices
            outlier_indices = X.index[outliers].tolist()
        
        # Store results
        result['outlier_counts'][col] = len(outlier_indices)
        result['feature_outliers'][col] = outlier_indices
    
    # Calculate overall statistics
    all_outlier_indices = set()
    for indices in result['feature_outliers'].values():
        all_outlier_indices.update(indices)
    
    result['outlier_indices'] = list(all_outlier_indices)
    result['outlier_percentage'] = len(all_outlier_indices) / len(X) * 100
    
    return result


def _detect_iqr_outliers(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index, is_dask: bool, threshold: float = 1.5) -> Dict:
    """
    Detect outliers using IQR method.
    
    Args:
        X: Input DataFrame
        numerical_cols: List of numerical column names
        is_dask: Whether X is a Dask DataFrame
        threshold: Multiplier for IQR for outlier detection
        
    Returns:
        Dictionary with outlier information
    """
    # Initialize result dictionary
    result = {
        'outlier_counts': {},
        'outlier_percentage': 0.0,
        'outlier_indices': [],
        'feature_outliers': {}
    }
    
    # Process each column
    for col in numerical_cols:
        if is_dask:
            # Calculate Q1, Q3, and IQR
            q1 = X[col].quantile(0.25).compute()
            q3 = X[col].quantile(0.75).compute()
            iqr = q3 - q1
            
            # Define bounds
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            # Identify outliers
            outliers = ((X[col] < lower_bound) | (X[col] > upper_bound)).compute()
            
            # Get outlier indices
            outlier_indices = X.index[outliers].compute().tolist()
        else:
            # Calculate Q1, Q3, and IQR
            q1 = X[col].quantile(0.25)
            q3 = X[col].quantile(0.75)
            iqr = q3 - q1
            
            # Define bounds
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            # Identify outliers
            outliers = (X[col] < lower_bound) | (X[col] > upper_bound)
            
            # Get outlier indices
            outlier_indices = X.index[outliers].tolist()
        
        # Store results
        result['outlier_counts'][col] = len(outlier_indices)
        result['feature_outliers'][col] = outlier_indices
    
    # Calculate overall statistics
    all_outlier_indices = set()
    for indices in result['feature_outliers'].values():
        all_outlier_indices.update(indices)
    
    result['outlier_indices'] = list(all_outlier_indices)
    result['outlier_percentage'] = len(all_outlier_indices) / len(X) * 100
    
    return result


def _detect_isolation_forest_outliers(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index, is_dask: bool, threshold: float = 0.1) -> Dict:
    """
    Detect outliers using Isolation Forest.
    
    Args:
        X: Input DataFrame
        numerical_cols: List of numerical column names
        is_dask: Whether X is a Dask DataFrame
        threshold: Contamination parameter for Isolation Forest
        
    Returns:
        Dictionary with outlier information
    """
    # Initialize result dictionary
    result = {
        'outlier_counts': {},
        'outlier_percentage': 0.0,
        'outlier_indices': [],
        'feature_outliers': {}
    }
    
    # Convert to pandas if using dask
    if is_dask:
        X_pandas = X.compute()
    else:
        X_pandas = X
    
    # Create and fit the Isolation Forest
    iso_forest = IsolationForest(n_estimators=100, contamination=threshold, random_state=42)
    iso_forest.fit(X_pandas)
    
    # Predict outliers
    predictions = iso_forest.predict(X_pandas)
    is_outlier = predictions == -1
    
    # Get outlier indices
    outlier_indices = X_pandas.index[is_outlier].tolist()
    
    # Store results for each column
    for col in numerical_cols:
        result['outlier_counts'][col] = len(outlier_indices)
        result['feature_outliers'][col] = outlier_indices
    
    # Calculate overall statistics
    result['outlier_indices'] = outlier_indices
    result['outlier_percentage'] = len(outlier_indices) / len(X_pandas) * 100
    
    return result


def _print_outlier_report(result: Dict) -> None:
    """
    Print a summary report of detected outliers.
    
    Args:
        result: Dictionary with outlier information
    """
    print("Outlier Detection Report")
    print("=======================")
    print(f"Total outliers detected: {len(result['outlier_indices'])}")
    print(f"Percentage of dataset affected: {result['outlier_percentage']:.2f}%")
    print("\nOutliers by feature:")
    for col, count in result['outlier_counts'].items():
        print(f"  {col}: {count} outliers")


def _visualize_outliers(X: Union[pd.DataFrame, dd.DataFrame], result: Dict, numerical_cols: pd.Index, is_dask: bool) -> None:
    """
    Visualize outliers using boxplots.
    
    Args:
        X: Input DataFrame
        result: Dictionary with outlier information
        numerical_cols: List of numerical column names
        is_dask: Whether X is a Dask DataFrame
    """
    # Convert to pandas DataFrame if needed
    if is_dask:
        X_pandas = X.compute()
    else:
        X_pandas = X
    
    # Create a figure with subplots
    n_cols = min(3, len(numerical_cols))
    n_rows = (len(numerical_cols) + n_cols - 1) // n_cols
    
    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=numerical_cols)
    
    # Add boxplots for each feature
    for i, col in enumerate(numerical_cols):
        row = i // n_cols + 1
        col_idx = i % n_cols + 1
        
        # Get data for this feature
        data = X_pandas[col].values
        
        # Create boxplot
        fig.add_trace(
            go.Box(y=data, name=col, boxpoints='outliers'),
            row=row, col=col_idx
        )
    
    # Update layout
    fig.update_layout(
        title_text="Outlier Detection Results",
        height=300 * n_rows,
        width=1000,
        showlegend=False
    )
    
    # Show the figure
    fig.show() 