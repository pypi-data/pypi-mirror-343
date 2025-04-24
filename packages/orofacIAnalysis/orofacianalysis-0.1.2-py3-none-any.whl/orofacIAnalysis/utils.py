"""Utility functions for orofacIAnalysis."""

import numpy as np
import pandas as pd
from math import e
from scipy.interpolate import UnivariateSpline
from scipy.signal import butter, filtfilt
import io
from PIL import Image


def load_image(image_data):
    """Function to load images as PIL images.
    
    Args:
       image_data: Image in various formats
        
    Returns:
        Image: PIL Image
    """
    try:
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, np.ndarray):
            image = Image.fromarray(image_data)
        else:
            image = Image.open(io.BytesIO(image_data.read()))
    except Exception:
        image = Image.open(image_data)

    return image

def euclidian_distance(point1, point2):
    """Calculate Euclidean distance between two points.
    
    Args:
        point1: First point as (x, y) or array
        point2: Second point as (x, y) or array
        
    Returns:
        float: Euclidean distance
    """
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.sqrt(np.sum((point1 - point2) ** 2))


def axis_translation(new_origin, point):
    """Translate coordinate system by moving origin.
    
    Args:
        new_origin: (x, y) coordinates of the new origin
        point: (x, y) coordinates to be translated
        
    Returns:
        tuple: Translated coordinates (x_transformed, y_transformed)
    """
    x_new_origin, y_new_origin = new_origin
    x, y = point

    x_transformed = x - x_new_origin
    y_transformed = y - y_new_origin

    return (x_transformed, y_transformed)


def pandas_entropy(column):
    """Calculate Shannon entropy of a pandas Series or list.
    
    Args:
        column: Data values as pandas Series or list
        
    Returns:
        float: Shannon entropy value
    """
    vc = pd.Series(column).value_counts(normalize=True, sort=False)
    return -(vc * np.log(vc) / np.log(e)).sum()


def butterworth_filter(data, order=2, cutoff=0.1):
    """Apply Butterworth low-pass filter to signal.
    
    Args:
        data: Input signal data
        order: Filter order (default: 2)
        cutoff: Cutoff frequency (default: 0.1)
        
    Returns:
        ndarray: Filtered signal
    """
    b, a = butter(order, cutoff, btype="low", analog=False)
    return filtfilt(b, a, data)


def moving_average(data, window_size=51):
    """Apply simple moving average filter.
    
    Args:
        data: Input signal data
        window_size: Size of the moving window (default: 51)
        
    Returns:
        ndarray: Smoothed signal
    """
    return np.convolve(data, np.ones(window_size) / window_size, mode="same")


def exponential_smoothing(data, alpha=0.3):
    """Apply exponential smoothing.
    
    Args:
        data: Input signal data
        alpha: Smoothing factor (default: 0.3)
        
    Returns:
        ndarray: Smoothed signal
    """
    result = np.zeros_like(data)
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = alpha * data[i] + (1 - alpha) * result[i - 1]
    return result


def spline_smoothing(data, smooth_factor=5):
    """Apply spline interpolation smoothing.
    
    Args:
        data: Input signal data
        smooth_factor: Smoothing factor (default: 5)
        
    Returns:
        ndarray: Smoothed signal
    """
    x = np.arange(len(data))
    spl = UnivariateSpline(x, data, s=smooth_factor)
    return spl(x)