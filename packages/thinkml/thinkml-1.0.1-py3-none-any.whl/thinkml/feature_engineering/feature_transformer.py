"""
Feature Transformer Module for ThinkML.

This module provides functionality for transforming features in machine learning pipelines.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PolynomialFeatures
from typing import List, Union, Dict, Any, Optional

class FeatureTransformer(BaseEstimator, TransformerMixin):
    """
    A class for transforming features in machine learning pipelines.
    
    This class provides methods for:
    - Polynomial feature generation
    - Feature interaction creation
    - Feature scaling
    - Feature encoding
    """
    
    def __init__(
        self,
        polynomial_degree: int = 2,
        interaction_only: bool = False,
        include_bias: bool = True,
        feature_names: Optional[List[str]] = None
    ):
        """
        Initialize the FeatureTransformer.
        
        Parameters
        ----------
        polynomial_degree : int, default=2
            Degree of polynomial features
        interaction_only : bool, default=False
            If True, only interaction features are produced
        include_bias : bool, default=True
            If True, include a bias column
        feature_names : List[str], optional
            List of feature names
        """
        self.polynomial_degree = polynomial_degree
        self.interaction_only = interaction_only
        self.include_bias = include_bias
        self.feature_names = feature_names
        self.poly_features = PolynomialFeatures(
            degree=polynomial_degree,
            interaction_only=interaction_only,
            include_bias=include_bias
        )
        
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> 'FeatureTransformer':
        """
        Fit the feature transformer to the data.
        
        Parameters
        ----------
        X : pd.DataFrame
            Training data
        y : pd.Series, optional
            Target values
            
        Returns
        -------
        self : FeatureTransformer
            Returns the instance itself
        """
        self.poly_features.fit(X)
        if self.feature_names is None:
            self.feature_names = X.columns.tolist()
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the data using the fitted feature transformer.
        
        Parameters
        ----------
        X : pd.DataFrame
            Data to transform
            
        Returns
        -------
        pd.DataFrame
            Transformed data
        """
        transformed = self.poly_features.transform(X)
        feature_names = self._get_feature_names(X)
        return pd.DataFrame(
            transformed,
            columns=feature_names,
            index=X.index
        )
    
    def _get_feature_names(self, X: pd.DataFrame) -> List[str]:
        """
        Get feature names for the transformed data.
        
        Parameters
        ----------
        X : pd.DataFrame
            Input data
            
        Returns
        -------
        List[str]
            List of feature names
        """
        if self.feature_names is None:
            self.feature_names = X.columns.tolist()
            
        feature_names = []
        if self.include_bias:
            feature_names.append('1')
            
        if self.interaction_only:
            for i in range(len(self.feature_names)):
                for j in range(i + 1, len(self.feature_names)):
                    feature_names.append(f"{self.feature_names[i]} * {self.feature_names[j]}")
        else:
            for i in range(len(self.feature_names)):
                feature_names.append(self.feature_names[i])
                if self.polynomial_degree > 1:
                    for d in range(2, self.polynomial_degree + 1):
                        feature_names.append(f"{self.feature_names[i]}^{d}")
                        
            for i in range(len(self.feature_names)):
                for j in range(i + 1, len(self.feature_names)):
                    feature_names.append(f"{self.feature_names[i]} * {self.feature_names[j]}")
                    
        return feature_names
    
    def get_feature_names(self) -> List[str]:
        """
        Get the names of the transformed features.
        
        Returns
        -------
        List[str]
            List of feature names
        """
        return self._get_feature_names(pd.DataFrame(columns=self.feature_names)) 