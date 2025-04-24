"""Base detector interfaces for orofacIAnalysis."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Union, Any
import numpy as np


@dataclass
class LandmarkPoint:
    """Standardized landmark point representation."""
    x: float  # Normalized x-coordinate (0-1)
    y: float  # Normalized y-coordinate (0-1)
    z: float = 0.0  # Normalized z-coordinate (0-1), if available
    visibility: float = 1.0  # Visibility/confidence score (0-1)


@dataclass
class LandmarkResult:
    """Container for landmark detection results."""
    landmarks: List[LandmarkPoint]  # List of detected landmarks
    confidence: float  # Overall detection confidence
    
    def get_landmark(self, index: int) -> Optional[LandmarkPoint]:
        """Get landmark at specified index if it exists."""
        if 0 <= index < len(self.landmarks):
            return self.landmarks[index]
        return None


class FaceDetector(ABC):
    """Abstract interface for face landmark detection."""
    
    @abstractmethod
    def process_image(self, image: np.ndarray) -> List[LandmarkResult]:
        """Process an image and return detected face landmarks.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            List of LandmarkResult, one for each detected face
        """
        pass
    
    @abstractmethod
    def get_landmark_indices(self) -> Dict[str, int]:
        """Get dictionary mapping landmark names to indices.
        
        Returns:
            Dictionary mapping landmark names to their indices
        """
        pass
    
    @abstractmethod
    def visualize(self, image: np.ndarray, results: List[LandmarkResult]) -> np.ndarray:
        """Draw landmarks on the image.
        
        Args:
            image: RGB image as numpy array
            results: List of LandmarkResult objects
            
        Returns:
            Image with drawn landmarks
        """
        pass


class HandDetector(ABC):
    """Abstract interface for hand detection."""
    
    @abstractmethod
    def process_image(self, image: np.ndarray) -> List[LandmarkResult]:
        """Process an image and return detected hand landmarks.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            List of LandmarkResult, one for each detected hand
        """
        pass
    
    @abstractmethod
    def get_landmark_indices(self) -> Dict[str, int]:
        """Get dictionary mapping landmark names to indices.
        
        Returns:
            Dictionary mapping landmark names to their indices
        """
        pass
    
    @abstractmethod
    def visualize(self, image: np.ndarray, results: List[LandmarkResult]) -> np.ndarray:
        """Draw landmarks on the image.
        
        Args:
            image: RGB image as numpy array
            results: List of LandmarkResult objects
            
        Returns:
            Image with drawn landmarks
        """
        pass


class PoseDetector(ABC):
    """Abstract interface for pose detection."""
    
    @abstractmethod
    def process_image(self, image: np.ndarray) -> List[LandmarkResult]:
        """Process an image and return detected pose landmarks.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            List of LandmarkResult, typically with one item for the detected pose
        """
        pass
    
    @abstractmethod
    def get_landmark_indices(self) -> Dict[str, int]:
        """Get dictionary mapping landmark names to indices.
        
        Returns:
            Dictionary mapping landmark names to their indices
        """
        pass
    
    @abstractmethod
    def visualize(self, image: np.ndarray, results: List[LandmarkResult]) -> np.ndarray:
        """Draw landmarks on the image.
        
        Args:
            image: RGB image as numpy array
            results: List of LandmarkResult objects
            
        Returns:
            Image with drawn landmarks
        """
        pass