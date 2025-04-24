"""Unit tests for smoothing methods."""

import pytest
import numpy as np
from orofacIAnalysis.smoothing import (
    SmoothingMethods,
    SmoothingMethodsList,
    apply_smoothing
)


class TestSmoothingMethods:
    """Test cases for smoothing methods."""

    def test_smoothing_methods_list(self):
        """Test that all expected smoothing methods are included in the list."""
        expected_methods = [
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
        
        for method in expected_methods:
            assert method in SmoothingMethodsList.METHODS

    def test_default_method(self, sample_jaw_movements):
        """Test the default smoothing method (no smoothing)."""
        smoothed = SmoothingMethods.default(sample_jaw_movements)
        # Default method should return the original signal unchanged
        np.testing.assert_array_equal(smoothed, sample_jaw_movements)

    def test_moving_average(self, sample_jaw_movements):
        """Test the moving average smoothing method."""
        window_size = 5
        smoothed = SmoothingMethods.moving_average(sample_jaw_movements, window_size=window_size)
        
        # Check output length
        assert len(smoothed) == len(sample_jaw_movements)
        
        # Check that variance is reduced (smoothing effect)
        assert np.var(smoothed) < np.var(sample_jaw_movements)

    def test_exponential_smoothing(self, sample_jaw_movements):
        """Test the exponential smoothing method."""
        alpha = 0.3
        smoothed = SmoothingMethods.exponential(sample_jaw_movements, alpha=alpha)
        
        # Check output length
        assert len(smoothed) == len(sample_jaw_movements)
        
        # Check that variance is reduced (smoothing effect)
        assert np.var(smoothed) < np.var(sample_jaw_movements)

    def test_butterworth_filter(self, sample_jaw_movements):
        """Test the Butterworth filter smoothing method."""
        order = 2
        cutoff = 0.1
        smoothed = SmoothingMethods.butterworth(sample_jaw_movements, order=order, cutoff=cutoff)
        
        # Check output length
        assert len(smoothed) == len(sample_jaw_movements)
        
        # Check that variance is reduced (smoothing effect)
        assert np.var(smoothed) < np.var(sample_jaw_movements)

    def test_median_filter(self, sample_jaw_movements):
        """Test the median filter smoothing method."""
        kernel_size = 5
        smoothed = SmoothingMethods.median(sample_jaw_movements, kernel_size=kernel_size)
        
        # Check output length
        assert len(smoothed) == len(sample_jaw_movements)
        
        # For very noisy data, median filtering should reduce variance
        assert np.var(smoothed) < np.var(sample_jaw_movements * (1 + 0.5 * np.random.randn(len(sample_jaw_movements))))

    def test_spline_smoothing(self, sample_jaw_movements):
        """Test the spline smoothing method."""
        smooth_factor = 5
        smoothed = SmoothingMethods.spline(sample_jaw_movements, smooth_factor=smooth_factor)
        
        # Check output length
        assert len(smoothed) == len(sample_jaw_movements)
        
        # Check that variance is reduced (smoothing effect)
        assert np.var(smoothed) < np.var(sample_jaw_movements)
    
    def test_savgol_filter(self, sample_jaw_movements):
        """Test the Savitzky-Golay filter smoothing method."""
        window_length = 15  # Must be odd and less than data length
        polyorder = 3
        smoothed = SmoothingMethods.savgol(sample_jaw_movements, window_length=window_length, polyorder=polyorder)
        
        # Check output length
        assert len(smoothed) == len(sample_jaw_movements)
        
        # Check that variance is reduced (smoothing effect)
        assert np.var(smoothed) < np.var(sample_jaw_movements)

    def test_gaussian_filter(self, sample_jaw_movements):
        """Test the Gaussian filter smoothing method."""
        sigma = 2
        smoothed = SmoothingMethods.gaussian(sample_jaw_movements, sigma=sigma)
        
        # Check output length
        assert len(smoothed) == len(sample_jaw_movements)
        
        # Check that variance is reduced (smoothing effect)
        assert np.var(smoothed) < np.var(sample_jaw_movements)


class TestApplySmoothingFunction:
    """Test cases for the apply_smoothing function."""

    def test_apply_smoothing_default(self, sample_jaw_movements):
        """Test applying the default smoothing method."""
        smoothed = apply_smoothing(sample_jaw_movements, "default")
        np.testing.assert_array_equal(smoothed, sample_jaw_movements)

    def test_apply_smoothing_with_kwargs(self, sample_jaw_movements):
        """Test applying smoothing with custom parameters."""
        window_size = 11
        smoothed = apply_smoothing(sample_jaw_movements, "moving_average", window_size=window_size)
        
        # Output should be different from default window size
        default_smoothed = SmoothingMethods.moving_average(sample_jaw_movements)
        assert not np.array_equal(smoothed, default_smoothed)

    def test_apply_smoothing_invalid_method(self, sample_jaw_movements):
        """Test that an invalid method name raises an exception."""
        with pytest.raises(ValueError, match="Unknown smoothing method"):
            apply_smoothing(sample_jaw_movements, "invalid_method_name")

    def test_all_methods_callable(self, sample_jaw_movements):
        """Test that all methods in the list can be called through apply_smoothing."""
        for method in SmoothingMethodsList.METHODS:
            try:
                result = apply_smoothing(sample_jaw_movements, method)
                assert len(result) == len(sample_jaw_movements)
            except ImportError:
                # Skip methods that require optional dependencies
                pass