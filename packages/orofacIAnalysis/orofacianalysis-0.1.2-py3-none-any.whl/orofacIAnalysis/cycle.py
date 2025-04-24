"""Chewing cycle implementation for orofacIAnalysis."""

import json
import numpy as np
from scipy.signal import find_peaks


class Cycle:
    """Represents a chewing cycle with associated jaw movements and analysis.
    
    A chewing cycle is a sequence of jaw movements that occur between 
    specific start and end frames in a video. This class provides methods
    to analyze these movements and extract useful metrics.
    
    Attributes:
        start_frame: The frame number where the cycle begins
        end_frame: The frame number where the cycle ends
        jaw_movements: List of vertical jaw movement measurements
        jaw_positions: List of (x, y) jaw positions
        smoothed: Smoothed version of jaw movement data
        peaks: Indices of detected peaks in the jaw movement data
        valleys: Indices of detected valleys in the jaw movement data
        directions: List of chewing directions (0=left, 1=right, 2=middle)
        left: Count of left chews
        right: Count of right chews
        middle: Count of middle chews
    """
    
    def __init__(self, start_frame=0):
        """Initialize a new chewing cycle.
        
        Args:
            start_frame: Frame number where this cycle begins (default: 0)
        """
        self.start_frame = start_frame
        self.end_frame = 0

        self.jaw_movements = []
        self.jaw_positions = []

        self.smoothed = None
        self.peaks = None
        self.valleys = None

        self.directions = []
        self.left = 0
        self.right = 0
        self.middle = 0

    def set_end_frame(self, end_frame):
        """Set the end frame for this cycle.
        
        Args:
            end_frame: Frame number where this cycle ends
        """
        self.end_frame = end_frame

    def fit(self):
        """Process jaw movement data to detect peaks, valleys, and calculate metrics.
        
        This method applies smoothing to the jaw movement data, detects peaks and valleys,
        and prepares the data for further analysis.
        
        Raises:
            Exception: If no jaw movements have been recorded
        """
        if not self.jaw_movements:
            raise Exception("No jaw movements")

        self.smoothed = np.convolve(
            self.jaw_movements, np.ones(5) / 5, mode="same")
        self.peaks, _ = find_peaks(self.smoothed, prominence=10, distance=10)
        self.valleys, _ = find_peaks(-self.smoothed,
                                     prominence=10, distance=10)

    def cicly_stats(self):
        """Calculate statistics for this chewing cycle.
        
        This method counts the number of left, right, and middle chews
        based on the detected directions.
        """
        self.left = self.directions.count(0)  # 0 = "Left"
        self.right = self.directions.count(1)  # 1 = "Right"
        self.middle = self.directions.count(2)  # 2 = "Middle"

    def to_dict(self):
        """Convert cycle data to a dictionary.
        
        Returns:
            dict: Dictionary representation of the cycle data
        """
        return {
            "start_frame": self.start_frame,
            "end_frame": self.end_frame,
            "jaw_movements": self.jaw_movements,
            "peaks": self.peaks.tolist() if isinstance(self.peaks, np.ndarray) else self.peaks,
            "valleys": self.valleys.tolist() if isinstance(self.valleys, np.ndarray) else self.valleys,
            "directions": self.directions,
            "left": self.left,
            "right": self.right,
            "middle": self.middle,
        }

    def to_json(self):
        """Convert cycle data to a JSON string.
        
        Returns:
            str: JSON representation of the cycle data
        """
        return json.dumps(self.to_dict())

    def __str__(self):
        """Generate a string representation of the cycle.
        
        Returns:
            str: Human-readable description of the cycle
        """
        return (f"Jaw movements: {self.jaw_movements} \n"
                f"Jaw positions: {self.jaw_positions} \n"
                f"Peaks: {self.peaks} \n"
                f"Valleys: {self.valleys} \n"
                f"Directions: {self.directions} \n"
                f"Chew count: {len(self.directions)} \n"
                f"Start Frame: {self.start_frame} \n"
                f"End Frame: {self.end_frame}")