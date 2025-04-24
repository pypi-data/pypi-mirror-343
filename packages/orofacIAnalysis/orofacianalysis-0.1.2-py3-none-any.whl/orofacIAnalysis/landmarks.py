"""Facial landmarks definitions for orofacIAnalysis."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Landmarks:
    """Class containing the main face landmarks indices for MediaPipe Face Mesh.
    
    These indices correspond to specific points on the face detected by MediaPipe's
    face mesh model. They are used to track facial features during chewing analysis.
    """

    # Indices for the left lip region
    LIPS_INDICES_LEFT = [
        32, 37, 39, 40, 43, 57, 58, 61, 78, 80, 81, 82, 83, 84, 85, 86, 87, 88, 91,
        106, 135, 136, 138, 140, 146, 148, 149, 150, 169, 170, 171, 172, 176, 178,
        181, 182, 185, 186, 191, 192, 194, 201, 202, 204, 208, 210, 211, 212, 214,
    ]

    # Indices for the right lip region
    LIPS_INDICES_RIGHT = [
        262, 267, 269, 270, 273, 287, 288, 291, 308, 310, 311, 312, 313, 314, 317,
        318, 321, 324, 335, 364, 365, 367, 369, 375, 377, 378, 379, 394, 395, 396,
        397, 400, 402, 405, 406, 409, 410, 415, 416, 418, 421, 422, 424, 428, 430,
        431, 432, 434, 435,
    ]

    # Indices for nose and mouth (key points for jaw movement tracking)
    NOSE_MOUTH_INDICES = [4, 152]