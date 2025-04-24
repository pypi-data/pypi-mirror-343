"""Unit tests for posture analysis functionality."""

import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from orofacIAnalysis.posture import PostureAnalyzer


class TestPostureAnalyzer:
    """Test cases for the PostureAnalyzer class."""

    def test_initialization(self):
        """Test that the PostureAnalyzer initializes properly."""
        analyzer = PostureAnalyzer()
        assert hasattr(analyzer, 'pose_detector')
        assert hasattr(analyzer, 'landmarks_map')

    def test_analyze_frontal_head_rotation(self, mock_pose_landmarks):
        """Test the analysis of frontal head rotation."""
        analyzer = PostureAnalyzer()
        
        # Test with default mock landmarks (should be balanced)
        rotation = analyzer._analyze_frontal_head_rotation(mock_pose_landmarks.landmark)
        assert rotation == "normal"
        
        # Test with head rotated left
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        # Move right ear farther from nose
        mock_landmarks[analyzer.landmarks_map["right_ear"]].x = 0.7
        rotation = analyzer._analyze_frontal_head_rotation(mock_landmarks)
        assert rotation == "left"
        
        # Test with head rotated right
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        # Move left ear farther from nose
        # Move left ear much farther from nose than right ear
        mock_landmarks[analyzer.landmarks_map["left_ear"]].x = 0.3
        mock_landmarks[analyzer.landmarks_map["right_ear"]].x = 0.55
        mock_landmarks[analyzer.landmarks_map["nose"]].x = 0.5
        rotation = analyzer._analyze_frontal_head_rotation(mock_landmarks)
        assert rotation == "right"

    def test_analyze_frontal_head_inclination(self, mock_pose_landmarks):
        """Test the analysis of frontal head inclination."""
        analyzer = PostureAnalyzer()
        
        # Test with head inclined to the left
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["left_ear"]].y = 0.28
        mock_landmarks[analyzer.landmarks_map["right_ear"]].y = 0.32
        inclination = analyzer._analyze_frontal_head_inclination(mock_landmarks)
        assert inclination == "right"
        
        # Test with head inclined to the right
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["left_ear"]].y = 0.32
        mock_landmarks[analyzer.landmarks_map["right_ear"]].y = 0.28
        inclination = analyzer._analyze_frontal_head_inclination(mock_landmarks)
        assert inclination == "left"

    def test_analyze_frontal_shoulder_position(self, mock_pose_landmarks):
        """Test the analysis of frontal shoulder position."""
        analyzer = PostureAnalyzer()
        
        # Test with balanced shoulders
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["left_shoulder"]].y = 0.5
        mock_landmarks[analyzer.landmarks_map["right_shoulder"]].y = 0.5
        position = analyzer._analyze_frontal_shoulder_position(mock_landmarks)
        assert position == "normal"
        
        # Test with elevated right shoulder
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["left_shoulder"]].y = 0.53
        mock_landmarks[analyzer.landmarks_map["right_shoulder"]].y = 0.5
        position = analyzer._analyze_frontal_shoulder_position(mock_landmarks)
        assert position == "elevated_right"
        
        # Test with elevated left shoulder
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["left_shoulder"]].y = 0.5
        mock_landmarks[analyzer.landmarks_map["right_shoulder"]].y = 0.53
        position = analyzer._analyze_frontal_shoulder_position(mock_landmarks)
        assert position == "elevated_left"
        
    def test_analyze_lateral_shoulder_position(self, mock_pose_landmarks):
        """Test the analysis of lateral shoulder position."""
        analyzer = PostureAnalyzer()
        
        # Test with normal shoulder position
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["right_shoulder"]].x = 0.58
        mock_landmarks[analyzer.landmarks_map["right_ear"]].x = 0.6
        position = analyzer._analyze_lateral_shoulder_position(mock_landmarks)
        assert position == "normal"
        
        # Test with anterior rotation
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["right_shoulder"]].x = 0.67
        mock_landmarks[analyzer.landmarks_map["right_ear"]].x = 0.6
        position = analyzer._analyze_lateral_shoulder_position(mock_landmarks)
        assert position == "anterior_rotation"
        
    def test_analyze_lateral_head_position(self, mock_pose_landmarks):
        """Test the analysis of lateral head position."""
        analyzer = PostureAnalyzer()
        
        # Test with normal head position
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["right_ear"]].x = 0.60
        mock_landmarks[analyzer.landmarks_map["right_shoulder"]].x = 0.60
        mock_landmarks[analyzer.landmarks_map["nose"]].x = 0.62
        position = analyzer._analyze_lateral_head_position(mock_landmarks)
        assert position == "normal"
        
        # Test with anterior head position
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["right_ear"]].x = 0.67
        mock_landmarks[analyzer.landmarks_map["right_shoulder"]].x = 0.60
        position = analyzer._analyze_lateral_head_position(mock_landmarks)
        assert position == "anterior"
        
        # Test with flexion - nose much further forward than ear and ear not in front of shoulder
        mock_landmarks = mock_pose_landmarks.landmark.copy()
        mock_landmarks[analyzer.landmarks_map["right_ear"]].x = 0.60
        mock_landmarks[analyzer.landmarks_map["right_shoulder"]].x = 0.61  # Shoulder slightly in front of ear
        mock_landmarks[analyzer.landmarks_map["nose"]].x = 0.67
        position = analyzer._analyze_lateral_head_position(mock_landmarks)
        assert position == "flexion"
        
    def test_analyze_posture_no_landmarks(self):
        """Test analyze_posture when no pose landmarks are detected."""
        # Create a PostureAnalyzer with a mock pose detector
        mock_pose_detector = MagicMock()
        mock_pose_detector.process_image.return_value = []  # No landmarks detected
        mock_pose_detector.get_landmark_indices.return_value = {}
        
        analyzer = PostureAnalyzer(pose_detector=mock_pose_detector)
        
        # Mock the _process_image method to return None
        with patch.object(analyzer, '_process_image', return_value=None):
            # Test that ValueError is raised when no pose landmarks are detected
            with pytest.raises(ValueError, match="Failed to detect pose landmarks"):
                analyzer.analyze_posture("dummy_frontal", "dummy_lateral")
            
    def test_analyze_posture_results_structure(self):
        """Test that analyze_posture produces expected results structure."""
        analyzer = PostureAnalyzer()
        
        # Mock process_image to return a valid result
        with patch.object(analyzer, '_process_image') as mock_process_image, \
             patch.object(analyzer, '_analyze_frontal_head_rotation', return_value="normal"), \
             patch.object(analyzer, '_analyze_frontal_head_inclination', return_value="left"), \
             patch.object(analyzer, '_analyze_frontal_shoulder_position', return_value="normal"), \
             patch.object(analyzer, '_analyze_lateral_head_position', return_value="normal"), \
             patch.object(analyzer, '_analyze_lateral_shoulder_position', return_value="normal"):
            
            # Create mock results with landmarks
            from orofacIAnalysis.detectors.base import LandmarkPoint, LandmarkResult
            
            # Create mock landmarks
            landmarks = []
            for i in range(33):  # MediaPipe pose has 33 landmarks
                landmarks.append(LandmarkPoint(0, 0, 0, 1.0))
                
            # Create mock results
            mock_result1 = LandmarkResult(landmarks=landmarks, confidence=1.0)
            mock_result2 = LandmarkResult(landmarks=landmarks, confidence=1.0)
            
            mock_process_image.side_effect = [mock_result1, mock_result2]
            
            # Call analyze_posture with dummy images
            results = analyzer.analyze_posture(b'dummy frontal', b'dummy lateral')
            
            # Check results structure
            assert "frontal_view" in results
            assert "lateral_view" in results
            
            frontal = results["frontal_view"]
            assert "head_rotation" in frontal
            assert "head_inclination" in frontal
            assert "shoulder_position" in frontal
            
            lateral = results["lateral_view"]
            assert "head_position" in lateral
            assert "shoulder_position" in lateral