"""Chewing annotation and analysis module for orofacIAnalysis."""

import json
import os
import tempfile
import numpy as np
import cv2
from typing import Optional, Dict, Any, Union, BinaryIO

from orofacIAnalysis.cycle import Cycle
from orofacIAnalysis.detectors import (
    FaceDetector,
    HandDetector,
    MediapipeFaceDetector,
    MediapipeHandDetector
)


class ChewAnnotator:
    """A class for analyzing chewing patterns in videos.
    
    This class uses face and hand detection to track jaw movements 
    and identify chewing cycles in videos. It can process both 
    local video files and in-memory video data.
    
    By default, it uses MediaPipe for detection but can work with any detector 
    that implements the FaceDetector and HandDetector interfaces.
    
    Attributes:
        hand_detector: Hand detector implementation
        face_detector: Face detector implementation
        cap: OpenCV video capture object
        num_frames: Total number of frames in the video
        cycles: List of detected chewing cycles
    """
    
    def __init__(self, video_path="", video_file=None, 
                hand_detector: Optional[HandDetector] = None,
                face_detector: Optional[FaceDetector] = None):
        """Initialize the ChewAnnotator with a video source and detectors.
        
        Args:
            video_path: Path to a video file (default: "")
            video_file: In-memory video file object (default: None)
            hand_detector: Hand detector implementation (defaults to MediaPipe)
            face_detector: Face detector implementation (defaults to MediaPipe)
            
        Note: 
            Either video_path or video_file should be provided, but not both.
        """
        # Initialize hand detector (use provided or default to MediaPipe)
        self.hand_detector = hand_detector or MediapipeHandDetector(
            static_image_mode=False,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
            max_num_hands=2
        )

        # Initialize face detector (use provided or default to MediaPipe)
        self.face_detector = face_detector or MediapipeFaceDetector(
            static_image_mode=False, 
            max_num_faces=1, 
            min_detection_confidence=0.5
        )

        # Initialize video capture
        if video_path:
            self.cap = cv2.VideoCapture(video_path)
        elif video_file:
            # Create a temporary file to store the video data
            temp_video_file = tempfile.NamedTemporaryFile(
                delete=False, suffix=".mp4")
            temp_video_file.write(video_file.read())
            temp_video_file.close()

            # Use the temporary file path with VideoCapture
            self.cap = cv2.VideoCapture(temp_video_file.name)
            
            # Store the temp file path to clean up later
            self._temp_file_path = temp_video_file.name
        else:
            raise ValueError("Either video_path or video_file must be provided")

        # Get the total number of frames in the video
        self.num_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Initialize list to store detected cycles
        self.cycles = []

    def __del__(self):
        """Clean up resources when the object is destroyed."""
        # Release the video capture
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
            
        # Remove temporary file if it exists
        if hasattr(self, '_temp_file_path') and os.path.exists(self._temp_file_path):
            try:
                os.unlink(self._temp_file_path)
            except:
                pass

    def detect_hand(self, frame):
        """Detect if a hand is present in the frame.
        
        Args:
            frame: OpenCV image frame
            
        Returns:
            bool: True if a hand is detected, False otherwise
        """
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image to detect hands
        results = self.hand_detector.process_image(img_rgb)

        # Check if any hands were detected
        return len(results) > 0

    def analyze_chewing(self, frame_limit=4000):
        """Analyze the video to detect and characterize chewing cycles.
        
        This method processes the video frame by frame, detecting jaw movements
        and identifying chewing cycles based on hand presence and jaw motion.
        
        Args:
            frame_limit: Maximum number of frames to process (default: 4000)
            
        Returns:
            list: List of dictionaries containing cycle data
        """
        frame_count = 0
        past_frame_has_hand = False

        # Create the first cycle
        cycle = Cycle()
        n_cycles = 0

        # Analyze all video frames and separate jaw movements into cycles
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret or frame_count >= frame_limit:
                break
                
            frame_count += 1
            
            # If a hand is detected, a new cycle starts
            if self.detect_hand(frame):
                if not past_frame_has_hand:
                    cycle.set_end_frame(frame_count - 1)
                    
                # Hand detected, continue to next frame
                past_frame_has_hand = True
                continue
            else:
                if past_frame_has_hand:
                    # Hand was present in previous frame but not in current frame
                    # This marks the start of a new cycle
                    self.cycles.append(cycle)
                    cycle = Cycle(start_frame=frame_count - 1)
                    n_cycles += 1
                    past_frame_has_hand = False

            # Process the frame to detect facial landmarks
            h, w, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_results = self.face_detector.process_image(frame_rgb)

            # Extract jaw movement data from facial landmarks
            if face_results:
                face_result = face_results[0]  # Use the first detected face
                landmark_map = self.face_detector.get_landmark_indices()
                
                # Get nose and jaw landmarks
                nose_idx = landmark_map.get("nose", 4)  # Default to MediaPipe index 4 if not mapped
                jaw_idx = landmark_map.get("gnathion", 152)  # Default to MediaPipe index 152 if not mapped
                
                nose = face_result.get_landmark(nose_idx)
                jaw = face_result.get_landmark(jaw_idx)
                
                if nose and jaw:
                    # Get nose and jaw positions
                    nose_y = nose.y * h
                    nose_x = nose.x * w
                    jaw_y = jaw.y * h
                    jaw_x = jaw.x * w

                    # Calculate vertical jaw movement relative to nose
                    cycle.jaw_movements.append(jaw_y - nose_y)
                    cycle.jaw_positions.append((jaw_x, jaw_y))

        # Add the last cycle
        self.cycles.append(cycle)

        # Process each cycle to extract chewing metrics
        for i, cycle in enumerate(self.cycles):
            # Skip the first cycle (usually incomplete/invalid)
            if i == 0:
                continue

            # Fit the cycle data
            cycle.fit()

            # Analyze each chewing motion within the cycle
            for peak_idx, peak in enumerate(cycle.peaks):
                # Find the next valley after this peak
                valley_candidates = [v for v in cycle.valleys if v > peak]
                if not valley_candidates:
                    continue
                    
                valley = valley_candidates[0]

                # Get jaw positions at peak (open) and valley (closed)
                jaw_open = cycle.jaw_positions[peak]
                jaw_closed = cycle.jaw_positions[valley]

                # Calculate motion vector from open to closed position
                motion_vector = np.array(jaw_closed) - np.array(jaw_open)

                # Analyze horizontal and vertical components of motion
                horizontal_motion = motion_vector[0]  # X-axis
                vertical_motion = motion_vector[1]    # Y-axis

                # Determine chewing direction based on motion vector
                if vertical_motion < 0:  # Moving upward
                    if horizontal_motion > 0:
                        direction = 0  # "Left"
                    elif horizontal_motion < 0:
                        direction = 1  # "Right"
                    else:
                        direction = 2  # "Middle"
                    cycle.directions.append(direction)

            # Calculate statistics for this cycle
            cycle.cicly_stats()

        # Return cycle data as dictionaries
        return [cycle.to_dict() for cycle in self.cycles[1:]]

    def cycles_to_json(self):
        """Convert all cycles to a JSON string.
        
        Returns:
            str: JSON representation of all cycles
        """
        return json.dumps([cycle.to_dict() for cycle in self.cycles[1:]])