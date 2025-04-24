# Detector Interfaces for orofacIAnalysis

This module provides generic detector interfaces that can be used with different computer vision libraries for facial landmark detection, hand detection, and pose detection.

## Overview

The detector system consists of:

1. **Base Interfaces**: Abstract classes that define the common functionality for different types of detectors.
2. **Implementation Classes**: Concrete implementations for specific libraries (currently MediaPipe and DLib).
3. **Common Data Structures**: Shared classes like `LandmarkPoint` and `LandmarkResult` that standardize the detection results.

## Using Detectors

All the main analyzer classes (`FacialAnalyzer`, `PostureAnalyzer`, and `ChewAnnotator`) can accept custom detector implementations through their constructors.

### Default Usage (MediaPipe)

```python
# Creates a facial analyzer with the default MediaPipe detector
analyzer = FacialAnalyzer()
```

### Custom MediaPipe Configuration

```python
from orofacIAnalysis.detectors import MediapipeFaceDetector

# Create a detector with custom parameters
detector = MediapipeFaceDetector(
    static_image_mode=True,
    max_num_faces=2,
    min_detection_confidence=0.7
)

# Use the custom detector
analyzer = FacialAnalyzer(face_detector=detector)
```

### Using DLib (if available)

```python
from orofacIAnalysis.detectors import DlibFaceDetector

# Create a DLib detector (requires dlib to be installed)
detector = DlibFaceDetector(
    predictor_path="path/to/shape_predictor_68_face_landmarks.dat",
    upsample_num_times=1
)

# Use DLib instead of MediaPipe
analyzer = FacialAnalyzer(face_detector=detector)
```

## Creating Custom Detectors

You can create your own detector implementations by extending the base classes:

- `FaceDetector`: For facial landmark detection
- `HandDetector`: For hand detection
- `PoseDetector`: For body pose detection

Each detector must implement:

1. `process_image(image)`: Process an image and return detection results
2. `get_landmark_indices()`: Return a dictionary mapping landmark names to indices
3. `visualize(image, results)`: Draw the landmarks on the image

See the example code in `examples/detector_usage.py` for a complete implementation of a custom detector.

## Data Structures

- `LandmarkPoint`: Represents a single landmark point with normalized coordinates (x, y, z) and visibility.
- `LandmarkResult`: Contains a list of landmarks and an overall confidence score for a detected object.

These standard structures allow different detector implementations to work with the same analyzer code.