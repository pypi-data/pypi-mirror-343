"""Facial analysis functionality for orofacIAnalysis."""

import math
import numpy as np
import cv2
from typing import Optional, Dict, Any, Union
from orofacIAnalysis.utils import load_image
from orofacIAnalysis.detectors import (
    FaceDetector,
    MediapipeFaceDetector,
    LandmarkResult
)


class FacialAnalyzer:
    """
    Class for analyzing facial measurements and proportions using facial landmarks.
    
    This analyzer can extract various facial measurements in millimeters and classify
    them as normal, increased, or reduced compared to reference values.
    
    By default, it uses MediaPipe for face detection but can work with any detector 
    that implements the FaceDetector interface.
    """
    
    # Reference values in mm for comparison
    REFERENCE_VALUES = {
        "middle_third": 90,
        "lower_third": 75,
        "total_height": 160,
        "face_width": 140,
        "left_eye_mouth": 80,
        "right_eye_mouth": 80,
        "upper_lip": 8,
        "lower_lip": 10
    }
    
    # Average head width in mm for scaling
    AVERAGE_HEAD_WIDTH_MM = 148
    
    def __init__(self, face_detector: Optional[FaceDetector] = None):
        """Initialize the facial analyzer with a face detector.
        
        Args:
            face_detector: Face detector implementation (defaults to MediaPipe)
        """
        # Use provided detector or create default MediaPipe detector
        self.face_detector = face_detector or MediapipeFaceDetector(
            static_image_mode=True,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
        
        # Get landmark indices from the detector
        self.LANDMARKS = self.face_detector.get_landmark_indices()
    
    @staticmethod
    def classify_value(value, reference):
        """
        Classify a measurement as increased, reduced, or normal based on reference value.
        
        Args:
            value: The measured value
            reference: The reference value for comparison
            
        Returns:
            str: Classification as "increased", "reduced", or "normal"
        """
        if value > reference * 1.1:
            return "increased"
        elif value < reference * 0.9:
            return "reduced"
        return "normal"
    
    @staticmethod
    def calculate_distance(point1, point2, image_width, image_height):
        """
        Calculate Euclidean distance between two points in pixel space.
        
        Args:
            point1: First landmark point
            point2: Second landmark point
            image_width: Width of the image in pixels
            image_height: Height of the image in pixels
            
        Returns:
            float: Distance in pixels
        """
        x1, y1 = int(point1.x * image_width), int(point1.y * image_height)
        x2, y2 = int(point2.x * image_width), int(point2.y * image_height)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def analyze_image(self, image_data):
        """
        Analyze facial measurements from an image.
        
        Args:
            image_data: Image data as bytes or file-like object
            
        Returns:
            dictionary containing facial measurements and classifications
            
        Raises:
            ValueError: If no face is detected in the image
        """
        # Load image
        image = load_image(image_data)
        
        image = np.array(image)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = image.shape
        
        # Process image with face detector
        face_results = self.face_detector.process_image(image_rgb)
        
        if not face_results:
            raise ValueError("No face was detected in the image")
        
        # Use the first detected face
        face_result = face_results[0]
        
        # Extract landmark points
        coordinate_points = {}
        for key, idx in self.LANDMARKS.items():
            landmark = face_result.get_landmark(idx)
            if landmark:
                coordinate_points[key] = landmark
            else:
                raise ValueError(f"Required landmark '{key}' (index {idx}) was not detected")
        
        # Calculate face width in pixels for scaling
        face_width_px = self.calculate_distance(
            coordinate_points["left_face_side"],
            coordinate_points["right_face_side"],
            image_width,
            image_height
        )
        
        # Calculate pixel-to-mm conversion factor
        scale_factor = self.AVERAGE_HEAD_WIDTH_MM / face_width_px
        
        # Calculate and classify all measurements
        middle_third_mm = round(self.calculate_distance(
            coordinate_points["glabella"],
            coordinate_points["subnasal"],
            image_width,
            image_height
        ) * scale_factor, 2)
        
        lower_third_mm = round(self.calculate_distance(
            coordinate_points["subnasal"],
            coordinate_points["gnathion"],
            image_width,
            image_height
        ) * scale_factor, 2)
        
        face_width_mm = round(face_width_px * scale_factor, 2)
        
        total_height_mm = round(self.calculate_distance(
            coordinate_points["glabella"],
            coordinate_points["gnathion"],
            image_width,
            image_height
        ) * scale_factor, 2)
        
        left_eye_lip_distance_mm = round(self.calculate_distance(
            coordinate_points["left_eye_corner"],
            coordinate_points["left_mouth_corner"],
            image_width,
            image_height
        ) * scale_factor, 2)
        
        right_eye_lip_distance_mm = round(self.calculate_distance(
            coordinate_points["right_eye_corner"],
            coordinate_points["right_mouth_corner"],
            image_width,
            image_height
        ) * scale_factor, 2)
        
        upper_lip_mm = round(self.calculate_distance(
            coordinate_points["lowest_upper_lip"],
            coordinate_points["subnasal"],
            image_width,
            image_height
        ) * scale_factor, 2)
        
        lower_lip_mm = round(self.calculate_distance(
            coordinate_points["highest_lower_lip"],
            coordinate_points["gnathion"],
            image_width,
            image_height
        ) * scale_factor, 2)
        
        # Compile results
        results = {
            "middle_third": {
                "value": middle_third_mm,
                "description": self.classify_value(middle_third_mm, 
                                                 self.REFERENCE_VALUES["middle_third"])
            },
            "lower_third": {
                "value": lower_third_mm,
                "description": self.classify_value(lower_third_mm,
                                                 self.REFERENCE_VALUES["lower_third"])
            },
            "face_height": {
                "value": total_height_mm,
                "description": self.classify_value(total_height_mm,
                                                 self.REFERENCE_VALUES["total_height"])
            },
            "face_width": {
                "value": face_width_mm,
                "description": self.classify_value(face_width_mm,
                                                 self.REFERENCE_VALUES["face_width"])
            },
            "left_eye_lip_distance": {
                "value": left_eye_lip_distance_mm,
                "description": self.classify_value(left_eye_lip_distance_mm,
                                                 self.REFERENCE_VALUES["left_eye_mouth"])
            },
            "right_eye_lip_distance": {
                "value": right_eye_lip_distance_mm,
                "description": self.classify_value(right_eye_lip_distance_mm,
                                                 self.REFERENCE_VALUES["right_eye_mouth"])
            },
            "upper_lip": {
                "value": upper_lip_mm,
                "description": self.classify_value(upper_lip_mm,
                                                 self.REFERENCE_VALUES["upper_lip"])
            },
            "lower_lip": {
                "value": lower_lip_mm,
                "description": self.classify_value(lower_lip_mm,
                                                 self.REFERENCE_VALUES["lower_lip"])
            }
        }
        
        return results
    
    def draw_landmarks(self, image_data, show_measurements=True):
        """
        Draw facial landmarks and optionally show measurements on the image.
        
        Args:
            image_data: Image data as bytes or file-like object
            show_measurements: Whether to show measurement annotations
            
        Returns:
            numpy.ndarray: Image with landmarks and optional measurements
            
        Raises:
            ValueError: If no face is detected in the image
        """
        # Load image
        image = load_image(image_data)
        
        image = np.array(image)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = image.shape
        
        # Process image with face detector
        face_results = self.face_detector.process_image(image_rgb)
        
        if not face_results:
            raise ValueError("No face was detected in the image")
        
        # Use the first detected face
        face_result = face_results[0]
        
        # Let the detector visualize the landmarks
        annotated_image = self.face_detector.visualize(image_rgb, [face_result])
        
        # Extract landmark points
        coordinate_points = {}
        for key, idx in self.LANDMARKS.items():
            landmark = face_result.get_landmark(idx)
            if landmark:
                coordinate_points[key] = landmark
            else:
                raise ValueError(f"Required landmark '{key}' (index {idx}) was not detected")
        
        # Draw key points with larger circles and different color
        for name, point in coordinate_points.items():
            x, y = int(point.x * image_width), int(point.y * image_height)
            cv2.circle(annotated_image, (x, y), 5, (255, 0, 0), -1)
            
            # Add labels if showing measurements
            if show_measurements:
                cv2.putText(
                    annotated_image,
                    name,
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA
                )
        
        # Draw measurement lines if requested
        if show_measurements:
            # Middle third
            self._draw_measurement_line(
                annotated_image,
                coordinate_points["glabella"],
                coordinate_points["subnasal"],
                "Middle Third",
                image_width,
                image_height
            )
            
            # Lower third
            self._draw_measurement_line(
                annotated_image,
                coordinate_points["subnasal"],
                coordinate_points["gnathion"],
                "Lower Third",
                image_width,
                image_height
            )
            
            # Face width
            self._draw_measurement_line(
                annotated_image,
                coordinate_points["left_face_side"],
                coordinate_points["right_face_side"],
                "Face Width",
                image_width,
                image_height
            )
        
        return cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    
    def _draw_measurement_line(self, image, point1, point2, label, image_width, image_height):
        """
        Draw a measurement line between two points with a label.
        
        Args:
            image: Image to draw on
            point1: First landmark point
            point2: Second landmark point
            label: Text label for the measurement
            image_width: Width of the image
            image_height: Height of the image
        """
        x1, y1 = int(point1.x * image_width), int(point1.y * image_height)
        x2, y2 = int(point2.x * image_width), int(point2.y * image_height)
        
        # Draw line
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        # Calculate middle point for label
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        
        # Draw label
        cv2.putText(
            image,
            label,
            (mid_x + 5, mid_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            1,
            cv2.LINE_AA
        )

    def _analyze_symmetry(self, symmetry_data):
        score = symmetry_data["symmetry_score"]
        analysis = {
            "score": score,
            "classification": self._classify_symmetry(score),
            "deviations": symmetry_data["deviations"]
        }
        return analysis

    def _analyze_proportions(self, proportion_data):
        thirds = proportion_data["thirds"]
        golden_ratio = proportion_data["golden_ratio"]
        
        return {
            "thirds_analysis": {
                "balance": self._analyze_thirds_balance(thirds),
                "upper": thirds["upper"],
                "middle": thirds["middle"],
                "lower": thirds["lower"]
            },
            "golden_ratio_analysis": {
                "value": golden_ratio,
                "deviation": abs(1.618 - golden_ratio)  # Golden ratio comparison
            }
        }

    def _classify_symmetry(self, score):
        if score >= 0.9:
            return "Excellent symmetry"
        elif score >= 0.8:
            return "Good symmetry"
        elif score >= 0.7:
            return "Fair symmetry"
        else:
            return "Poor symmetry"

    def _analyze_thirds_balance(self, thirds):
        # Analyze balance between facial thirds
        differences = [
            abs(thirds["upper"] - thirds["middle"]),
            abs(thirds["middle"] - thirds["lower"]),
            abs(thirds["upper"] - thirds["lower"])
        ]
        
        if max(differences) < 0.1:
            return "Well balanced"
        elif max(differences) < 0.2:
            return "Slightly unbalanced"
        else:
            return "Unbalanced"

    def _generate_recommendations(self, symmetry_analysis, proportion_analysis):
        recommendations = []
        
        # Add recommendations based on analysis
        if symmetry_analysis["score"] < 0.8:
            recommendations.append("Consider evaluation for facial asymmetry")
            
        if proportion_analysis["thirds_analysis"]["balance"] == "Unbalanced":
            recommendations.append("Evaluate facial thirds proportions")
            
        if proportion_analysis["golden_ratio_analysis"]["deviation"] > 0.2:
            recommendations.append("Consider aesthetic evaluation")
            
        return recommendations
