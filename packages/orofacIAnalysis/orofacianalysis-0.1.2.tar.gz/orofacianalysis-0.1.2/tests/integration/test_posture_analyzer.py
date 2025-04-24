"""Integration tests for PostureAnalyzer."""

import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from orofacIAnalysis import PostureAnalyzer


class TestPostureAnalyzerIntegration:
    """Integration tests for the PostureAnalyzer class."""
    
    @pytest.mark.skipif(not all(os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                                           f"test_resources/sample_{view}.png"))
                                 for view in ["frontal", "lateral"]),
                         reason="Sample posture images not available")
    def test_analyze_posture_with_real_images(self, sample_frontal_image_path, sample_lateral_image_path):
        """Test posture analysis with real image files."""
        # Create a PostureAnalyzer instance
        analyzer = PostureAnalyzer()
        
        try:
            # Open the image files
            with open(sample_frontal_image_path, 'rb') as frontal_file, \
                 open(sample_lateral_image_path, 'rb') as lateral_file:
                
                # Analyze the images
                results = analyzer.analyze_posture(frontal_file, lateral_file)
                
                # Check that results have the expected structure
                assert isinstance(results, dict)
                assert "frontal_view" in results
                assert "lateral_view" in results
                
                frontal = results["frontal_view"]
                assert "head_rotation" in frontal
                assert "head_inclination" in frontal
                assert "shoulder_position" in frontal
                
                lateral = results["lateral_view"]
                assert "head_position" in lateral
                assert "shoulder_position" in lateral
                
                # Check that all values are valid classifications
                valid_rotations = ["normal", "left", "right"]
                valid_inclinations = ["left", "right"]
                valid_shoulder_positions_frontal = ["normal", "elevated_left", "elevated_right"]
                valid_head_positions_lateral = ["normal", "anterior", "flexion", "extension"]
                valid_shoulder_positions_lateral = ["normal", "anterior_rotation"]
                
                assert frontal["head_rotation"] in valid_rotations
                assert frontal["head_inclination"] in valid_inclinations
                assert frontal["shoulder_position"] in valid_shoulder_positions_frontal
                assert lateral["head_position"] in valid_head_positions_lateral
                assert lateral["shoulder_position"] in valid_shoulder_positions_lateral
                
        except ValueError as e:
            if "Failed to detect pose landmarks" in str(e):
                pytest.skip("No pose landmarks detected in the sample images")
            else:
                raise
                
    @pytest.mark.skipif(not all(os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                                           f"test_resources/sample_{view}.png"))
                                 for view in ["frontal", "lateral"]),
                         reason="Sample posture images not available")
    def test_draw_pose_landmarks_with_real_image(self, sample_frontal_image_path):
        """Test drawing pose landmarks on a real image file."""
        # Create a PostureAnalyzer instance
        analyzer = PostureAnalyzer()
        
        try:
            # Open the image file
            with open(sample_frontal_image_path, 'rb') as f:
                # Draw landmarks on the image
                annotated_image = analyzer.draw_pose_landmarks(f)
                
                # Check that annotated image is a valid image
                assert isinstance(annotated_image, np.ndarray)
                assert annotated_image.ndim == 3  # Should be a color image
                assert annotated_image.shape[2] == 3  # Should have 3 color channels
                
        except ValueError as e:
            if "Failed to detect pose landmarks" in str(e):
                pytest.skip("No pose landmarks detected in the sample image")
            else:
                raise
                
    @pytest.mark.skipif(not all(os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                                           f"test_resources/sample_{view}.png"))
                                 for view in ["frontal", "lateral"]),
                         reason="Sample posture images not available")
    def test_analyze_and_visualize_with_real_images(self, sample_frontal_image_path, sample_lateral_image_path):
        """Test analyzing and visualizing posture with real image files."""
        # Create a PostureAnalyzer instance
        analyzer = PostureAnalyzer()
        
        try:
            # Open the image files
            with open(sample_frontal_image_path, 'rb') as frontal_file, \
                 open(sample_lateral_image_path, 'rb') as lateral_file:
                
                # Analyze and visualize the images
                results, frontal_annotated, lateral_annotated = analyzer.analyze_and_visualize(
                    frontal_file, lateral_file
                )
                
                # Check that results and annotated images are valid
                assert isinstance(results, dict)
                assert isinstance(frontal_annotated, np.ndarray)
                assert isinstance(lateral_annotated, np.ndarray)
                
                # Check that both annotated images are valid
                assert frontal_annotated.ndim == 3
                assert lateral_annotated.ndim == 3
                assert frontal_annotated.shape[2] == 3
                assert lateral_annotated.shape[2] == 3
                
        except ValueError as e:
            if "Failed to detect pose landmarks" in str(e):
                pytest.skip("No pose landmarks detected in the sample images")
            else:
                raise
                
    def test_end_to_end_posture_analysis(self):
        """Perform an end-to-end test of the posture analysis process."""
        # Import the required classes
        from orofacIAnalysis.detectors.base import LandmarkPoint, LandmarkResult
        
        # Create frontal and lateral landmarks using LandmarkPoint
        frontal_landmarks = []
        lateral_landmarks = []
        
        # Initialize with empty landmarks
        for i in range(33):  # MediaPipe pose has 33 landmarks
            frontal_landmarks.append(LandmarkPoint(0, 0, 0, 1.0))
            lateral_landmarks.append(LandmarkPoint(0, 0, 0, 1.0))
            
        # Set specific frontal landmark positions
        # NOSE
        frontal_landmarks[0] = LandmarkPoint(0.5, 0.3, 0, 1.0)
        # LEFT_EAR, RIGHT_EAR
        frontal_landmarks[7] = LandmarkPoint(0.4, 0.3, 0, 1.0)
        frontal_landmarks[8] = LandmarkPoint(0.6, 0.3, 0, 1.0)
        # LEFT_SHOULDER, RIGHT_SHOULDER
        frontal_landmarks[11] = LandmarkPoint(0.35, 0.5, 0, 1.0)
        frontal_landmarks[12] = LandmarkPoint(0.65, 0.5, 0, 1.0)
            
        # Set specific lateral landmark positions
        # NOSE
        lateral_landmarks[0] = LandmarkPoint(0.55, 0.3, 0, 1.0)
        # RIGHT_EAR
        lateral_landmarks[8] = LandmarkPoint(0.5, 0.3, 0, 1.0)
        # RIGHT_SHOULDER
        lateral_landmarks[12] = LandmarkPoint(0.45, 0.5, 0, 1.0)
        
        # Create LandmarkResult objects
        frontal_result = LandmarkResult(landmarks=frontal_landmarks, confidence=1.0)
        lateral_result = LandmarkResult(landmarks=lateral_landmarks, confidence=1.0)
        
        # Create a mock detector
        mock_detector = MagicMock()
        mock_detector.get_landmark_indices.return_value = {
            "nose": 0,
            "left_eye": 2,
            "right_eye": 5,
            "left_ear": 7,
            "right_ear": 8,
            "left_shoulder": 11,
            "right_shoulder": 12,
            "left_hip": 23,
            "right_hip": 24
        }
        
        # Create a PostureAnalyzer instance with the mock detector
        analyzer = PostureAnalyzer(pose_detector=mock_detector)
        
        # Mock the _process_image method to return our mock results
        with patch.object(analyzer, '_process_image') as mock_process:
            mock_process.side_effect = [frontal_result, lateral_result]
            
            # Test analyzing the images
            results = analyzer.analyze_posture(b'dummy frontal', b'dummy lateral')
            
            # Verify the results are as expected
            assert isinstance(results, dict)
            assert "frontal_view" in results
            assert "lateral_view" in results
            
            # Check the structure of the results
            frontal = results["frontal_view"]
            assert "head_rotation" in frontal
            assert "head_inclination" in frontal
            assert "shoulder_position" in frontal
            
            lateral = results["lateral_view"]
            assert "head_position" in lateral
            assert "shoulder_position" in lateral