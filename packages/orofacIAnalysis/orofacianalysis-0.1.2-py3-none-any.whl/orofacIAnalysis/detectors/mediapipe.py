"""MediaPipe implementations of detector interfaces."""

import cv2
import numpy as np
import mediapipe as mp
from typing import List, Dict, Any, Optional, Tuple

from orofacIAnalysis.detectors.base import (
    FaceDetector,
    HandDetector,
    PoseDetector,
    LandmarkPoint,
    LandmarkResult
)


class MediapipeFaceDetector(FaceDetector):
    """MediaPipe implementation of face landmark detection."""
    
    # Common face landmarks mapping
    FACE_LANDMARKS = {
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
        "nose": 4,
    }
    
    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_faces: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        """Initialize MediaPipe face mesh detector.
        
        Args:
            static_image_mode: Whether to analyze as static images vs video
            max_num_faces: Maximum number of faces to detect
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            max_num_faces=max_num_faces,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(
            color=(0, 255, 0), thickness=1, circle_radius=1)
        
    def process_image(self, image: np.ndarray) -> List[LandmarkResult]:
        """Process an image and return detected face landmarks.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            List of LandmarkResult, one for each detected face
        """
        results = []
        
        # Process the image with MediaPipe
        mp_results = self.face_mesh.process(image)
        
        if mp_results.multi_face_landmarks:
            for face_landmarks in mp_results.multi_face_landmarks:
                # Convert MediaPipe landmarks to standardized format
                landmarks = []
                for i, lm in enumerate(face_landmarks.landmark):
                    landmarks.append(LandmarkPoint(
                        x=lm.x,
                        y=lm.y,
                        z=lm.z if hasattr(lm, 'z') else 0.0,
                        visibility=1.0  # MediaPipe face mesh doesn't provide visibility
                    ))
                
                # Create result with estimated confidence (MediaPipe doesn't provide this)
                results.append(LandmarkResult(
                    landmarks=landmarks,
                    confidence=1.0  # Using a default value as MediaPipe doesn't provide this
                ))
        
        return results
    
    def get_landmark_indices(self) -> Dict[str, int]:
        """Get dictionary mapping landmark names to indices.
        
        Returns:
            Dictionary mapping landmark names to their indices
        """
        return self.FACE_LANDMARKS
    
    def visualize(self, image: np.ndarray, results: List[LandmarkResult]) -> np.ndarray:
        """Draw landmarks on the image.
        
        Args:
            image: RGB image as numpy array
            results: List of LandmarkResult objects
            
        Returns:
            Image with drawn landmarks
        """
        annotated_image = image.copy()
        
        for result in results:
            # Convert to MediaPipe format for drawing
            landmarks_proto = self._convert_to_mp_format(result.landmarks)
            
            # Draw the face mesh
            self.mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.drawing_spec
            )
            
            # Highlight key landmarks
            height, width = image.shape[:2]
            for name, idx in self.FACE_LANDMARKS.items():
                if idx < len(result.landmarks):
                    lm = result.landmarks[idx]
                    x, y = int(lm.x * width), int(lm.y * height)
                    cv2.circle(annotated_image, (x, y), 5, (255, 0, 0), -1)
        
        return annotated_image
    
    def _convert_to_mp_format(self, landmarks: List[LandmarkPoint]) -> Any:
        """Convert our landmark format to MediaPipe format for visualization."""
        import mediapipe.framework.formats.landmark_pb2 as landmark_pb2
        
        landmark_list = landmark_pb2.NormalizedLandmarkList()
        for lm in landmarks:
            landmark = landmark_pb2.NormalizedLandmark()
            landmark.x = lm.x
            landmark.y = lm.y
            landmark.z = lm.z
            landmark_list.landmark.append(landmark)
        
        return landmark_list


class MediapipeHandDetector(HandDetector):
    """MediaPipe implementation of hand detection."""
    
    # Common hand landmarks mapping
    HAND_LANDMARKS = {
        "wrist": 0,
        "thumb_tip": 4,
        "index_finger_tip": 8,
        "middle_finger_tip": 12,
        "ring_finger_tip": 16,
        "pinky_tip": 20
    }
    
    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        """Initialize MediaPipe hand detector.
        
        Args:
            static_image_mode: Whether to analyze as static images vs video
            max_num_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence value for detection
            min_tracking_confidence: Minimum confidence value for tracking
        """
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
    
    def process_image(self, image: np.ndarray) -> List[LandmarkResult]:
        """Process an image and return detected hand landmarks.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            List of LandmarkResult, one for each detected hand
        """
        results = []
        
        # Process the image with MediaPipe
        mp_results = self.hands.process(image)
        
        if mp_results.multi_hand_landmarks:
            for hand_landmarks in mp_results.multi_hand_landmarks:
                # Convert MediaPipe landmarks to standardized format
                landmarks = []
                for i, lm in enumerate(hand_landmarks.landmark):
                    landmarks.append(LandmarkPoint(
                        x=lm.x,
                        y=lm.y,
                        z=lm.z if hasattr(lm, 'z') else 0.0,
                        visibility=1.0  # MediaPipe hand landmarks don't provide visibility
                    ))
                
                # Create result with confidence
                results.append(LandmarkResult(
                    landmarks=landmarks,
                    confidence=1.0  # Using a default value
                ))
        
        return results
    
    def get_landmark_indices(self) -> Dict[str, int]:
        """Get dictionary mapping landmark names to indices.
        
        Returns:
            Dictionary mapping landmark names to their indices
        """
        return self.HAND_LANDMARKS
    
    def visualize(self, image: np.ndarray, results: List[LandmarkResult]) -> np.ndarray:
        """Draw landmarks on the image.
        
        Args:
            image: RGB image as numpy array
            results: List of LandmarkResult objects
            
        Returns:
            Image with drawn landmarks
        """
        annotated_image = image.copy()
        
        for result in results:
            # Convert to MediaPipe format for drawing
            landmarks_proto = self._convert_to_mp_format(result.landmarks)
            
            # Draw the hand landmarks
            self.mp_drawing.draw_landmarks(
                annotated_image,
                landmarks_proto,
                mp.solutions.hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
        
        return annotated_image
    
    def _convert_to_mp_format(self, landmarks: List[LandmarkPoint]) -> Any:
        """Convert our landmark format to MediaPipe format for visualization."""
        import mediapipe.framework.formats.landmark_pb2 as landmark_pb2
        
        landmark_list = landmark_pb2.NormalizedLandmarkList()
        for lm in landmarks:
            landmark = landmark_pb2.NormalizedLandmark()
            landmark.x = lm.x
            landmark.y = lm.y
            landmark.z = lm.z
            landmark_list.landmark.append(landmark)
        
        return landmark_list


class MediapipePoseDetector(PoseDetector):
    """MediaPipe implementation of pose detection."""
    
    # Common pose landmarks mapping
    POSE_LANDMARKS = {
        "nose": 0,
        "left_eye": 2,
        "right_eye": 5,
        "left_ear": 7,
        "right_ear": 8,
        "left_shoulder": 11,
        "right_shoulder": 12,
        "left_elbow": 13,
        "right_elbow": 14,
        "left_wrist": 15,
        "right_wrist": 16,
        "left_hip": 23,
        "right_hip": 24,
        "left_knee": 25,
        "right_knee": 26,
        "left_ankle": 27,
        "right_ankle": 28
    }
    
    def __init__(
        self,
        static_image_mode: bool = False,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        """Initialize MediaPipe pose detector.
        
        Args:
            static_image_mode: Whether to analyze as static images vs video
            model_complexity: Model complexity (0, 1, or 2)
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Store the mapping from MediaPipe enum to our indices
        self.landmarks_enum = mp.solutions.pose.PoseLandmark
    
    def process_image(self, image: np.ndarray) -> List[LandmarkResult]:
        """Process an image and return detected pose landmarks.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            List of LandmarkResult, typically with one item for the detected pose
        """
        results = []
        
        # Process the image with MediaPipe
        mp_results = self.pose.process(image)
        
        if mp_results.pose_landmarks:
            # Convert MediaPipe landmarks to standardized format
            landmarks = []
            for i, lm in enumerate(mp_results.pose_landmarks.landmark):
                landmarks.append(LandmarkPoint(
                    x=lm.x,
                    y=lm.y,
                    z=lm.z if hasattr(lm, 'z') else 0.0,
                    visibility=lm.visibility if hasattr(lm, 'visibility') else 1.0
                ))
            
            # Create result with confidence
            results.append(LandmarkResult(
                landmarks=landmarks,
                confidence=1.0  # MediaPipe doesn't provide an overall confidence
            ))
        
        return results
    
    def get_landmark_indices(self) -> Dict[str, int]:
        """Get dictionary mapping landmark names to indices.
        
        Returns:
            Dictionary mapping landmark names to their indices
        """
        return self.POSE_LANDMARKS
    
    def visualize(self, image: np.ndarray, results: List[LandmarkResult]) -> np.ndarray:
        """Draw landmarks on the image.
        
        Args:
            image: RGB image as numpy array
            results: List of LandmarkResult objects
            
        Returns:
            Image with drawn landmarks
        """
        annotated_image = image.copy()
        
        for result in results:
            # Convert to MediaPipe format for drawing
            landmarks_proto = self._convert_to_mp_format(result.landmarks)
            
            # Draw the pose landmarks
            self.mp_drawing.draw_landmarks(
                annotated_image,
                landmarks_proto,
                mp.solutions.pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing.DrawingSpec(
                    color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=self.mp_drawing.DrawingSpec(
                    color=(255, 0, 0), thickness=2)
            )
            
            # Optionally add labels for key landmarks
            height, width = image.shape[:2]
            for name, idx in self.POSE_LANDMARKS.items():
                if idx < len(result.landmarks):
                    lm = result.landmarks[idx]
                    if lm.visibility > 0.5:  # Only show visible landmarks
                        x, y = int(lm.x * width), int(lm.y * height)
                        cv2.putText(
                            annotated_image,
                            name.split('_')[-1],
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 255),
                            1,
                            cv2.LINE_AA
                        )
        
        return annotated_image
    
    def _convert_to_mp_format(self, landmarks: List[LandmarkPoint]) -> Any:
        """Convert our landmark format to MediaPipe format for visualization."""
        import mediapipe.framework.formats.landmark_pb2 as landmark_pb2
        
        landmark_list = landmark_pb2.NormalizedLandmarkList()
        for lm in landmarks:
            landmark = landmark_pb2.NormalizedLandmark()
            landmark.x = lm.x
            landmark.y = lm.y
            landmark.z = lm.z
            landmark.visibility = lm.visibility
            landmark_list.landmark.append(landmark)
        
        return landmark_list