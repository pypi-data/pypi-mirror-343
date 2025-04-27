"""
Optimization module for ThinkML.
"""

from .early_stopping import EarlyStopping
from .gpu_acceleration import GPUAccelerator
from .parallel_processing import ParallelProcessor

__all__ = [
    'EarlyStopping',
    'GPUAccelerator',
    'ParallelProcessor'
] 