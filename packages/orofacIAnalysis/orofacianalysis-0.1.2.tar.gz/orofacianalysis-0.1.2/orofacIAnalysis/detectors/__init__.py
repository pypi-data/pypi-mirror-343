"""Detection interfaces and implementations for orofacIAnalysis."""

from orofacIAnalysis.detectors.base import (
    FaceDetector,
    HandDetector,
    PoseDetector,
    LandmarkPoint,
    LandmarkResult
)
from orofacIAnalysis.detectors.mediapipe import (
    MediapipeFaceDetector,
    MediapipeHandDetector,
    MediapipePoseDetector
)

# Import DLib detector conditionally
try:
    from orofacIAnalysis.detectors.dlib_detector import DlibFaceDetector
    __all__ = [
        'FaceDetector',
        'HandDetector',
        'PoseDetector',
        'LandmarkPoint',
        'LandmarkResult',
        'MediapipeFaceDetector',
        'MediapipeHandDetector',
        'MediapipePoseDetector',
        'DlibFaceDetector'
    ]
except ImportError:
    __all__ = [
        'FaceDetector',
        'HandDetector',
        'PoseDetector',
        'LandmarkPoint',
        'LandmarkResult',
        'MediapipeFaceDetector',
        'MediapipeHandDetector',
        'MediapipePoseDetector'
    ]