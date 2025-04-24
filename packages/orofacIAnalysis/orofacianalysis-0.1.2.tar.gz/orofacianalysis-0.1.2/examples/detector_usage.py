"""Example of using custom detectors with orofacIAnalysis."""

import cv2
import numpy as np
from pathlib import Path

from orofacIAnalysis.face import FacialAnalyzer
from orofacIAnalysis.posture import PostureAnalyzer
from orofacIAnalysis.chew_annotator import ChewAnnotator
from orofacIAnalysis.detectors import (
    MediapipeFaceDetector,
    MediapipePoseDetector,
    MediapipeHandDetector
)

# Example 1: Using default MediaPipe detectors (implicit)
def example_default_detectors():
    """Example using default MediaPipe detectors."""
    # Create analyzers with default (MediaPipe) detectors
    facial_analyzer = FacialAnalyzer()  # Uses MediaPipe by default
    posture_analyzer = PostureAnalyzer()  # Uses MediaPipe by default
    
    print("Created analyzers with default MediaPipe detectors")
    
    # Process example images
    sample_face_path = Path("tests/test_resources/sample_face.jpg")
    if sample_face_path.exists():
        try:
            with open(sample_face_path, "rb") as f:
                results = facial_analyzer.analyze_image(f)
                print(f"Face analysis results: {results.keys()}")
        except Exception as e:
            print(f"Error analyzing face: {e}")
    else:
        print(f"Sample face image not found at {sample_face_path}")


# Example 2: Explicitly using MediaPipe detectors
def example_explicit_mediapipe():
    """Example explicitly using MediaPipe detectors."""
    # Create MediaPipe detectors with custom parameters
    face_detector = MediapipeFaceDetector(
        static_image_mode=True,
        max_num_faces=2,  # Detect up to 2 faces
        min_detection_confidence=0.7  # Higher confidence threshold
    )
    
    pose_detector = MediapipePoseDetector(
        static_image_mode=True,
        model_complexity=2,  # Highest complexity for better accuracy
        min_detection_confidence=0.6
    )
    
    # Create analyzers with the custom detectors
    facial_analyzer = FacialAnalyzer(face_detector=face_detector)
    posture_analyzer = PostureAnalyzer(pose_detector=pose_detector)
    
    print("Created analyzers with custom MediaPipe detector parameters")


# Example 3: Using a custom detector implementation
def example_custom_detector():
    """Example showing how to create and use a custom detector."""
    # This is an example of how you could implement a custom detector
    try:
        from orofacIAnalysis.detectors import DlibFaceDetector
        
        # Create a DLib face detector (if dlib is installed)
        try:
            # Path to the shape predictor model (you would need to download this)
            model_path = "shape_predictor_68_face_landmarks.dat"
            dlib_detector = DlibFaceDetector(
                predictor_path=model_path,
                upsample_num_times=1
            )
            
            # Create a facial analyzer using the DLib detector
            facial_analyzer = FacialAnalyzer(face_detector=dlib_detector)
            print("Created facial analyzer with DLib detector")
        except Exception as e:
            print(f"Could not initialize DLib detector: {e}")
    except ImportError:
        print("DLib detector not available - this is just an example")
    
    # Implement a mock custom detector as an example
    from orofacIAnalysis.detectors.base import FaceDetector, LandmarkPoint, LandmarkResult
    
    class MockFaceDetector(FaceDetector):
        """A simple mock face detector for demonstration purposes."""
        
        def __init__(self):
            """Initialize the mock detector."""
            self.landmarks_map = {
                "left_face_side": 0,
                "right_face_side": 1,
                "glabella": 2,
                "subnasal": 3,
                "gnathion": 4,
                "left_eye_corner": 5,
                "right_eye_corner": 6,
                "left_mouth_corner": 7,
                "right_mouth_corner": 8,
                "lowest_upper_lip": 9,
                "highest_lower_lip": 10,
                "nose": 11
            }
        
        def process_image(self, image):
            """Process image and return mock landmarks."""
            height, width = image.shape[:2]
            
            # Generate mock landmarks for demonstration
            landmarks = [
                # Left face side
                LandmarkPoint(x=0.2, y=0.5, z=0.0),
                # Right face side
                LandmarkPoint(x=0.8, y=0.5, z=0.0),
                # Glabella (forehead)
                LandmarkPoint(x=0.5, y=0.3, z=0.0),
                # Subnasal (nose bottom)
                LandmarkPoint(x=0.5, y=0.55, z=0.0),
                # Gnathion (chin)
                LandmarkPoint(x=0.5, y=0.8, z=0.0),
                # Left eye corner
                LandmarkPoint(x=0.35, y=0.4, z=0.0),
                # Right eye corner
                LandmarkPoint(x=0.65, y=0.4, z=0.0),
                # Left mouth corner
                LandmarkPoint(x=0.4, y=0.65, z=0.0),
                # Right mouth corner
                LandmarkPoint(x=0.6, y=0.65, z=0.0),
                # Lowest upper lip
                LandmarkPoint(x=0.5, y=0.62, z=0.0),
                # Highest lower lip
                LandmarkPoint(x=0.5, y=0.68, z=0.0),
                # Nose
                LandmarkPoint(x=0.5, y=0.5, z=0.0)
            ]
            
            # Return a single face result
            result = LandmarkResult(landmarks=landmarks, confidence=1.0)
            return [result]
        
        def get_landmark_indices(self):
            """Return the landmark indices map."""
            return self.landmarks_map
        
        def visualize(self, image, results):
            """Visualize landmarks on the image."""
            annotated_image = image.copy()
            
            if not results:
                return annotated_image
                
            height, width = image.shape[:2]
            result = results[0]
            
            # Draw key points
            for i, landmark in enumerate(result.landmarks):
                x, y = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(annotated_image, (x, y), 3, (0, 255, 0), -1)
                
                # Draw a face oval
                cv2.ellipse(
                    annotated_image,
                    (width // 2, height // 2),
                    (int(width * 0.3), int(height * 0.4)),
                    0, 0, 360, (0, 255, 0), 1
                )
            
            return annotated_image
    
    # Create a facial analyzer with the mock detector
    mock_detector = MockFaceDetector()
    facial_analyzer = FacialAnalyzer(face_detector=mock_detector)
    print("Created facial analyzer with mock detector")
    
    # Create a test image
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.ellipse(test_image, (320, 240), (150, 200), 0, 0, 360, (255, 255, 255), -1)
    
    # Test the analyzer with the mock detector
    try:
        results = facial_analyzer.analyze_image(test_image)
        print(f"Mock analysis results: {results.keys()}")
    except Exception as e:
        print(f"Error with mock analysis: {e}")


if __name__ == "__main__":
    print("Example 1: Using default MediaPipe detectors")
    example_default_detectors()
    
    print("\nExample 2: Explicitly using MediaPipe detectors with custom parameters")
    example_explicit_mediapipe()
    
    print("\nExample 3: Using a custom detector implementation")
    example_custom_detector()