"""Unit tests for facial analysis functionality."""

import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from orofacIAnalysis.face import FacialAnalyzer


class TestFacialAnalyzer:
    """Test cases for the FacialAnalyzer class."""

    def test_initialization(self):
        """Test that the FacialAnalyzer initializes properly."""
        analyzer = FacialAnalyzer()
        assert hasattr(analyzer, 'face_detector')
        assert analyzer.LANDMARKS is not None
        assert analyzer.REFERENCE_VALUES is not None
        assert analyzer.AVERAGE_HEAD_WIDTH_MM > 0

    def test_classify_value(self):
        """Test the classify_value method."""
        # Normal value (within 10% of reference)
        assert FacialAnalyzer.classify_value(95, 100) == "normal"
        assert FacialAnalyzer.classify_value(105, 100) == "normal"
        
        # Increased value (more than 10% above reference)
        assert FacialAnalyzer.classify_value(111, 100) == "increased"
        
        # Reduced value (more than 10% below reference)
        assert FacialAnalyzer.classify_value(89, 100) == "reduced"
        
        # Edge cases
        assert FacialAnalyzer.classify_value(90, 100) == "normal"
        assert FacialAnalyzer.classify_value(110, 100) == "normal"

    def test_calculate_distance(self):
        """Test the calculate_distance method."""
        # Create mock points
        class MockPoint:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        point1 = MockPoint(0.1, 0.2)
        point2 = MockPoint(0.4, 0.6)
        
        # Calculate distance with image dimensions 100x100
        distance = FacialAnalyzer.calculate_distance(point1, point2, 100, 100)
        
        # Expected result (using Pythagorean theorem)
        expected = np.sqrt((40 - 10)**2 + (60 - 20)**2)
        assert np.isclose(distance, expected)

    def test_analyze_image_no_face(self, mock_face_detector):
        """Test analyze_image when no face is detected."""
        # Configure the mock detector to return no faces
        mock_face_detector.process_image.return_value = []
        
        # Test that ValueError is raised when no face is detected
        analyzer = FacialAnalyzer(face_detector=mock_face_detector)
        with pytest.raises(ValueError, match="No face was detected"):
            analyzer.analyze_image(np.zeros((100, 100, 3), dtype=np.uint8))

    def test_analyze_image_results(self, mock_face_detector):
        """Test that analyze_image produces expected results structure."""
        # Create analyzer with mock detector
        analyzer = FacialAnalyzer(face_detector=mock_face_detector)
        
        # Call analyze_image with a dummy image
        results = analyzer.analyze_image(np.zeros((480, 640, 3), dtype=np.uint8))
        
        # Check that results have expected structure
        expected_measurements = [
            "middle_third", "lower_third", "face_height", "face_width",
            "left_eye_lip_distance", "right_eye_lip_distance",
            "upper_lip", "lower_lip"
        ]
        
        for measurement in expected_measurements:
            assert measurement in results
            assert "value" in results[measurement]
            assert "description" in results[measurement]
            assert results[measurement]["description"] in ["normal", "increased", "reduced"]