"""Shared fixtures for orofacIAnalysis tests."""

import os
import pytest
import numpy as np
from pathlib import Path

# Define the path to test resources
TEST_RESOURCES = Path(__file__).parent / "test_resources"


@pytest.fixture
def test_resources_dir():
    """Return the path to the test resources directory."""
    return TEST_RESOURCES


@pytest.fixture
def sample_jaw_movements():
    """Generate sample jaw movement data for testing."""
    # Generate a sinusoidal signal with some noise to simulate jaw movements
    x = np.linspace(0, 4 * np.pi, 200)
    signal = np.sin(x) + 0.2 * np.random.randn(len(x))
    return signal.tolist()


@pytest.fixture
def sample_jaw_positions():
    """Generate sample jaw position data for testing."""
    # Generate a list of (x, y) tuples to simulate jaw positions
    x = np.linspace(0, 4 * np.pi, 200)
    positions = []
    for i in range(len(x)):
        # Create realistic jaw positions that move in a pattern
        x_pos = 320 + 20 * np.sin(x[i])
        y_pos = 240 + 30 * np.sin(x[i])
        positions.append((x_pos, y_pos))
    return positions


@pytest.fixture
def sample_directions():
    """Generate sample chewing direction data for testing."""
    # 0 = left, 1 = right, 2 = middle
    directions = [0, 0, 1, 0, 2, 1, 1, 0, 2, 1]
    return directions


@pytest.fixture
def sample_video_path_1():
    """Path to a sample video file for testing."""
    video_path = TEST_RESOURCES / "sample_chewing_1.mp4"
    if not video_path.exists():
        pytest.skip(f"Sample video not found at {video_path}")
    return str(video_path)

@pytest.fixture
def sample_video_path_2():
    """Path to a sample video file for testing."""
    video_path = TEST_RESOURCES / "sample_chewing_2.mp4"
    if not video_path.exists():
        pytest.skip(f"Sample video not found at {video_path}")
    return str(video_path)


@pytest.fixture
def sample_face_image_path():
    """Path to a sample face image for testing."""
    image_path = TEST_RESOURCES / "face.jpg"
    if not image_path.exists():
        pytest.skip(f"Sample face image not found at {image_path}")
    return str(image_path)


@pytest.fixture
def sample_frontal_image_path():
    """Path to a sample frontal body image for testing."""
    image_path = TEST_RESOURCES / "sample_frontal.png"
    if not image_path.exists():
        pytest.skip(f"Sample frontal image not found at {image_path}")
    return str(image_path)


@pytest.fixture
def sample_lateral_image_path():
    """Path to a sample lateral body image for testing."""
    image_path = TEST_RESOURCES / "sample_lateral.png"
    if not image_path.exists():
        pytest.skip(f"Sample lateral image not found at {image_path}")
    return str(image_path)


@pytest.fixture
def mock_face_landmarks():
    """Create a mock face landmarks structure for testing."""
    class MockLandmark:
        def __init__(self, x, y, z=0):
            self.x = x
            self.y = y
            self.z = z
    
    class MockFaceLandmarks:
        def __init__(self):
            self.landmark = {}
            # Add some key landmarks with realistic normalized coordinates
            self.landmark[2] = MockLandmark(0.5, 0.6)    # subnasal
            self.landmark[4] = MockLandmark(0.5, 0.5)    # nose tip
            self.landmark[9] = MockLandmark(0.5, 0.3)    # glabella
            self.landmark[13] = MockLandmark(0.5, 0.65)  # lowest upper lip
            self.landmark[14] = MockLandmark(0.5, 0.7)   # highest lower lip
            self.landmark[61] = MockLandmark(0.4, 0.65)  # left mouth corner
            self.landmark[116] = MockLandmark(0.3, 0.5)  # left face side
            self.landmark[152] = MockLandmark(0.5, 0.85) # gnathion (chin)
            self.landmark[226] = MockLandmark(0.4, 0.45) # left eye corner
            self.landmark[291] = MockLandmark(0.6, 0.65) # right mouth corner
            self.landmark[345] = MockLandmark(0.7, 0.5)  # right face side
            self.landmark[446] = MockLandmark(0.6, 0.45) # right eye corner
            
    return MockFaceLandmarks()


@pytest.fixture
def mock_face_detector():
    """Create a mock face detector for testing."""
    from orofacIAnalysis.detectors.base import FaceDetector, LandmarkPoint, LandmarkResult
    from unittest.mock import MagicMock
    
    # Create mock landmarks for the standardized format
    landmarks = []
    landmark_map = {
        "subnasal": 2,
        "nose": 4,
        "glabella": 9,
        "lowest_upper_lip": 13,
        "highest_lower_lip": 14,
        "left_mouth_corner": 61,
        "left_face_side": 116,
        "gnathion": 152,
        "left_eye_corner": 226,
        "right_mouth_corner": 291,
        "right_face_side": 345,
        "right_eye_corner": 446
    }
    
    # Initialize with empty landmarks (will be populated later)
    for i in range(500):  # MediaPipe face has around 468 landmarks
        landmarks.append(LandmarkPoint(0, 0, 0, 1.0))
    
    # Set specific landmarks
    landmarks[2] = LandmarkPoint(0.5, 0.6, 0, 1.0)    # subnasal
    landmarks[4] = LandmarkPoint(0.5, 0.5, 0, 1.0)    # nose
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
    
    # Create a mock detector
    mock_detector = MagicMock(spec=FaceDetector)
    
    # Set up the get_landmark_indices method
    mock_detector.get_landmark_indices.return_value = landmark_map
    
    # Set up the process_image method to return a LandmarkResult
    result = LandmarkResult(landmarks=landmarks, confidence=1.0)
    mock_detector.process_image.return_value = [result]
    
    # Set up visualize method
    mock_detector.visualize.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    
    return mock_detector


@pytest.fixture
def mock_pose_landmarks():
    """Create a mock pose landmarks structure for testing."""
    class MockLandmark:
        def __init__(self, x, y, z=0, visibility=1.0):
            self.x = x
            self.y = y
            self.z = z
            self.visibility = visibility
    
    class MockPoseLandmarks:
        def __init__(self):
            self.landmark = [MockLandmark(0, 0)] * 33  # MediaPipe pose has 33 landmarks
            
            # Set specific landmark positions
            # NOSE
            self.landmark[0] = MockLandmark(0.5, 0.3)
            # LEFT_EYE_INNER, LEFT_EYE, LEFT_EYE_OUTER
            self.landmark[1] = MockLandmark(0.48, 0.28)
            self.landmark[2] = MockLandmark(0.46, 0.28)
            self.landmark[3] = MockLandmark(0.44, 0.29)
            # RIGHT_EYE_INNER, RIGHT_EYE, RIGHT_EYE_OUTER
            self.landmark[4] = MockLandmark(0.52, 0.28)
            self.landmark[5] = MockLandmark(0.54, 0.28)
            self.landmark[6] = MockLandmark(0.56, 0.29)
            # LEFT_EAR, RIGHT_EAR
            self.landmark[7] = MockLandmark(0.4, 0.3)
            self.landmark[8] = MockLandmark(0.6, 0.3)
            # LEFT_SHOULDER, RIGHT_SHOULDER
            self.landmark[11] = MockLandmark(0.35, 0.5)
            self.landmark[12] = MockLandmark(0.65, 0.5)
            # LEFT_HIP, RIGHT_HIP
            self.landmark[23] = MockLandmark(0.4, 0.7)
            self.landmark[24] = MockLandmark(0.6, 0.7)
            
    return MockPoseLandmarks()


@pytest.fixture
def mock_pose_detector():
    """Create a mock pose detector for testing."""
    from orofacIAnalysis.detectors.base import PoseDetector, LandmarkPoint, LandmarkResult
    from unittest.mock import MagicMock
    
    # Create mock landmarks for the standardized format
    landmarks = []
    landmark_map = {
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
    
    # Initialize with empty landmarks
    for i in range(33):  # MediaPipe pose has 33 landmarks
        landmarks.append(LandmarkPoint(0, 0, 0, 1.0))
    
    # Set specific landmarks
    landmarks[0] = LandmarkPoint(0.5, 0.3, 0, 1.0)    # nose
    landmarks[1] = LandmarkPoint(0.48, 0.28, 0, 1.0)  # left_eye_inner
    landmarks[2] = LandmarkPoint(0.46, 0.28, 0, 1.0)  # left_eye
    landmarks[3] = LandmarkPoint(0.44, 0.29, 0, 1.0)  # left_eye_outer
    landmarks[4] = LandmarkPoint(0.52, 0.28, 0, 1.0)  # right_eye_inner
    landmarks[5] = LandmarkPoint(0.54, 0.28, 0, 1.0)  # right_eye
    landmarks[6] = LandmarkPoint(0.56, 0.29, 0, 1.0)  # right_eye_outer
    landmarks[7] = LandmarkPoint(0.4, 0.3, 0, 1.0)    # left_ear
    landmarks[8] = LandmarkPoint(0.6, 0.3, 0, 1.0)    # right_ear
    landmarks[11] = LandmarkPoint(0.35, 0.5, 0, 1.0)  # left_shoulder
    landmarks[12] = LandmarkPoint(0.65, 0.5, 0, 1.0)  # right_shoulder
    landmarks[23] = LandmarkPoint(0.4, 0.7, 0, 1.0)   # left_hip
    landmarks[24] = LandmarkPoint(0.6, 0.7, 0, 1.0)   # right_hip
    
    # Create a mock detector
    mock_detector = MagicMock(spec=PoseDetector)
    
    # Set up the get_landmark_indices method
    mock_detector.get_landmark_indices.return_value = landmark_map
    
    # Set up the process_image method to return a LandmarkResult
    result = LandmarkResult(landmarks=landmarks, confidence=1.0)
    mock_detector.process_image.return_value = [result]
    
    # Set up visualize method
    mock_detector.visualize.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    
    return mock_detector


@pytest.fixture
def mock_hand_detector():
    """Create a mock hand detector for testing."""
    from orofacIAnalysis.detectors.base import HandDetector, LandmarkPoint, LandmarkResult
    from unittest.mock import MagicMock
    
    # Create mock landmarks for the standardized format
    landmarks = []
    landmark_map = {
        "wrist": 0,
        "thumb_tip": 4,
        "index_finger_tip": 8,
        "middle_finger_tip": 12,
        "ring_finger_tip": 16,
        "pinky_tip": 20
    }
    
    # Initialize with empty landmarks
    for i in range(21):  # MediaPipe hand has 21 landmarks
        landmarks.append(LandmarkPoint(0, 0, 0, 1.0))
    
    # Set specific landmarks
    landmarks[0] = LandmarkPoint(0.6, 0.6, 0, 1.0)  # wrist
    landmarks[4] = LandmarkPoint(0.5, 0.4, 0, 1.0)  # thumb_tip
    landmarks[8] = LandmarkPoint(0.6, 0.3, 0, 1.0)  # index_finger_tip
    landmarks[12] = LandmarkPoint(0.7, 0.3, 0, 1.0) # middle_finger_tip
    landmarks[16] = LandmarkPoint(0.8, 0.4, 0, 1.0) # ring_finger_tip
    landmarks[20] = LandmarkPoint(0.9, 0.5, 0, 1.0) # pinky_tip
    
    # Create a mock detector
    mock_detector = MagicMock(spec=HandDetector)
    
    # Set up the get_landmark_indices method
    mock_detector.get_landmark_indices.return_value = landmark_map
    
    # Set up the process_image method to return a LandmarkResult with a hand
    result = LandmarkResult(landmarks=landmarks, confidence=1.0)
    mock_detector.process_image.return_value = [result]
    
    # Set up visualize method
    mock_detector.visualize.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    
    return mock_detector


@pytest.fixture
def mock_hand_detector_no_hands():
    """Create a mock hand detector that doesn't detect any hands."""
    from orofacIAnalysis.detectors.base import HandDetector
    from unittest.mock import MagicMock
    
    # Create a mock detector
    mock_detector = MagicMock(spec=HandDetector)
    
    # Set up the get_landmark_indices method
    mock_detector.get_landmark_indices.return_value = {
        "wrist": 0,
        "thumb_tip": 4,
        "index_finger_tip": 8,
        "middle_finger_tip": 12,
        "ring_finger_tip": 16,
        "pinky_tip": 20
    }
    
    # Set up the process_image method to return an empty list (no hands)
    mock_detector.process_image.return_value = []
    
    # Set up visualize method
    mock_detector.visualize.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    
    return mock_detector