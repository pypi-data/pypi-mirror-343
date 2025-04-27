"""
MulticollinearityHandler module for detecting and resolving multicollinearity in datasets.

This module provides functionality to:
1. Detect multicollinearity using Variance Inflation Factor (VIF)
2. Resolve multicollinearity by removing highly correlated features
3. Generate reports on multicollinearity issues
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Union, Optional
import logging
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Configure logging
logger = logging.getLogger(__name__)

class MulticollinearityHandler:
    """
    Handler for detecting and resolving multicollinearity in datasets.
    """

    def __init__(self, threshold: float = 5.0):
        """
        Initialize the MulticollinearityHandler.

        Args:
            threshold (float): VIF threshold for multicollinearity detection.
                Default is 5.0.
        """
        self.threshold = threshold
        self.vif_scores = {}
        self.high_vif_features = []

    def detect_multicollinearity(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Detect multicollinearity using Variance Inflation Factor (VIF).

        Args:
            data (pd.DataFrame): Input DataFrame.

        Returns:
            Dict[str, float]: Dictionary mapping feature names to their VIF scores.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")

        if data.empty:
            raise ValueError("Empty dataset provided")

        # Initialize VIF scores dictionary
        vif_scores = {}
        high_vif_features = []

        # Calculate VIF for each feature
        for feature in data.columns:
            # Create feature matrix excluding the current feature
            X = data.drop(columns=[feature])
            y = data[feature]

            # Fit linear regression
            model = LinearRegression()
            model.fit(X, y)

            # Calculate R-squared
            r_squared = model.score(X, y)

            # Calculate VIF
            vif = 1 / (1 - r_squared) if r_squared != 1 else float('inf')
            vif_scores[feature] = vif

            # Check if VIF exceeds threshold
            if vif > self.threshold:
                high_vif_features.append(feature)
                logger.warning(f"High VIF score for feature '{feature}': {vif:.2f}")

        self.vif_scores = vif_scores
        self.high_vif_features = high_vif_features

        # Check that high VIF features are detected
        assert any(vif > 5.0 for vif in vif_scores.values()), "No high VIF features detected"

        return vif_scores

    def resolve_multicollinearity(
        self,
        data: pd.DataFrame,
        method: str = 'drop',
        threshold: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Resolve multicollinearity in the dataset.

        Args:
            data (pd.DataFrame): Input DataFrame.
            method (str): Method to resolve multicollinearity.
                Options: 'drop', 'pca', 'threshold'.
            threshold (Optional[float]): Custom threshold for feature selection.
                If None, uses the instance threshold.

        Returns:
            pd.DataFrame: DataFrame with multicollinearity resolved.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")

        if data.empty:
            raise ValueError("Empty dataset provided")

        # Use instance threshold if none provided
        if threshold is None:
            threshold = self.threshold

        # Detect multicollinearity if not already done
        if not self.vif_scores:
            self.detect_multicollinearity(data)

        if method == 'drop':
            # Drop features with high VIF
            features_to_drop = [f for f, vif in self.vif_scores.items() if vif > threshold]
            if features_to_drop:
                logger.info(f"Dropping {len(features_to_drop)} features with high VIF")
                return data.drop(columns=features_to_drop)
            return data

        elif method == 'pca':
            # Apply PCA to features with high VIF
            high_vif_features = [f for f, vif in self.vif_scores.items() if vif > threshold]
            if not high_vif_features:
                return data

            # Separate high VIF features
            high_vif_data = data[high_vif_features]
            other_data = data.drop(columns=high_vif_features)

            # Apply PCA
            pca = PCA(n_components=0.95)  # Keep 95% of variance
            pca_result = pca.fit_transform(high_vif_data)

            # Create DataFrame with PCA components
            pca_df = pd.DataFrame(
                pca_result,
                columns=[f'PC{i+1}' for i in range(pca_result.shape[1])],
                index=data.index
            )

            # Combine with other features
            return pd.concat([other_data, pca_df], axis=1)

        elif method == 'threshold':
            # Keep only features with VIF below threshold
            features_to_keep = [f for f, vif in self.vif_scores.items() if vif <= threshold]
            if len(features_to_keep) < len(data.columns):
                logger.info(f"Keeping {len(features_to_keep)} features with VIF <= {threshold}")
                return data[features_to_keep]
            return data

        else:
            raise ValueError(f"Unknown method: {method}")

    def generate_report(self) -> Dict:
        """
        Generate a report on multicollinearity issues.
        
        Returns
        -------
        Dict
            A dictionary containing information about multicollinearity issues.
        """
        if not self.vif_scores:
            return {
                "status": "No VIF scores calculated yet",
                "timestamp": pd.Timestamp.now().isoformat()
            }
        
        # Create a DataFrame for the report
        report_df = pd.DataFrame({
            "Feature": list(self.vif_scores.keys()),
            "VIF Score": list(self.vif_scores.values()),
            "Status": ["High" if vif > self.threshold else "Acceptable" 
                      for vif in self.vif_scores.values()]
        })
        
        # Sort by VIF score in descending order
        report_df = report_df.sort_values("VIF Score", ascending=False)
        
        # Count high VIF features
        high_vif_count = sum(1 for vif in self.vif_scores.values() if vif > self.threshold)
        
        # Generate summary
        summary = {
            "total_features": len(self.vif_scores),
            "high_vif_features": high_vif_count,
            "threshold": self.threshold,
            "resolution_applied": self.high_vif_features,
            "features_removed": len(self.high_vif_features)
        }
        
        return {
            "summary": summary,
            "vif_scores": self.vif_scores,
            "features_removed": self.high_vif_features,
            "timestamp": pd.Timestamp.now().isoformat()
        }
    
    def get_suggestions(self) -> List[str]:
        """
        Get suggestions for resolving multicollinearity issues.
        
        Returns
        -------
        List[str]
            A list of suggestions for resolving multicollinearity issues.
        """
        if not self.vif_scores:
            return ["No VIF scores calculated yet. Run detect_multicollinearity() first."]
        
        suggestions = []
        
        # Add suggestions based on VIF scores
        suggestions.append(f"Found {len(self.high_vif_features)} features with high VIF scores:")
        
        for feature in self.high_vif_features:
            vif = self.vif_scores[feature]
            suggestions.append(f"- '{feature}' has a VIF score of {vif:.2f}")
        
        suggestions.append(f"Consider removing these features or using feature selection methods.")
        
        # Add specific suggestions for pairs of highly correlated features
        if len(self.high_vif_features) >= 2:
            suggestions.append("For pairs of highly correlated features, consider:")
            suggestions.append("- Keeping only one of the features")
            suggestions.append("- Creating a composite feature")
            suggestions.append("- Using dimensionality reduction techniques like PCA")
        
        return suggestions

    def calculate_vif(self, data: pd.DataFrame, threshold: float = 5.0) -> Dict[str, float]:
        """
        Calculate Variance Inflation Factor (VIF) for each feature.

        Args:
            data: Input DataFrame
            threshold: VIF threshold for identifying multicollinearity

        Returns:
            Dictionary mapping feature names to their VIF scores
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        # Select only numeric columns
        numeric_data = data.select_dtypes(include=['int64', 'float64'])
        
        if numeric_data.empty:
            raise ValueError("No numeric columns found in the dataset")

        vif_scores = {}
        high_vif_features = []

        for column in numeric_data.columns:
            # Create feature matrix excluding the current column
            X = numeric_data.drop(columns=[column])
            y = numeric_data[column]

            # Fit linear regression
            model = LinearRegression()
            model.fit(X, y)

            # Calculate R-squared
            r_squared = model.score(X, y)

            # Calculate VIF
            if r_squared == 1:
                vif = float('inf')
            else:
                vif = 1 / (1 - r_squared)

            vif_scores[column] = float(vif)  # Ensure VIF is a float

            if vif > threshold:
                high_vif_features.append(column)

        self.vif_scores = vif_scores
        self.high_vif_features = high_vif_features

        return vif_scores


def detect_multicollinearity(data: pd.DataFrame) -> Dict[str, float]:
    """
    Detect multicollinearity in the dataset using Variance Inflation Factor (VIF).
    
    Parameters
    ----------
    data : pd.DataFrame
        The dataset to analyze.
        
    Returns
    -------
    Dict[str, float]
        Dictionary mapping feature names to their VIF scores.
    """
    handler = MulticollinearityHandler()
    return handler.detect_multicollinearity(data)


def resolve_multicollinearity(data: pd.DataFrame, 
                             method: str = 'drop',
                             threshold: Optional[float] = None) -> pd.DataFrame:
    """
    Resolve multicollinearity in the dataset.
    
    Parameters
    ----------
    data : pd.DataFrame
        The dataset to process.
    method : str
        Method to resolve multicollinearity.
        Options: 'drop', 'pca', 'threshold'.
    threshold : float, optional
        Custom threshold for feature selection. If None, uses the instance threshold.
        
    Returns
    -------
    pd.DataFrame
        The processed dataset with multicollinearity resolved.
    """
    handler = MulticollinearityHandler()
    return handler.resolve_multicollinearity(data, method, threshold)

def calculate_vif(data: pd.DataFrame, threshold: float = 5.0) -> Dict[str, float]:
    """
    Calculate Variance Inflation Factor (VIF) for each feature.

    Args:
        data: Input DataFrame
        threshold: VIF threshold for identifying multicollinearity

    Returns:
        Dictionary mapping column names to their VIF scores

    Raises:
        ValueError: If input data contains non-numeric columns
        TypeError: If input is not a pandas DataFrame
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # Check for non-numeric columns
    non_numeric_cols = data.select_dtypes(exclude=['int64', 'float64']).columns
    if len(non_numeric_cols) > 0:
        raise ValueError(f"Non-numeric columns found: {non_numeric_cols.tolist()}")

    # Initialize VIF scores dictionary
    vif_scores = {}
    high_vif_features = []

    # Calculate VIF for each feature
    for col in data.columns:
        # Create feature matrix excluding current column
        X = data.drop(columns=[col])
        y = data[col]

        # Fit linear regression
        model = LinearRegression()
        model.fit(X, y)

        # Calculate R-squared
        r_squared = model.score(X, y)

        # Calculate VIF
        vif = 1 / (1 - r_squared) if r_squared != 1 else float('inf')
        vif_scores[col] = vif

        # Check if VIF exceeds threshold
        if vif > threshold:
            high_vif_features.append(col)

    # Log high VIF features
    if high_vif_features:
        logging.warning(f"High VIF features detected: {high_vif_features}")

    return vif_scores 