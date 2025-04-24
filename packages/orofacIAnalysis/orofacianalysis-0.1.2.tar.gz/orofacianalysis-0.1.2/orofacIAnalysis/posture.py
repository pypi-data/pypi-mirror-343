"""Posture analysis functionality for orofacIAnalysis."""

import numpy as np
import cv2
from typing import Optional, Dict, Any, Union
from orofacIAnalysis.utils import load_image
from orofacIAnalysis.detectors import (
    PoseDetector,
    MediapipePoseDetector,
    LandmarkResult
)


class PostureAnalyzer:
    """
    Class for analyzing body posture using pose detection.
    
    This analyzer can process frontal and lateral (side) view images
    to assess various aspects of posture including head position,
    shoulder alignment, and body orientation.
    
    By default, it uses MediaPipe for pose detection but can work with any detector 
    that implements the PoseDetector interface.
    """
    
    def __init__(self, pose_detector: Optional[PoseDetector] = None):
        """Initialize the posture analyzer with a pose detector.
        
        Args:
            pose_detector: Pose detector implementation (defaults to MediaPipe)
        """
        # Use provided detector or create default MediaPipe detector
        self.pose_detector = pose_detector or MediapipePoseDetector(
            static_image_mode=True,
            model_complexity=2,
            min_detection_confidence=0.5
        )
        
        # Get landmark indices from the detector
        self.landmarks_map = self.pose_detector.get_landmark_indices()
    
    def analyze_posture(self, frontal_image, lateral_image):
        """
        Analyze posture from frontal and lateral images.
        
        Args:
            frontal_image: Front view image data (bytes or file-like object)
            lateral_image: Side view image data (bytes or file-like object)
            
        Returns:
            dict: Dictionary containing posture analysis results
            
        Raises:
            ValueError: If pose detection fails on either image
        """
        # Process both images
        frontal_result = self._process_image(frontal_image)
        lateral_result = self._process_image(lateral_image)
        
        if not frontal_result:
            raise ValueError("Failed to detect pose landmarks in frontal image")
        
        if not lateral_result:
            raise ValueError("Failed to detect pose landmarks in lateral image")
        
        # Analyze frontal view
        head_rotation = self._analyze_frontal_head_rotation(frontal_result.landmarks)
        head_inclination = self._analyze_frontal_head_inclination(frontal_result.landmarks)
        frontal_shoulder_position = self._analyze_frontal_shoulder_position(frontal_result.landmarks)
        
        # Analyze lateral view
        lateral_head_position = self._analyze_lateral_head_position(lateral_result.landmarks)
        lateral_shoulder_position = self._analyze_lateral_shoulder_position(lateral_result.landmarks)
        
        # Compile results
        analysis_results = {
            "frontal_view": {
                "head_rotation": head_rotation,
                "head_inclination": head_inclination,
                "shoulder_position": frontal_shoulder_position
            },
            "lateral_view": {
                "head_position": lateral_head_position,
                "shoulder_position": lateral_shoulder_position
            }
        }
        
        return analysis_results
    
    def _process_image(self, image_data):
        """
        Process image with pose detection.
        
        Args:
            image_data: Image data as bytes or file-like object
            
        Returns:
            LandmarkResult: The detected pose landmarks
        """
        # Load image
        image = load_image(image_data)
        
        image = np.array(image.convert('RGB'))
        
        # Process with pose detector
        results = self.pose_detector.process_image(image)
        if not results:
            return None
        
        # Return the first result (usually only one pose is detected)
        return results[0]
    
    def _analyze_frontal_head_rotation(self, landmarks):
        """
        Analyze frontal head rotation (left, right, or normal).
        
        Args:
            landmarks: List of LandmarkPoint objects
            
        Returns:
            str: Head rotation classification
        """
        left_ear = landmarks[self.landmarks_map["left_ear"]]
        right_ear = landmarks[self.landmarks_map["right_ear"]]
        nose = landmarks[self.landmarks_map["nose"]]
        
        left_ear_distance = np.sqrt((nose.x - left_ear.x)**2 + (nose.y - left_ear.y)**2)
        right_ear_distance = np.sqrt((nose.x - right_ear.x)**2 + (nose.y - right_ear.y)**2)
        
        ratio = left_ear_distance / right_ear_distance if right_ear_distance > 0 else float('inf')
        
        threshold = 0.1
        
        if abs(ratio - 1) <= threshold:
            return "normal"
        elif ratio > 1 + threshold:
            return "right"
        else:
            return "left"
    
    def _analyze_frontal_head_inclination(self, landmarks):
        """
        Analyze frontal head inclination (left or right).
        
        Args:
            landmarks: List of LandmarkPoint objects
            
        Returns:
            str: Head inclination classification
        """
        left_ear = landmarks[self.landmarks_map["left_ear"]]
        right_ear = landmarks[self.landmarks_map["right_ear"]]
        
        # If left ear is higher than right ear, head is inclined to the right
        if left_ear.y < right_ear.y:
            return "right"
        else:
            return "left"
    
    def _analyze_frontal_shoulder_position(self, landmarks):
        """
        Analyze frontal shoulder position (normal, elevated left, or elevated right).
        
        Args:
            landmarks: List of LandmarkPoint objects
            
        Returns:
            str: Shoulder position classification
        """
        left_shoulder = landmarks[self.landmarks_map["left_shoulder"]]
        right_shoulder = landmarks[self.landmarks_map["right_shoulder"]]
        
        height_diff = left_shoulder.y - right_shoulder.y
        
        threshold = 0.02
        
        if abs(height_diff) <= threshold:
            return "normal"
        elif height_diff > threshold:
            return "elevated_right"
        else:
            return "elevated_left"
    
    def _analyze_lateral_shoulder_position(self, landmarks):
        """
        Analyze lateral shoulder position (normal or anterior rotation).
        
        Args:
            landmarks: List of LandmarkPoint objects
            
        Returns:
            str: Shoulder position classification
        """
        shoulder = landmarks[self.landmarks_map["right_shoulder"]]
        ear = landmarks[self.landmarks_map["right_ear"]]
        
        # Create a vertical line from ear and check if shoulder is in front
        ear_vertical_x = ear.x
        
        threshold = 0.05
        
        if shoulder.x > ear_vertical_x + threshold:
            return "anterior_rotation"
        else:
            return "normal"
    
    def _analyze_lateral_head_position(self, landmarks):
        """
        Analyze lateral head position (normal, anterior, flexion, or extension).
        
        Args:
            landmarks: List of LandmarkPoint objects
            
        Returns:
            str: Head position classification
        """
        ear = landmarks[self.landmarks_map["right_ear"]]
        shoulder = landmarks[self.landmarks_map["right_shoulder"]]
        nose = landmarks[self.landmarks_map["nose"]]
        
        horizontal_diff = ear.x - shoulder.x
        nose_ear_diff = nose.x - ear.x
        
        horizontal_threshold = 0.05
        
        if horizontal_diff > horizontal_threshold:
            # Ear is in front of shoulder
            return "anterior"
        elif nose_ear_diff > horizontal_threshold:
            # Nose is far in front of ear
            return "flexion"
        elif abs(horizontal_diff) <= horizontal_threshold:
            # Ear is aligned with shoulder
            return "normal"
        else:
            return "extension"
    
    def draw_pose_landmarks(self, image_data, show_labels=True):
        """
        Draw pose landmarks on the image.
        
        Args:
            image_data: Image data as bytes or file-like object
            show_labels: Whether to show landmark labels
            
        Returns:
            numpy.ndarray: Image with landmarks drawn
            
        Raises:
            ValueError: If pose detection fails
        """
        image = load_image(image_data)
        image = np.array(image.convert('RGB'))
        
        # Process with pose detector
        result = self._process_image(image_data)
        
        if not result:
            raise ValueError("Failed to detect pose landmarks in the image")
        
        # Use the detector's visualization method
        annotated_image = self.pose_detector.visualize(image, [result])
        
        # Add additional labels for key landmarks if requested
        if show_labels:
            height, width, _ = annotated_image.shape
            
            key_landmarks = {
                "nose": self.landmarks_map["nose"],
                "left_ear": self.landmarks_map["left_ear"],
                "right_ear": self.landmarks_map["right_ear"],
                "left_shoulder": self.landmarks_map["left_shoulder"],
                "right_shoulder": self.landmarks_map["right_shoulder"],
                "left_hip": self.landmarks_map["left_hip"],
                "right_hip": self.landmarks_map["right_hip"]
            }
            
            for name, landmark_idx in key_landmarks.items():
                landmark = result.landmarks[landmark_idx]
                if landmark.visibility > 0.5:  # Only show visible landmarks
                    x, y = int(landmark.x * width), int(landmark.y * height)
                    
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
        
        return cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    
    def analyze_and_visualize(self, frontal_image, lateral_image):
        """
        Analyze posture and create visualizations with annotations.
        
        Args:
            frontal_image: Front view image data (bytes or file-like object)
            lateral_image: Side view image data (bytes or file-like object)
            
        Returns:
            tuple: (analysis_results, frontal_annotated, lateral_annotated)
                analysis_results: Dictionary of posture analysis
                frontal_annotated: Annotated frontal image
                lateral_annotated: Annotated lateral image
                
        Raises:
            ValueError: If pose detection fails on either image
        """
        # Get analysis results
        results = self.analyze_posture(frontal_image, lateral_image)
        
        # Create visualizations
        frontal_annotated = self.draw_pose_landmarks(frontal_image)
        lateral_annotated = self.draw_pose_landmarks(lateral_image)
        
        # Annotate frontal image
        y_pos = 30
        for key, value in results["frontal_view"].items():
            text = f"{key.replace('_', ' ').title()}: {value}"
            cv2.putText(
                frontal_annotated,
                text,
                (10, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )
            y_pos += 30
        
        # Annotate lateral image
        y_pos = 30
        for key, value in results["lateral_view"].items():
            text = f"{key.replace('_', ' ').title()}: {value}"
            cv2.putText(
                lateral_annotated,
                text,
                (10, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )
            y_pos += 30
        
        return results, frontal_annotated, lateral_annotated