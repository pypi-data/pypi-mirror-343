"""Signal smoothing methods for orofacIAnalysis."""

import numpy as np
from dataclasses import dataclass
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt, savgol_filter
import statsmodels.api as sm

# Import smoothing methods from utils
from orofacIAnalysis.utils import (
    butterworth_filter,
    exponential_smoothing,
    moving_average,
    spline_smoothing,
)

# Optional dependency - we'll handle its potential absence
try:
    from PyEMD.EMD import EMD
    HAS_EMD = True
except ImportError:
    HAS_EMD = False


@dataclass(frozen=True)
class SmoothingMethodsList:
    """List of available smoothing methods."""

    METHODS = [
        "savgol",
        "gaussian",
        "emd",
        "lowess",
        "moving_average",
        "exponential",
        "spline",
        "butterworth",
        "median",
        "default",
    ]


class SmoothingMethods:
    """Collection of signal smoothing methods for jaw movement data.
    
    This class provides a unified interface to various signal smoothing
    techniques that can be applied to jaw movement time series data.
    """

    @staticmethod
    def savgol(jaw_movements, window_length=25, polyorder=3):
        """Apply Savitzky-Golay filter."""
        return savgol_filter(jaw_movements, window_length=window_length, polyorder=polyorder)
    
    @staticmethod
    def gaussian(jaw_movements, sigma=5):
        """Apply Gaussian filter."""
        return gaussian_filter(jaw_movements, sigma=sigma)
    
    @staticmethod
    def emd(jaw_movements):
        """Apply Empirical Mode Decomposition."""
        if not HAS_EMD:
            raise ImportError("PyEMD is required for EMD smoothing. Install with pip install PyEMD")
        emd = EMD()
        emd_result = emd(np.array(jaw_movements))[1:]
        return np.sum(emd_result, axis=0)
    
    @staticmethod
    def lowess(jaw_movements, frac=0.05):
        """Apply Locally Weighted Scatterplot Smoothing."""
        return sm.nonparametric.lowess(
            jaw_movements, np.arange(len(jaw_movements)), frac=frac
        )[:, 1]
    
    @staticmethod
    def moving_average(jaw_movements, window_size=51):
        """Apply moving average smoothing."""
        return moving_average(jaw_movements, window_size=window_size)
    
    @staticmethod
    def exponential(jaw_movements, alpha=0.3):
        """Apply exponential smoothing."""
        return exponential_smoothing(jaw_movements, alpha=alpha)
    
    @staticmethod
    def spline(jaw_movements, smooth_factor=5):
        """Apply spline smoothing."""
        return spline_smoothing(jaw_movements, smooth_factor=smooth_factor)
    
    @staticmethod
    def butterworth(jaw_movements, order=2, cutoff=0.1):
        """Apply Butterworth filter."""
        return butterworth_filter(jaw_movements, order=order, cutoff=cutoff)
    
    @staticmethod
    def median(jaw_movements, kernel_size=7):
        """Apply median filter."""
        return medfilt(jaw_movements, kernel_size=kernel_size)
    
    @staticmethod
    def default(jaw_movements):
        """Return unmodified signal (no smoothing)."""
        return jaw_movements


def apply_smoothing(jaw_movements, method_name, **kwargs):
    """Apply the specified smoothing method to jaw movement data.
    
    Args:
        jaw_movements: Array of jaw movement data
        method_name: String name of the smoothing method to use
        **kwargs: Additional parameters to pass to the smoothing method
        
    Returns:
        ndarray: Smoothed jaw movement data
        
    Raises:
        ValueError: If the specified method is not recognized
    """
    # Build the method mapping
    method_map = {
        "savgol": SmoothingMethods.savgol,
        "gaussian": SmoothingMethods.gaussian,
        "emd": SmoothingMethods.emd,
        "lowess": SmoothingMethods.lowess,
        "moving_average": SmoothingMethods.moving_average,
        "exponential": SmoothingMethods.exponential,
        "spline": SmoothingMethods.spline,
        "butterworth": SmoothingMethods.butterworth,
        "median": SmoothingMethods.median,
        "default": SmoothingMethods.default,
    }
    
    if method_name not in method_map:
        valid_methods = list(method_map.keys())
        raise ValueError(f"Unknown smoothing method: {method_name}. Valid methods are: {valid_methods}")
    
    # Apply the selected method with any provided kwargs
    return method_map[method_name](jaw_movements, **kwargs)