"""
Plotting functions for exploratory data analysis.

This module provides functions for creating various types of plots for data analysis,
with support for large datasets through chunk-based processing and Dask integration.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Union, List, Dict, Any
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

def plot(
    X: pd.DataFrame,
    y: Optional[Union[pd.Series, np.ndarray]] = None,
    plot_type: str = 'histogram',
    interactive: bool = False,
    highlight_outliers: bool = True,
    chunk_size: int = 100000
) -> None:
    """
    Create various types of plots for exploratory data analysis.

    Parameters
    ----------
    X : pd.DataFrame
        Input features DataFrame.
    y : Optional[Union[pd.Series, np.ndarray]], default=None
        Target variable for plots that require it (e.g., countplot).
    plot_type : str, default='histogram'
        Type of plot to create. Options:
        - 'histogram': For numerical features
        - 'boxplot': For numerical features
        - 'correlation_heatmap': For numerical features
        - 'countplot': For categorical target variable (requires y)
    interactive : bool, default=False
        If True, creates interactive plots using Plotly.
    highlight_outliers : bool, default=True
        For boxplot, highlights outliers using Z-score and IQR methods.
    chunk_size : int, default=100000
        Size of chunks for processing large datasets.

    Returns
    -------
    None
        Displays the plot directly.

    Raises
    ------
    ValueError
        If plot_type is invalid or if required parameters are missing.
    """
    if X.empty:
        raise ValueError("Input DataFrame X cannot be empty")

    if plot_type not in ['histogram', 'boxplot', 'correlation_heatmap', 'countplot']:
        raise ValueError(
            f"Invalid plot_type: {plot_type}. Must be one of: "
            "'histogram', 'boxplot', 'correlation_heatmap', 'countplot'"
        )

    # Handle large datasets
    if len(X) > 1_000_000:
        if plot_type in ['histogram', 'boxplot', 'correlation_heatmap']:
            # Sample for these plot types
            X = X.sample(n=100000, random_state=42)
        else:
            # Use Dask for countplot
            X = dd.from_pandas(X, chunksize=chunk_size)
            if y is not None:
                y = dd.from_pandas(pd.Series(y), chunks_size=chunk_size)

    # Get numerical columns
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
    if len(numerical_cols) == 0 and plot_type != 'countplot':
        raise ValueError("No numerical columns found in the dataset")

    if interactive:
        if plot_type == 'histogram':
            _plot_histogram_interactive(X, numerical_cols)
        elif plot_type == 'boxplot':
            _plot_boxplot_interactive(X, numerical_cols, highlight_outliers)
        elif plot_type == 'correlation_heatmap':
            _plot_correlation_heatmap_interactive(X, numerical_cols)
        elif plot_type == 'countplot':
            if y is None:
                raise ValueError("Target variable y is required for countplot")
            _plot_countplot_interactive(X, y)
    else:
        # Set up the plot style for matplotlib
        plt.style.use('seaborn')
        
        if plot_type == 'histogram':
            _plot_histogram(X, numerical_cols)
        elif plot_type == 'boxplot':
            _plot_boxplot(X, numerical_cols, highlight_outliers)
        elif plot_type == 'correlation_heatmap':
            _plot_correlation_heatmap(X, numerical_cols)
        elif plot_type == 'countplot':
            if y is None:
                raise ValueError("Target variable y is required for countplot")
            _plot_countplot(X, y)

        plt.tight_layout()
        plt.show()

def _detect_outliers(data: pd.Series) -> Dict[str, np.ndarray]:
    """
    Detect outliers using Z-score and IQR methods.
    
    Parameters
    ----------
    data : pd.Series
        Numerical data series.
        
    Returns
    -------
    Dict[str, np.ndarray]
        Dictionary containing outlier indices for each method.
    """
    # Z-score method (|z| > 3)
    z_scores = np.abs(stats.zscore(data.dropna()))
    z_score_outliers = np.where(z_scores > 3)[0]
    
    # IQR method
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    iqr_outliers = np.where((data < lower_bound) | (data > upper_bound))[0]
    
    return {
        'z_score': z_score_outliers,
        'iqr': iqr_outliers
    }

def _plot_histogram(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index) -> None:
    """Create histogram plots for numerical features using matplotlib."""
    n_cols = min(3, len(numerical_cols))
    n_rows = (len(numerical_cols) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    axes = axes.flatten()

    for idx, col in enumerate(numerical_cols):
        if isinstance(X, dd.DataFrame):
            with ProgressBar():
                data = X[col].compute()
        else:
            data = X[col]
        
        sns.histplot(data=data, ax=axes[idx], kde=True)
        axes[idx].set_title(f'Distribution of {col}')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Count')

    # Hide empty subplots
    for idx in range(len(numerical_cols), len(axes)):
        axes[idx].set_visible(False)

def _plot_histogram_interactive(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index) -> None:
    """Create interactive histogram plots for numerical features using Plotly."""
    if isinstance(X, dd.DataFrame):
        with ProgressBar():
            data = X[numerical_cols].compute()
    else:
        data = X[numerical_cols]
    
    n_cols = min(3, len(numerical_cols))
    n_rows = (len(numerical_cols) + n_cols - 1) // n_cols
    
    fig = make_subplots(
        rows=n_rows, 
        cols=n_cols,
        subplot_titles=[f'Distribution of {col}' for col in numerical_cols],
        specs=[[{"type": "histogram"}] for _ in range(n_rows * n_cols)]
    )
    
    for idx, col in enumerate(numerical_cols):
        row = idx // n_cols + 1
        col_idx = idx % n_cols + 1
        
        fig.add_trace(
            go.Histogram(
                x=data[col],
                name=col,
                nbinsx=30,
                histnorm='count',
                hovertemplate="Value: %{x}<br>Count: %{y}<extra></extra>"
            ),
            row=row, col=col_idx
        )
    
    fig.update_layout(
        height=300 * n_rows,
        width=1200,
        title_text="Distribution of Numerical Features",
        showlegend=False,
        template="plotly_white"
    )
    
    fig.show()

def _plot_boxplot(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index, highlight_outliers: bool) -> None:
    """Create boxplots for numerical features using matplotlib."""
    plt.figure(figsize=(15, 6))
    if isinstance(X, dd.DataFrame):
        with ProgressBar():
            data = X[numerical_cols].compute()
    else:
        data = X[numerical_cols]
    
    if highlight_outliers:
        # Create boxplot without outliers first
        bp = plt.boxplot(data, labels=numerical_cols, showfliers=False)
        
        # Add outliers with custom markers
        for i, col in enumerate(numerical_cols):
            outliers = _detect_outliers(data[col])
            all_outliers = np.unique(np.concatenate([outliers['z_score'], outliers['iqr']]))
            
            if len(all_outliers) > 0:
                outlier_values = data[col].iloc[all_outliers]
                plt.plot([i+1] * len(outlier_values), outlier_values, 'ro', 
                         markersize=8, alpha=0.7, label='Outlier' if i == 0 else "")
                
                # Add annotations for some outliers
                for j, val in enumerate(outlier_values[:5]):  # Limit to 5 annotations
                    plt.annotate(f'{val:.2f}', 
                                xy=(i+1, val),
                                xytext=(10, 10), 
                                textcoords='offset points',
                                fontsize=8)
    else:
        plt.boxplot(data, labels=numerical_cols)
    
    plt.xticks(rotation=45)
    plt.title('Boxplots of Numerical Features')
    if highlight_outliers:
        plt.legend()

def _plot_boxplot_interactive(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index, highlight_outliers: bool) -> None:
    """Create interactive boxplots for numerical features using Plotly."""
    if isinstance(X, dd.DataFrame):
        with ProgressBar():
            data = X[numerical_cols].compute()
    else:
        data = X[numerical_cols]
    
    fig = go.Figure()
    
    for col in numerical_cols:
        # Add boxplot
        fig.add_trace(
            go.Box(
                y=data[col],
                name=col,
                boxpoints='outliers' if not highlight_outliers else False,
                jitter=0.3,
                pointpos=-1.8,
                hovertemplate="Feature: %{x}<br>Value: %{y}<extra></extra>"
            )
        )
        
        # Add custom outliers if highlighting is enabled
        if highlight_outliers:
            outliers = _detect_outliers(data[col])
            all_outliers = np.unique(np.concatenate([outliers['z_score'], outliers['iqr']]))
            
            if len(all_outliers) > 0:
                outlier_values = data[col].iloc[all_outliers]
                fig.add_trace(
                    go.Scatter(
                        x=[col] * len(outlier_values),
                        y=outlier_values,
                        mode='markers',
                        marker=dict(
                            color='red',
                            size=10,
                            symbol='x'
                        ),
                        name=f'{col} Outliers',
                        hovertemplate="Feature: %{x}<br>Value: %{y}<br>Outlier<extra></extra>"
                    )
                )
    
    fig.update_layout(
        title="Boxplots of Numerical Features",
        yaxis_title="Value",
        xaxis_title="Feature",
        template="plotly_white",
        height=600,
        width=1200
    )
    
    fig.show()

def _plot_correlation_heatmap(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index) -> None:
    """Create correlation heatmap for numerical features using matplotlib."""
    plt.figure(figsize=(12, 10))
    if isinstance(X, dd.DataFrame):
        with ProgressBar():
            data = X[numerical_cols].compute()
    else:
        data = X[numerical_cols]
    
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')

def _plot_correlation_heatmap_interactive(X: Union[pd.DataFrame, dd.DataFrame], numerical_cols: pd.Index) -> None:
    """Create interactive correlation heatmap for numerical features using Plotly."""
    if isinstance(X, dd.DataFrame):
        with ProgressBar():
            data = X[numerical_cols].compute()
    else:
        data = X[numerical_cols]
    
    correlation_matrix = data.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hovertemplate="Feature 1: %{y}<br>Feature 2: %{x}<br>Correlation: %{z:.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Correlation Heatmap",
        xaxis_title="Feature",
        yaxis_title="Feature",
        template="plotly_white",
        height=800,
        width=1000
    )
    
    fig.show()

def _plot_countplot(X: Union[pd.DataFrame, dd.DataFrame], y: Union[pd.Series, dd.Series]) -> None:
    """Create countplot for categorical target variable using matplotlib."""
    if isinstance(X, dd.DataFrame):
        with ProgressBar():
            target_counts = y.value_counts().compute()
    else:
        target_counts = y.value_counts()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=target_counts.index, y=target_counts.values)
    plt.title('Target Variable Distribution')
    plt.xlabel('Target Class')
    plt.ylabel('Count')

def _plot_countplot_interactive(X: Union[pd.DataFrame, dd.DataFrame], y: Union[pd.Series, dd.Series]) -> None:
    """Create interactive countplot for categorical target variable using Plotly."""
    if isinstance(X, dd.DataFrame):
        with ProgressBar():
            target_counts = y.value_counts().compute()
    else:
        target_counts = y.value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=target_counts.index,
            y=target_counts.values,
            text=target_counts.values,
            textposition='auto',
            hovertemplate="Class: %{x}<br>Count: %{y}<extra></extra>"
        )
    ])
    
    fig.update_layout(
        title="Target Variable Distribution",
        xaxis_title="Target Class",
        yaxis_title="Count",
        template="plotly_white",
        height=500,
        width=800
    )
    
    fig.show() 