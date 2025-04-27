"""
Feature Creator Module for ThinkML.

This module provides functionality for creating and transforming features in machine learning pipelines.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from typing import List, Union, Dict, Any, Optional

class FeatureCreator(BaseEstimator, TransformerMixin):
    """
    A class for creating and transforming features in machine learning pipelines.
    
    This class provides methods for:
    - Creating interaction features
    - Generating polynomial features
    - Creating time-based features
    - Handling categorical variables
    - Scaling numerical features
    """
    
    def __init__(
        self,
        numerical_features: Optional[List[str]] = None,
        categorical_features: Optional[List[str]] = None,
        interaction_features: Optional[List[tuple]] = None,
        polynomial_degree: int = 2,
        scaling_method: str = 'standard',
        encoding_method: str = 'onehot'
    ):
        """
        Initialize the FeatureCreator.
        
        Parameters
        ----------
        numerical_features : List[str], optional
            List of numerical feature names
        categorical_features : List[str], optional
            List of categorical feature names
        interaction_features : List[tuple], optional
            List of feature pairs to create interactions
        polynomial_degree : int, default=2
            Degree of polynomial features
        scaling_method : str, default='standard'
            Method for scaling numerical features ('standard', 'minmax', 'robust')
        encoding_method : str, default='onehot'
            Method for encoding categorical features ('onehot', 'label')
        """
        self.numerical_features = numerical_features or []
        self.categorical_features = categorical_features or []
        self.interaction_features = interaction_features or []
        self.polynomial_degree = polynomial_degree
        self.scaling_method = scaling_method
        self.encoding_method = encoding_method
        
        # Initialize transformers
        self.scalers = {}
        self.encoders = {}
        self.feature_names = []
        
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> 'FeatureCreator':
        """
        Fit the feature creator to the data.
        
        Parameters
        ----------
        X : pd.DataFrame
            Training data
        y : pd.Series, optional
            Target values
            
        Returns
        -------
        self : FeatureCreator
            Returns the instance itself
        """
        # Fit numerical feature scalers
        for feature in self.numerical_features:
            if feature in X.columns:
                if self.scaling_method == 'standard':
                    self.scalers[feature] = StandardScaler()
                elif self.scaling_method == 'minmax':
                    self.scalers[feature] = MinMaxScaler()
                elif self.scaling_method == 'robust':
                    self.scalers[feature] = RobustScaler()
                self.scalers[feature].fit(X[[feature]])
        
        # Fit categorical feature encoders
        for feature in self.categorical_features:
            if feature in X.columns:
                if self.encoding_method == 'onehot':
                    self.encoders[feature] = OneHotEncoder(sparse=False, handle_unknown='ignore')
                else:
                    self.encoders[feature] = LabelEncoder()
                self.encoders[feature].fit(X[feature].values.reshape(-1, 1))
        
        # Generate feature names
        self._generate_feature_names(X)
        
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the data using the fitted feature creator.
        
        Parameters
        ----------
        X : pd.DataFrame
            Data to transform
            
        Returns
        -------
        pd.DataFrame
            Transformed data
        """
        transformed_data = []
        
        # Transform numerical features
        for feature in self.numerical_features:
            if feature in X.columns and feature in self.scalers:
                scaled_values = self.scalers[feature].transform(X[[feature]])
                transformed_data.append(pd.DataFrame(
                    scaled_values,
                    columns=[f"{feature}_scaled"],
                    index=X.index
                ))
        
        # Transform categorical features
        for feature in self.categorical_features:
            if feature in X.columns and feature in self.encoders:
                if self.encoding_method == 'onehot':
                    encoded_values = self.encoders[feature].transform(X[feature].values.reshape(-1, 1))
                    encoded_df = pd.DataFrame(
                        encoded_values,
                        columns=[f"{feature}_{i}" for i in range(encoded_values.shape[1])],
                        index=X.index
                    )
                else:
                    encoded_values = self.encoders[feature].transform(X[feature])
                    encoded_df = pd.DataFrame(
                        encoded_values,
                        columns=[f"{feature}_encoded"],
                        index=X.index
                    )
                transformed_data.append(encoded_df)
        
        # Create interaction features
        for feat1, feat2 in self.interaction_features:
            if feat1 in X.columns and feat2 in X.columns:
                interaction = X[feat1] * X[feat2]
                transformed_data.append(pd.DataFrame(
                    interaction,
                    columns=[f"{feat1}_{feat2}_interaction"],
                    index=X.index
                ))
        
        # Combine all transformed features
        if transformed_data:
            result = pd.concat(transformed_data, axis=1)
            return result
        return X
    
    def _generate_feature_names(self, X: pd.DataFrame) -> None:
        """Generate feature names for the transformed data."""
        feature_names = []
        
        # Add scaled numerical feature names
        for feature in self.numerical_features:
            if feature in X.columns:
                feature_names.append(f"{feature}_scaled")
        
        # Add encoded categorical feature names
        for feature in self.categorical_features:
            if feature in X.columns and feature in self.encoders:
                if self.encoding_method == 'onehot':
                    n_categories = len(self.encoders[feature].categories_[0])
                    feature_names.extend([f"{feature}_{i}" for i in range(n_categories)])
                else:
                    feature_names.append(f"{feature}_encoded")
        
        # Add interaction feature names
        for feat1, feat2 in self.interaction_features:
            if feat1 in X.columns and feat2 in X.columns:
                feature_names.append(f"{feat1}_{feat2}_interaction")
        
        self.feature_names = feature_names
    
    def get_feature_names(self) -> List[str]:
        """
        Get the names of the transformed features.
        
        Returns
        -------
        List[str]
            List of feature names
        """
        return self.feature_names 