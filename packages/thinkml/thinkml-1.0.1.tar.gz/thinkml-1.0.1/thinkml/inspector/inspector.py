"""
Data Inspector module for ThinkML.

This module provides functionality for inspecting and automatically fixing data issues.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import re
import unicodedata
from datetime import datetime
import logging
import json
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('thinkml.inspector')


class DataInspector:
    """
    A class for inspecting and automatically fixing data issues.
    
    This class provides methods for:
    - Inspecting data for common issues
    - Automatically fixing detected issues
    - Generating reports of data quality
    """
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        Initialize the DataInspector.
        
        Args:
            log_dir: Directory to store logs and reports. If None, logs will be stored in memory.
        """
        self.log_dir = log_dir
        self.inspection_results = {}
        self.fix_results = {}
        self.report_data = {}
        
        # Create log directory if specified
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            self.log_file = os.path.join(log_dir, f'inspector_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(file_handler)
    
    def inspect_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Inspect data for common issues.
        
        Args:
            data: Input DataFrame to inspect.
            
        Returns:
            Dictionary containing inspection results.
        """
        logger.info("Starting data inspection")
        self.inspection_results = {}
        
        # Check for empty dataset
        if data.empty:
            logger.warning("Empty dataset detected")
            self.inspection_results['empty_dataset'] = True
            return self.inspection_results
        
        # Basic dataset info
        self.inspection_results['shape'] = data.shape
        self.inspection_results['columns'] = list(data.columns)
        self.inspection_results['dtypes'] = {col: str(dtype) for col, dtype in data.dtypes.items()}
        
        # Check for missing data
        missing_data = self._check_missing_data(data)
        self.inspection_results['missing_data'] = missing_data
        
        # Check for outliers
        outliers = self._check_outliers(data)
        self.inspection_results['outliers'] = outliers
        
        # Check for mixed data types
        mixed_types = self._check_mixed_types(data)
        self.inspection_results['mixed_types'] = mixed_types
        
        # Check for unicode issues
        unicode_issues = self._check_unicode(data)
        self.inspection_results['unicode_issues'] = unicode_issues
        
        # Check for special characters in column names
        special_chars = self._check_special_chars(data)
        self.inspection_results['special_chars'] = special_chars
        
        # Check for time series issues
        time_series_issues = self._check_time_series(data)
        self.inspection_results['time_series_issues'] = time_series_issues
        
        # Check for nested data
        nested_data = self._check_nested_data(data)
        self.inspection_results['nested_data'] = nested_data
        
        # Check for highly correlated features
        correlations = self._check_correlations(data)
        self.inspection_results['correlations'] = correlations
        
        # Check for imbalanced datasets
        imbalanced = self._check_imbalanced(data)
        self.inspection_results['imbalanced'] = imbalanced
        
        # Check for sparse datasets
        sparse = self._check_sparse(data)
        self.inspection_results['sparse'] = sparse
        
        logger.info("Data inspection completed")
        return self.inspection_results
    
    def auto_fix_data(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Automatically fix detected issues in the data.
        
        Args:
            data: Input DataFrame to fix.
            
        Returns:
            Tuple containing the fixed DataFrame and a dictionary of fixes applied.
        """
        logger.info("Starting automatic data fixing")
        
        # Run inspection if not already done
        if not self.inspection_results:
            self.inspect_data(data)
        
        # Create a copy of the data to avoid modifying the original
        fixed_data = data.copy()
        self.fix_results = {}
        
        # Fix missing data
        if self.inspection_results.get('missing_data', {}).get('has_missing', False):
            fixed_data, missing_fixes = self._fix_missing_data(fixed_data)
            self.fix_results['missing_data'] = missing_fixes
        
        # Fix outliers
        if self.inspection_results.get('outliers', {}).get('has_outliers', False):
            fixed_data, outlier_fixes = self._fix_outliers(fixed_data)
            self.fix_results['outliers'] = outlier_fixes
        
        # Fix mixed data types
        if self.inspection_results.get('mixed_types', {}).get('has_mixed_types', False):
            fixed_data, mixed_type_fixes = self._fix_mixed_types(fixed_data)
            self.fix_results['mixed_types'] = mixed_type_fixes
        
        # Fix unicode issues
        if self.inspection_results.get('unicode_issues', {}).get('has_unicode_issues', False):
            fixed_data, unicode_fixes = self._fix_unicode(fixed_data)
            self.fix_results['unicode_issues'] = unicode_fixes
        
        # Fix special characters in column names
        if self.inspection_results.get('special_chars', {}).get('has_special_chars', False):
            fixed_data, special_char_fixes = self._fix_special_chars(fixed_data)
            self.fix_results['special_chars'] = special_char_fixes
        
        # Fix time series issues
        if self.inspection_results.get('time_series_issues', {}).get('has_time_series_issues', False):
            fixed_data, time_series_fixes = self._fix_time_series(fixed_data)
            self.fix_results['time_series_issues'] = time_series_fixes
        
        # Fix nested data
        if self.inspection_results.get('nested_data', {}).get('has_nested_data', False):
            fixed_data, nested_data_fixes = self._fix_nested_data(fixed_data)
            self.fix_results['nested_data'] = nested_data_fixes
        
        # Fix highly correlated features
        if self.inspection_results.get('correlations', {}).get('has_high_correlations', False):
            fixed_data, correlation_fixes = self._fix_correlations(fixed_data)
            self.fix_results['correlations'] = correlation_fixes
        
        # Fix imbalanced datasets
        if self.inspection_results.get('imbalanced', {}).get('is_imbalanced', False):
            fixed_data, imbalanced_fixes = self._fix_imbalanced(fixed_data)
            self.fix_results['imbalanced'] = imbalanced_fixes
        
        # Fix sparse datasets
        if self.inspection_results.get('sparse', {}).get('is_sparse', False):
            fixed_data, sparse_fixes = self._fix_sparse(fixed_data)
            self.fix_results['sparse'] = sparse_fixes
        
        logger.info("Automatic data fixing completed")
        return fixed_data, self.fix_results
    
    def generate_report(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a report of the inspection and fixing results.
        
        Args:
            output_path: Path to save the report. If None, the report will be returned but not saved.
            
        Returns:
            Dictionary containing the report data.
        """
        logger.info("Generating inspection report")
        
        # Prepare report data
        self.report_data = {
            'inspection_results': self.inspection_results,
            'fix_results': self.fix_results,
            'timestamp': datetime.now().isoformat(),
            'summary': self._generate_summary()
        }
        
        # Save report if output path is provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(self.report_data, f, indent=2)
            logger.info(f"Report saved to {output_path}")
        
        return self.report_data
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of the inspection and fixing results."""
        summary = {
            'total_issues': 0,
            'issues_fixed': 0,
            'issues_by_type': {}
        }
        
        # Count issues by type
        for issue_type, issue_data in self.inspection_results.items():
            if isinstance(issue_data, dict) and 'has_' in issue_data:
                for key, value in issue_data.items():
                    if key.startswith('has_') and value:
                        issue_name = key[4:]  # Remove 'has_' prefix
                        summary['issues_by_type'][issue_name] = True
                        summary['total_issues'] += 1
        
        # Count fixed issues
        for fix_type, fix_data in self.fix_results.items():
            if fix_data:
                summary['issues_fixed'] += 1
        
        return summary
    
    # Inspection methods
    def _check_missing_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for missing data in the DataFrame."""
        result = {
            'has_missing': False,
            'missing_counts': {},
            'missing_percentages': {},
            'columns_with_missing': []
        }
        
        for col in data.columns:
            missing_count = data[col].isnull().sum()
            missing_percentage = (missing_count / len(data)) * 100
            
            result['missing_counts'][col] = int(missing_count)
            result['missing_percentages'][col] = float(missing_percentage)
            
            if missing_count > 0:
                result['has_missing'] = True
                result['columns_with_missing'].append(col)
        
        return result
    
    def _check_outliers(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for outliers in numeric columns."""
        result = {
            'has_outliers': False,
            'outlier_counts': {},
            'outlier_percentages': {},
            'columns_with_outliers': []
        }
        
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                # Calculate IQR
                q1 = data[col].quantile(0.25)
                q3 = data[col].quantile(0.75)
                iqr = q3 - q1
                
                # Define outlier bounds
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                # Count outliers
                outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)][col]
                outlier_count = len(outliers)
                outlier_percentage = (outlier_count / len(data)) * 100
                
                result['outlier_counts'][col] = int(outlier_count)
                result['outlier_percentages'][col] = float(outlier_percentage)
                
                if outlier_count > 0:
                    result['has_outliers'] = True
                    result['columns_with_outliers'].append(col)
        
        return result
    
    def _check_mixed_types(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for mixed data types in columns."""
        result = {
            'has_mixed_types': False,
            'mixed_type_columns': []
        }
        
        for col in data.columns:
            # Check if column has mixed types
            unique_types = data[col].apply(type).unique()
            if len(unique_types) > 1:
                result['has_mixed_types'] = True
                result['mixed_type_columns'].append(col)
        
        return result
    
    def _check_unicode(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for unicode issues in string columns."""
        result = {
            'has_unicode_issues': False,
            'unicode_issues_by_column': {}
        }
        
        for col in data.columns:
            if pd.api.types.is_string_dtype(data[col]):
                # Check for non-ASCII characters
                non_ascii_count = 0
                for val in data[col].dropna():
                    if any(ord(c) > 127 for c in str(val)):
                        non_ascii_count += 1
                
                if non_ascii_count > 0:
                    result['has_unicode_issues'] = True
                    result['unicode_issues_by_column'][col] = {
                        'non_ascii_count': non_ascii_count,
                        'non_ascii_percentage': (non_ascii_count / len(data)) * 100
                    }
        
        return result
    
    def _check_special_chars(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for special characters in column names."""
        result = {
            'has_special_chars': False,
            'columns_with_special_chars': []
        }
        
        for col in data.columns:
            # Check for special characters in column names
            if re.search(r'[^a-zA-Z0-9_]', col):
                result['has_special_chars'] = True
                result['columns_with_special_chars'].append(col)
        
        return result
    
    def _check_time_series(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for time series issues."""
        result = {
            'has_time_series_issues': False,
            'datetime_columns': [],
            'missing_dates': False,
            'irregular_intervals': False
        }
        
        # Check for datetime columns
        for col in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[col]):
                result['datetime_columns'].append(col)
                
                # Check for missing dates
                if data[col].isnull().any():
                    result['missing_dates'] = True
                
                # Check for irregular intervals
                if len(data) > 2:
                    sorted_dates = data[col].sort_values()
                    intervals = sorted_dates.diff().dropna()
                    if len(intervals.unique()) > 1:
                        result['irregular_intervals'] = True
        
        if result['datetime_columns']:
            result['has_time_series_issues'] = True
        
        return result
    
    def _check_nested_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for nested data structures."""
        result = {
            'has_nested_data': False,
            'nested_columns': []
        }
        
        for col in data.columns:
            # Check if column contains dictionaries or lists
            if data[col].apply(lambda x: isinstance(x, (dict, list))).any():
                result['has_nested_data'] = True
                result['nested_columns'].append(col)
        
        return result
    
    def _check_correlations(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for highly correlated features."""
        result = {
            'has_high_correlations': False,
            'correlation_matrix': {},
            'high_correlation_pairs': []
        }
        
        # Get numeric columns
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
        
        if len(numeric_cols) > 1:
            # Calculate correlation matrix
            corr_matrix = data[numeric_cols].corr()
            result['correlation_matrix'] = corr_matrix.to_dict()
            
            # Find highly correlated pairs
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    col1, col2 = numeric_cols[i], numeric_cols[j]
                    corr = corr_matrix.loc[col1, col2]
                    
                    if abs(corr) > 0.95:
                        result['has_high_correlations'] = True
                        result['high_correlation_pairs'].append({
                            'column1': col1,
                            'column2': col2,
                            'correlation': float(corr)
                        })
        
        return result
    
    def _check_imbalanced(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for imbalanced datasets."""
        result = {
            'is_imbalanced': False,
            'target_column': None,
            'class_distribution': {},
            'imbalance_ratio': None
        }
        
        # Try to identify target column (assuming it's the last column)
        if len(data.columns) > 0:
            target_col = data.columns[-1]
            
            # Check if target column is categorical
            if pd.api.types.is_categorical_dtype(data[target_col]) or data[target_col].dtype == 'object':
                # Calculate class distribution
                class_counts = data[target_col].value_counts()
                result['class_distribution'] = class_counts.to_dict()
                
                # Calculate imbalance ratio
                if len(class_counts) > 1:
                    min_class = class_counts.min()
                    max_class = class_counts.max()
                    imbalance_ratio = max_class / min_class
                    
                    # Consider imbalanced if ratio > 2
                    if imbalance_ratio > 2:
                        result['is_imbalanced'] = True
                        result['target_column'] = target_col
                        result['imbalance_ratio'] = float(imbalance_ratio)
        
        return result
    
    def _check_sparse(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Check for sparse datasets."""
        result = {
            'is_sparse': False,
            'sparsity_by_column': {},
            'overall_sparsity': None
        }
        
        # Calculate sparsity for each column
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                # Count zeros
                zero_count = (data[col] == 0).sum()
                sparsity = zero_count / len(data)
                
                result['sparsity_by_column'][col] = float(sparsity)
                
                # Consider column sparse if more than 50% zeros
                if sparsity > 0.5:
                    result['is_sparse'] = True
        
        # Calculate overall sparsity
        if result['sparsity_by_column']:
            result['overall_sparsity'] = sum(result['sparsity_by_column'].values()) / len(result['sparsity_by_column'])
        
        return result
    
    # Fix methods
    def _fix_missing_data(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix missing data in the DataFrame."""
        fixed_data = data.copy()
        fixes = {
            'columns_fixed': [],
            'method_used': {}
        }
        
        for col in fixed_data.columns:
            if fixed_data[col].isnull().any():
                # Choose imputation method based on data type
                if pd.api.types.is_numeric_dtype(fixed_data[col]):
                    # For numeric columns, use median
                    fixed_data[col] = fixed_data[col].fillna(fixed_data[col].median())
                    fixes['method_used'][col] = 'median'
                else:
                    # For categorical columns, use mode
                    mode_val = fixed_data[col].mode().iloc[0] if not fixed_data[col].mode().empty else 'unknown'
                    fixed_data[col] = fixed_data[col].fillna(mode_val)
                    fixes['method_used'][col] = 'mode'
                
                fixes['columns_fixed'].append(col)
        
        return fixed_data, fixes
    
    def _fix_outliers(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix outliers in the DataFrame."""
        fixed_data = data.copy()
        fixes = {
            'columns_fixed': [],
            'outliers_capped': {}
        }
        
        for col in fixed_data.columns:
            if pd.api.types.is_numeric_dtype(fixed_data[col]):
                # Calculate IQR
                q1 = fixed_data[col].quantile(0.25)
                q3 = fixed_data[col].quantile(0.75)
                iqr = q3 - q1
                
                # Define outlier bounds
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                # Count outliers before capping
                outliers_before = fixed_data[(fixed_data[col] < lower_bound) | (fixed_data[col] > upper_bound)][col]
                
                if len(outliers_before) > 0:
                    # Cap outliers
                    fixed_data[col] = fixed_data[col].clip(lower_bound, upper_bound)
                    
                    # Count outliers after capping
                    outliers_after = fixed_data[(fixed_data[col] < lower_bound) | (fixed_data[col] > upper_bound)][col]
                    
                    fixes['columns_fixed'].append(col)
                    fixes['outliers_capped'][col] = {
                        'before': len(outliers_before),
                        'after': len(outliers_after)
                    }
        
        return fixed_data, fixes
    
    def _fix_mixed_types(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix mixed data types in the DataFrame."""
        fixed_data = data.copy()
        fixes = {
            'columns_fixed': [],
            'conversions_applied': {}
        }
        
        for col in fixed_data.columns:
            # Check if column has mixed types
            unique_types = fixed_data[col].apply(type).unique()
            if len(unique_types) > 1:
                # Try to convert to string first
                fixed_data[col] = fixed_data[col].astype(str)
                fixes['columns_fixed'].append(col)
                fixes['conversions_applied'][col] = 'string'
        
        return fixed_data, fixes
    
    def _fix_unicode(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix unicode issues in the DataFrame."""
        fixed_data = data.copy()
        fixes = {
            'columns_fixed': [],
            'normalizations_applied': {}
        }
        
        for col in fixed_data.columns:
            if pd.api.types.is_string_dtype(fixed_data[col]):
                # Check for non-ASCII characters
                has_non_ascii = fixed_data[col].apply(lambda x: any(ord(c) > 127 for c in str(x))).any()
                
                if has_non_ascii:
                    # Normalize unicode characters
                    fixed_data[col] = fixed_data[col].apply(
                        lambda x: unicodedata.normalize('NFKC', str(x)) if pd.notnull(x) else x
                    )
                    
                    fixes['columns_fixed'].append(col)
                    fixes['normalizations_applied'][col] = 'NFKC'
        
        return fixed_data, fixes
    
    def _fix_special_chars(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix special characters in column names."""
        fixed_data = data.copy()
        fixes = {
            'columns_renamed': {},
            'original_names': {}
        }
        
        # Create a mapping of old column names to new ones
        new_columns = {}
        for col in fixed_data.columns:
            if re.search(r'[^a-zA-Z0-9_]', col):
                # Replace special characters with underscores
                new_col = re.sub(r'[^a-zA-Z0-9_]', '_', col)
                
                # Ensure uniqueness
                if new_col in new_columns.values():
                    counter = 1
                    while f"{new_col}_{counter}" in new_columns.values():
                        counter += 1
                    new_col = f"{new_col}_{counter}"
                
                new_columns[col] = new_col
                fixes['columns_renamed'][col] = new_col
                fixes['original_names'][new_col] = col
        
        # Rename columns
        if new_columns:
            fixed_data = fixed_data.rename(columns=new_columns)
        
        return fixed_data, fixes
    
    def _fix_time_series(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix time series issues."""
        fixed_data = data.copy()
        fixes = {
            'columns_fixed': [],
            'missing_dates_filled': {},
            'irregular_intervals_fixed': {}
        }
        
        for col in fixed_data.columns:
            if pd.api.types.is_datetime64_any_dtype(fixed_data[col]):
                # Fill missing dates
                if fixed_data[col].isnull().any():
                    # Forward fill missing dates
                    fixed_data[col] = fixed_data[col].fillna(method='ffill')
                    fixes['missing_dates_filled'][col] = 'forward_fill'
                    fixes['columns_fixed'].append(col)
                
                # Fix irregular intervals
                if len(fixed_data) > 2:
                    sorted_dates = fixed_data[col].sort_values()
                    intervals = sorted_dates.diff().dropna()
                    if len(intervals.unique()) > 1:
                        # Create a regular date range
                        min_date = fixed_data[col].min()
                        max_date = fixed_data[col].max()
                        regular_dates = pd.date_range(start=min_date, end=max_date, freq='D')
                        
                        # Create a new DataFrame with regular dates
                        date_df = pd.DataFrame({col: regular_dates})
                        
                        # Merge with original data
                        fixed_data = pd.merge(date_df, fixed_data, on=col, how='left')
                        
                        # Forward fill missing values
                        fixed_data = fixed_data.fillna(method='ffill')
                        
                        fixes['irregular_intervals_fixed'][col] = 'regularized'
                        fixes['columns_fixed'].append(col)
        
        return fixed_data, fixes
    
    def _fix_nested_data(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix nested data structures."""
        fixed_data = data.copy()
        fixes = {
            'columns_flattened': [],
            'new_columns': {}
        }
        
        for col in fixed_data.columns:
            # Check if column contains dictionaries
            if fixed_data[col].apply(lambda x: isinstance(x, dict)).any():
                # Flatten dictionary column
                flattened = pd.json_normalize(fixed_data[col].dropna().tolist())
                
                # Rename columns to avoid conflicts
                flattened.columns = [f"{col}_{c}" for c in flattened.columns]
                
                # Add flattened columns to the DataFrame
                for new_col in flattened.columns:
                    fixed_data[new_col] = None
                    fixed_data.loc[flattened.index, new_col] = flattened[new_col]
                
                # Drop the original column
                fixed_data = fixed_data.drop(columns=[col])
                
                fixes['columns_flattened'].append(col)
                fixes['new_columns'][col] = list(flattened.columns)
            
            # Check if column contains lists
            elif fixed_data[col].apply(lambda x: isinstance(x, list)).any():
                # For lists, we'll just convert to string representation
                fixed_data[col] = fixed_data[col].apply(lambda x: str(x) if isinstance(x, list) else x)
                fixes['columns_flattened'].append(col)
                fixes['new_columns'][col] = 'string_representation'
        
        return fixed_data, fixes
    
    def _fix_correlations(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix highly correlated features."""
        fixed_data = data.copy()
        fixes = {
            'columns_removed': [],
            'correlation_pairs': {}
        }
        
        # Get numeric columns
        numeric_cols = fixed_data.select_dtypes(include=['int64', 'float64']).columns
        
        if len(numeric_cols) > 1:
            # Calculate correlation matrix
            corr_matrix = fixed_data[numeric_cols].corr()
            
            # Find highly correlated pairs
            columns_to_remove = set()
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    col1, col2 = numeric_cols[i], numeric_cols[j]
                    corr = corr_matrix.loc[col1, col2]
                    
                    if abs(corr) > 0.95:
                        # Keep the column with higher variance
                        var1 = fixed_data[col1].var()
                        var2 = fixed_data[col2].var()
                        
                        if var1 >= var2:
                            columns_to_remove.add(col2)
                            fixes['correlation_pairs'][col2] = {
                                'removed': col2,
                                'kept': col1,
                                'correlation': float(corr)
                            }
                        else:
                            columns_to_remove.add(col1)
                            fixes['correlation_pairs'][col1] = {
                                'removed': col1,
                                'kept': col2,
                                'correlation': float(corr)
                            }
            
            # Remove highly correlated columns
            if columns_to_remove:
                fixed_data = fixed_data.drop(columns=list(columns_to_remove))
                fixes['columns_removed'] = list(columns_to_remove)
        
        return fixed_data, fixes
    
    def _fix_imbalanced(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix imbalanced datasets."""
        fixed_data = data.copy()
        fixes = {
            'target_column': None,
            'method_applied': None,
            'class_weights': {}
        }
        
        # Try to identify target column (assuming it's the last column)
        if len(fixed_data.columns) > 0:
            target_col = fixed_data.columns[-1]
            
            # Check if target column is categorical
            if pd.api.types.is_categorical_dtype(fixed_data[target_col]) or fixed_data[target_col].dtype == 'object':
                # Calculate class distribution
                class_counts = fixed_data[target_col].value_counts()
                
                if len(class_counts) > 1:
                    # Calculate class weights
                    total = len(fixed_data)
                    class_weights = {cls: total / (len(class_counts) * count) for cls, count in class_counts.items()}
                    
                    fixes['target_column'] = target_col
                    fixes['method_applied'] = 'class_weights'
                    fixes['class_weights'] = class_weights
        
        return fixed_data, fixes
    
    def _fix_sparse(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Fix sparse datasets."""
        fixed_data = data.copy()
        fixes = {
            'columns_optimized': [],
            'optimization_method': {}
        }
        
        # For sparse datasets, we'll convert to sparse format for memory efficiency
        for col in fixed_data.columns:
            if pd.api.types.is_numeric_dtype(fixed_data[col]):
                # Calculate sparsity
                zero_count = (fixed_data[col] == 0).sum()
                sparsity = zero_count / len(fixed_data)
                
                # Consider column sparse if more than 50% zeros
                if sparsity > 0.5:
                    # Convert to sparse format
                    fixed_data[col] = pd.SparseArray(fixed_data[col].values, fill_value=0)
                    fixes['columns_optimized'].append(col)
                    fixes['optimization_method'][col] = 'sparse_format'
        
        return fixed_data, fixes 