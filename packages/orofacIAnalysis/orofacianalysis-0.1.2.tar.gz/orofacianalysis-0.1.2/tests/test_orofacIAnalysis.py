"""Basic tests for the package."""

import unittest
import numpy as np
from orofacIAnalysis import (
    Cycle,
    SmoothingMethods,
    apply_smoothing,
)


class TestCycle(unittest.TestCase):
    """Test the Cycle class."""

    def test_cycle_initialization(self):
        """Test that a Cycle object can be created."""
        cycle = Cycle(start_frame=10)
        self.assertEqual(cycle.start_frame, 10)
        self.assertEqual(cycle.end_frame, 0)
        self.assertEqual(cycle.jaw_movements, [])
        self.assertEqual(cycle.jaw_positions, [])

    def test_cycle_to_dict(self):
        """Test converting a Cycle to a dictionary."""
        cycle = Cycle(start_frame=10)
        cycle.set_end_frame(20)
        cycle_dict = cycle.to_dict()
        self.assertEqual(cycle_dict['start_frame'], 10)
        self.assertEqual(cycle_dict['end_frame'], 20)


class TestSmoothing(unittest.TestCase):
    """Test smoothing methods."""

    def test_smoothing_methods(self):
        """Test that basic smoothing methods work."""
        # Create a simple sine wave with noise
        x = np.linspace(0, 4 * np.pi, 100)
        signal = np.sin(x) + 0.2 * np.random.randn(len(x))
        
        # Apply different smoothing methods
        smooth_moving_avg = apply_smoothing(signal, "moving_average", window_size=5)
        smooth_expo = apply_smoothing(signal, "exponential", alpha=0.3)
        smooth_butter = apply_smoothing(signal, "butterworth", order=2, cutoff=0.1)
        
        # Check that outputs have the expected length
        self.assertEqual(len(smooth_moving_avg), len(signal))
        self.assertEqual(len(smooth_expo), len(signal))
        self.assertEqual(len(smooth_butter), len(signal))


if __name__ == '__main__':
    unittest.main()