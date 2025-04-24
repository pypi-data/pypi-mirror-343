"""Integration tests for FacialAnalyzer."""

import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from orofacIAnalysis import FacialAnalyzer
from pathlib import Path




class TestFacialAnalyzerIntegration:
    """Integration tests for the FacialAnalyzer class."""
    
    @pytest.mark.skipif(not os.path.exists(Path(__file__).parent.parent / "test_resources" / "sample_face.jpg"),
                         reason="Sample face image not available")
    def test_analyze_image_with_real_image(self, sample_face_image_path):
        """Test facial analysis with a real image file."""
        # Create a FacialAnalyzer instance
        analyzer = FacialAnalyzer()

        try:
            # Open the image file
            with open(sample_face_image_path, 'rb') as f:
                # Analyze the image
                results = analyzer.analyze_image(f)
                
                # Check that results have the expected structure
                assert isinstance(results, dict)
                
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
                    assert isinstance(results[measurement]["value"], float)
                            
        except ValueError as e:
            if "No face was detected" in str(e):
                pytest.skip("No face detected in the sample image")
            else:
                raise
                
    # @pytest.mark.skipif(not os.path.exists(os.path.join("tests", "test_resources", "sample_face.jpg")),
    #                      reason="Sample face image not available")
    def test_draw_landmarks_with_real_image(self, sample_face_image_path):
        """Test drawing landmarks on a real image file."""
        # Create a FacialAnalyzer instance
        analyzer = FacialAnalyzer()
        
        try:
            # Open the image file
            with open(sample_face_image_path, 'rb') as f:
                # Draw landmarks on the image
                annotated_image = analyzer.draw_landmarks(f)

                # Check that annotated image is a valid image
                assert isinstance(annotated_image, np.ndarray)
                assert annotated_image.ndim == 3  # Should be a color image
                assert annotated_image.shape[2] == 3  # Should have 3 color channels
                
        except ValueError as e:
            if "No face was detected" in str(e):
                pytest.skip("No face detected in the sample image")
            else:
                raise
                
    def test_end_to_end_facial_analysis(self):
        """Perform an end-to-end test of the facial analysis process."""
        # Import the required classes
        from orofacIAnalysis.detectors.base import LandmarkPoint, LandmarkResult
        
        # Create landmarks using LandmarkPoint
        landmarks = []
        # Initialize with empty landmarks (MediaPipe face mesh has 468 landmarks)
        for i in range(500):
            landmarks.append(LandmarkPoint(0, 0, 0, 1.0))
        
        # Set key landmark points with realistic coordinates
        landmarks[2] = LandmarkPoint(0.5, 0.6, 0, 1.0)    # subnasal
        landmarks[4] = LandmarkPoint(0.5, 0.5, 0, 1.0)    # nose tip
        landmarks[9] = LandmarkPoint(0.5, 0.3, 0, 1.0)    # glabella
        landmarks[13] = LandmarkPoint(0.5, 0.65, 0, 1.0)  # lowest upper lip
        landmarks[14] = LandmarkPoint(0.5, 0.7, 0, 1.0)   # highest lower lip
        landmarks[61] = LandmarkPoint(0.4, 0.65, 0, 1.0)  # left mouth corner
        landmarks[116] = LandmarkPoint(0.3, 0.5, 0, 1.0)  # left face side
        landmarks[152] = LandmarkPoint(0.5, 0.85, 0, 1.0) # gnathion (chin)
        landmarks[226] = LandmarkPoint(0.4, 0.45, 0, 1.0) # left eye corner
        landmarks[291] = LandmarkPoint(0.6, 0.65, 0, 1.0) # right mouth corner
        landmarks[345] = LandmarkPoint(0.7, 0.5, 0, 1.0)  # right face side
        landmarks[446] = LandmarkPoint(0.6, 0.45, 0, 1.0) # right eye corner
        
        # Create a LandmarkResult
        face_result = LandmarkResult(landmarks=landmarks, confidence=1.0)
        
        # Create a mock detector
        mock_detector = MagicMock()
        mock_detector.get_landmark_indices.return_value = {
            "left_face_side": 116,
            "right_face_side": 345,
            "glabella": 9,
            "subnasal": 2,
            "gnathion": 152,
            "left_eye_corner": 226,
            "right_eye_corner": 446,
            "left_mouth_corner": 61,
            "right_mouth_corner": 291,
            "lowest_upper_lip": 13,
            "highest_lower_lip": 14,
            "nose": 4
        }
        mock_detector.process_image.return_value = [face_result]
        
        # Create a FacialAnalyzer instance with the mock detector
        analyzer = FacialAnalyzer(face_detector=mock_detector)
        
        # Test analyzing the image with a dummy image
        with patch('cv2.cvtColor', return_value=np.zeros((480, 640, 3), dtype=np.uint8)):
            results = analyzer.analyze_image(np.zeros((480, 640, 3), dtype=np.uint8))
            
            # Verify the results are as expected
            assert isinstance(results, dict)

            # Check that all expected measurements are present
            expected_measurements = [
                "middle_third", "lower_third", "face_height", "face_width",
                "left_eye_lip_distance", "right_eye_lip_distance",
                "upper_lip", "lower_lip"
            ]
            
            for measurement in expected_measurements:
                assert measurement in results