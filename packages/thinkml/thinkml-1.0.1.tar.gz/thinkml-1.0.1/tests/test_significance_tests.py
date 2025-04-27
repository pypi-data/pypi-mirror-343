"""
Tests for statistical significance tests.
"""

import pytest
import numpy as np
from thinkml.statistics.significance_tests import (
    t_test,
    anova_test,
    confidence_interval,
    TTestResult,
    AnovaResult
)

@pytest.fixture
def two_groups():
    """Create two groups for t-test."""
    np.random.seed(42)
    group1 = np.random.normal(0, 1, 100)
    group2 = np.random.normal(1, 1, 100)
    return group1, group2

@pytest.fixture
def multiple_groups():
    """Create multiple groups for ANOVA."""
    np.random.seed(42)
    groups = [
        np.random.normal(0, 1, 100),
        np.random.normal(1, 1, 100),
        np.random.normal(2, 1, 100)
    ]
    return groups

def test_t_test(two_groups):
    """Test t-test functionality."""
    group1, group2 = two_groups
    result = t_test(group1, group2)
    
    assert isinstance(result, TTestResult)
    assert isinstance(result.statistic, float)
    assert isinstance(result.p_value, float)
    assert isinstance(result.degrees_of_freedom, int)
    assert isinstance(result.mean_difference, float)
    assert isinstance(result.confidence_interval, tuple)
    assert len(result.confidence_interval) == 2
    
    # Test with equal_var=False
    result_unequal = t_test(group1, group2, equal_var=False)
    assert isinstance(result_unequal, TTestResult)
    assert result_unequal.degrees_of_freedom != result.degrees_of_freedom

def test_t_test_significance(two_groups):
    """Test t-test significance levels."""
    group1, group2 = two_groups
    
    # Test different significance levels
    for alpha in [0.01, 0.05, 0.1]:
        result = t_test(group1, group2, alpha=alpha)
        assert isinstance(result.p_value, float)
        assert 0 <= result.p_value <= 1

def test_anova_test(multiple_groups):
    """Test ANOVA test functionality."""
    result = anova_test(multiple_groups)
    
    assert isinstance(result, AnovaResult)
    assert isinstance(result.statistic, float)
    assert isinstance(result.p_value, float)
    assert isinstance(result.degrees_of_freedom, tuple)
    assert len(result.degrees_of_freedom) == 2
    assert isinstance(result.mean_squares, tuple)
    assert len(result.mean_squares) == 2
    assert isinstance(result.f_ratio, float)

def test_anova_test_significance(multiple_groups):
    """Test ANOVA test significance levels."""
    # Test different significance levels
    for alpha in [0.01, 0.05, 0.1]:
        result = anova_test(multiple_groups, alpha=alpha)
        assert isinstance(result.p_value, float)
        assert 0 <= result.p_value <= 1

def test_confidence_interval():
    """Test confidence interval calculation."""
    data = np.random.normal(0, 1, 100)
    
    # Test t-distribution method
    ci_t = confidence_interval(data, method='t')
    assert isinstance(ci_t, tuple)
    assert len(ci_t) == 2
    assert ci_t[0] < ci_t[1]
    
    # Test normal distribution method
    ci_z = confidence_interval(data, method='z')
    assert isinstance(ci_z, tuple)
    assert len(ci_z) == 2
    assert ci_z[0] < ci_z[1]

def test_confidence_interval_significance():
    """Test confidence interval with different significance levels."""
    data = np.random.normal(0, 1, 100)
    
    # Test different significance levels
    for alpha in [0.01, 0.05, 0.1]:
        ci = confidence_interval(data, alpha=alpha)
        assert isinstance(ci, tuple)
        assert len(ci) == 2
        assert ci[0] < ci[1]

def test_t_test_edge_cases():
    """Test t-test with edge cases."""
    # Test with identical groups
    group1 = np.array([1, 2, 3])
    group2 = np.array([1, 2, 3])
    result = t_test(group1, group2)
    assert result.p_value > 0.05  # Should not be significant
    
    # Test with very different groups
    group1 = np.array([1, 2, 3])
    group2 = np.array([10, 11, 12])
    result = t_test(group1, group2)
    assert result.p_value < 0.05  # Should be significant

def test_anova_test_edge_cases():
    """Test ANOVA with edge cases."""
    # Test with identical groups
    groups = [
        np.array([1, 2, 3]),
        np.array([1, 2, 3]),
        np.array([1, 2, 3])
    ]
    result = anova_test(groups)
    assert result.p_value > 0.05  # Should not be significant
    
    # Test with very different groups
    groups = [
        np.array([1, 2, 3]),
        np.array([10, 11, 12]),
        np.array([20, 21, 22])
    ]
    result = anova_test(groups)
    assert result.p_value < 0.05  # Should be significant

def test_confidence_interval_edge_cases():
    """Test confidence interval with edge cases."""
    # Test with constant data
    data = np.array([1, 1, 1])
    ci = confidence_interval(data)
    assert ci[0] == ci[1]  # Should have zero width
    
    # Test with large spread
    data = np.array([-100, 0, 100])
    ci = confidence_interval(data)
    assert ci[1] - ci[0] > 0  # Should have positive width

def test_invalid_inputs():
    """Test functions with invalid inputs."""
    # Test t-test with empty arrays
    with pytest.raises(ValueError):
        t_test(np.array([]), np.array([]))
    
    # Test ANOVA with empty groups
    with pytest.raises(ValueError):
        anova_test([])
    
    # Test confidence interval with empty data
    with pytest.raises(ValueError):
        confidence_interval(np.array([]))
    
    # Test invalid confidence interval method
    with pytest.raises(ValueError):
        confidence_interval(np.array([1, 2, 3]), method='invalid') 