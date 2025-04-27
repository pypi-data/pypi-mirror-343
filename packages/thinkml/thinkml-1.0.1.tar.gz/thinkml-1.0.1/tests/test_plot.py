"""Tests for the plot function in the EDA module."""

import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from thinkml.eda.plot import plot

@pytest.fixture
def numerical_dataset():
    """Create a sample numerical dataset with missing values."""
    np.random.seed(42)
    n_samples = 1000
    data = {
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(5, 2, n_samples),
        'feature3': np.random.normal(-2, 0.5, n_samples)
    }
    df = pd.DataFrame(data)
    # Add some missing values
    df.loc[::10, 'feature1'] = np.nan
    df.loc[::15, 'feature2'] = np.nan
    return df

@pytest.fixture
def dataset_with_outliers():
    """Create a dataset with known outliers."""
    np.random.seed(42)
    n_samples = 1000
    data = {
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(5, 2, n_samples),
        'feature3': np.random.normal(-2, 0.5, n_samples)
    }
    df = pd.DataFrame(data)
    # Add outliers
    df.loc[0, 'feature1'] = 10  # Z-score outlier
    df.loc[1, 'feature2'] = 20  # Z-score outlier
    df.loc[2, 'feature3'] = 5   # Z-score outlier
    return df

@pytest.fixture
def categorical_target():
    """Create a sample categorical target variable."""
    np.random.seed(42)
    n_samples = 1000
    classes = ['A', 'B', 'C']
    # Create imbalanced classes
    probabilities = [0.6, 0.3, 0.1]
    return pd.Series(np.random.choice(classes, n_samples, p=probabilities))

@pytest.fixture
def large_dataset():
    """Create a large dataset (>1 million rows) for testing chunk processing."""
    np.random.seed(42)
    n_samples = 1_500_000
    data = {
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(5, 2, n_samples),
        'feature3': np.random.normal(-2, 0.5, n_samples)
    }
    return pd.DataFrame(data)

def test_histogram_plot_static(numerical_dataset):
    """Test static histogram plot generation for numerical features."""
    plot(numerical_dataset, plot_type='histogram', interactive=False)
    plt.close()

def test_histogram_plot_interactive(numerical_dataset):
    """Test interactive histogram plot generation for numerical features."""
    plot(numerical_dataset, plot_type='histogram', interactive=True)
    plt.close()

def test_boxplot_plot_static(numerical_dataset):
    """Test static boxplot generation."""
    plot(numerical_dataset, plot_type='boxplot', interactive=False)
    plt.close()

def test_boxplot_plot_interactive(numerical_dataset):
    """Test interactive boxplot generation."""
    plot(numerical_dataset, plot_type='boxplot', interactive=True)
    plt.close()

def test_boxplot_with_outliers_static(dataset_with_outliers):
    """Test static boxplot with outlier highlighting."""
    plot(dataset_with_outliers, plot_type='boxplot', highlight_outliers=True, interactive=False)
    plt.close()

def test_boxplot_with_outliers_interactive(dataset_with_outliers):
    """Test interactive boxplot with outlier highlighting."""
    plot(dataset_with_outliers, plot_type='boxplot', highlight_outliers=True, interactive=True)
    plt.close()

def test_correlation_heatmap_plot_static(numerical_dataset):
    """Test static correlation heatmap generation."""
    plot(numerical_dataset, plot_type='correlation_heatmap', interactive=False)
    plt.close()

def test_correlation_heatmap_plot_interactive(numerical_dataset):
    """Test interactive correlation heatmap generation."""
    plot(numerical_dataset, plot_type='correlation_heatmap', interactive=True)
    plt.close()

def test_countplot_plot_static(numerical_dataset, categorical_target):
    """Test static countplot generation for target variable."""
    plot(numerical_dataset, y=categorical_target, plot_type='countplot', interactive=False)
    plt.close()

def test_countplot_plot_interactive(numerical_dataset, categorical_target):
    """Test interactive countplot generation for target variable."""
    plot(numerical_dataset, y=categorical_target, plot_type='countplot', interactive=True)
    plt.close()

def test_large_dataset_chunk_processing(large_dataset):
    """Test chunk-based processing for large datasets."""
    # Test histogram with large dataset (should sample)
    plot(large_dataset, plot_type='histogram', interactive=False)
    plt.close()

    # Test histogram with large dataset (interactive)
    plot(large_dataset, plot_type='histogram', interactive=True)
    plt.close()

    # Test countplot with large dataset (should use Dask)
    categorical_target = pd.Series(np.random.choice(['A', 'B'], len(large_dataset)))
    plot(large_dataset, y=categorical_target, plot_type='countplot', interactive=False)
    plt.close()

    # Test countplot with large dataset (interactive)
    plot(large_dataset, y=categorical_target, plot_type='countplot', interactive=True)
    plt.close()

def test_invalid_plot_type(numerical_dataset):
    """Test that invalid plot_type raises ValueError."""
    with pytest.raises(ValueError):
        plot(numerical_dataset, plot_type='invalid_type')

def test_empty_dataframe():
    """Test that empty DataFrame raises ValueError."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError):
        plot(empty_df)

def test_countplot_without_target(numerical_dataset):
    """Test that countplot without target variable raises ValueError."""
    with pytest.raises(ValueError):
        plot(numerical_dataset, plot_type='countplot')

def test_no_numerical_columns():
    """Test that plotting with no numerical columns raises ValueError."""
    categorical_df = pd.DataFrame({
        'cat1': ['A', 'B', 'C'],
        'cat2': ['X', 'Y', 'Z']
    })
    with pytest.raises(ValueError):
        plot(categorical_df, plot_type='histogram') 