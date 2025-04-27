import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_data_shape(data: pd.DataFrame, expected_shape: tuple) -> bool:
    """
    Validate the shape of the data against the expected shape.
    
    Args:
        data: Input DataFrame
        expected_shape: Expected shape of the data (rows, columns)
        
    Returns:
        True if the shape matches the expected shape, False otherwise
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    
    actual_shape = data.shape
    if actual_shape != expected_shape:
        logger.warning(f"Data shape mismatch: expected {expected_shape}, got {actual_shape}")
        return False
    
    return True 