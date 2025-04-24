"""orofacIAnalysis - A library for analyzing chewing patterns, facial measurements, and posture using computer vision."""

__version__ = "0.1.0"

# Import main classes and functions to expose at the package level
from orofacIAnalysis.cycle import Cycle
from orofacIAnalysis.chew_annotator import ChewAnnotator
from orofacIAnalysis.landmarks import Landmarks
from orofacIAnalysis.smoothing import (
    SmoothingMethods,
    SmoothingMethodsList,
    apply_smoothing
)
from orofacIAnalysis.utils import (
    euclidian_distance,
    axis_translation,
    pandas_entropy,
    butterworth_filter,
    moving_average,
    exponential_smoothing,
    spline_smoothing
)
from orofacIAnalysis.face import FacialAnalyzer
from orofacIAnalysis.posture import PostureAnalyzer

# Import detector interfaces and implementations
from orofacIAnalysis.detectors import (
    FaceDetector,
    HandDetector,
    PoseDetector,
    MediapipeFaceDetector,
    MediapipeHandDetector,
    MediapipePoseDetector
)

# Try to import DLib detector
try:
    from orofacIAnalysis.detectors import DlibFaceDetector
except ImportError:
    pass