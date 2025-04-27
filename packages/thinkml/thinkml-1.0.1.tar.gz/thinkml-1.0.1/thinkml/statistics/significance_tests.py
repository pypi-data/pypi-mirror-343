"""
Statistical significance tests and analysis.
"""

import numpy as np
from typing import List, Tuple, Union
from scipy import stats
from dataclasses import dataclass

@dataclass
class TTestResult:
    """Results from a t-test."""
    statistic: float
    p_value: float
    degrees_of_freedom: int
    mean_difference: float
    confidence_interval: Tuple[float, float]

@dataclass
class AnovaResult:
    """Results from an ANOVA test."""
    statistic: float
    p_value: float
    degrees_of_freedom: Tuple[int, int]
    mean_squares: Tuple[float, float]
    f_ratio: float

def t_test(
    group1: np.ndarray,
    group2: np.ndarray,
    alpha: float = 0.05,
    equal_var: bool = True
) -> TTestResult:
    """
    Perform a t-test to compare two groups.
    
    Parameters
    ----------
    group1 : np.ndarray
        First group of samples
    group2 : np.ndarray
        Second group of samples
    alpha : float, optional
        Significance level
    equal_var : bool, optional
        Whether to assume equal variances
        
    Returns
    -------
    TTestResult
        Results of the t-test
    """
    # Convert inputs to numpy arrays
    group1 = np.asarray(group1)
    group2 = np.asarray(group2)
    
    # Calculate basic statistics
    n1, n2 = len(group1), len(group2)
    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    # Calculate pooled variance if equal_var is True
    if equal_var:
        pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
        se = np.sqrt(pooled_var * (1/n1 + 1/n2))
        df = n1 + n2 - 2
    else:
        se = np.sqrt(var1/n1 + var2/n2)
        df = (var1/n1 + var2/n2)**2 / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1))
    
    # Calculate t-statistic
    t_stat = (mean1 - mean2) / se
    
    # Calculate p-value
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
    
    # Calculate confidence interval
    ci = stats.t.interval(1 - alpha, df, loc=mean1 - mean2, scale=se)
    
    return TTestResult(
        statistic=t_stat,
        p_value=p_value,
        degrees_of_freedom=df,
        mean_difference=mean1 - mean2,
        confidence_interval=ci
    )

def anova_test(groups: List[np.ndarray], alpha: float = 0.05) -> AnovaResult:
    """
    Perform one-way ANOVA test to compare multiple groups.
    
    Parameters
    ----------
    groups : List[np.ndarray]
        List of groups to compare
    alpha : float, optional
        Significance level
        
    Returns
    -------
    AnovaResult
        Results of the ANOVA test
    """
    # Convert inputs to numpy arrays
    groups = [np.asarray(group) for group in groups]
    
    # Calculate basic statistics
    n_groups = len(groups)
    n_total = sum(len(group) for group in groups)
    
    # Calculate grand mean
    grand_mean = np.mean(np.concatenate(groups))
    
    # Calculate between-group sum of squares
    ss_between = sum(len(group) * (np.mean(group) - grand_mean)**2 for group in groups)
    df_between = n_groups - 1
    ms_between = ss_between / df_between
    
    # Calculate within-group sum of squares
    ss_within = sum(np.sum((group - np.mean(group))**2) for group in groups)
    df_within = n_total - n_groups
    ms_within = ss_within / df_within
    
    # Calculate F-statistic
    f_stat = ms_between / ms_within
    
    # Calculate p-value
    p_value = 1 - stats.f.cdf(f_stat, df_between, df_within)
    
    return AnovaResult(
        statistic=f_stat,
        p_value=p_value,
        degrees_of_freedom=(df_between, df_within),
        mean_squares=(ms_between, ms_within),
        f_ratio=f_stat
    )

def confidence_interval(
    data: np.ndarray,
    alpha: float = 0.05,
    method: str = 't'
) -> Tuple[float, float]:
    """
    Calculate confidence interval for a sample.
    
    Parameters
    ----------
    data : np.ndarray
        Sample data
    alpha : float, optional
        Significance level
    method : str, optional
        Method to use ('t' for t-distribution, 'z' for normal distribution)
        
    Returns
    -------
    Tuple[float, float]
        Confidence interval (lower, upper)
    """
    data = np.asarray(data)
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    if method == 't':
        # Use t-distribution for small samples
        ci = stats.t.interval(1 - alpha, n - 1, loc=mean, scale=std/np.sqrt(n))
    else:
        # Use normal distribution for large samples
        ci = stats.norm.interval(1 - alpha, loc=mean, scale=std/np.sqrt(n))
    
    return ci 