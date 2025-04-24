#!/usr/bin/env python
"""
Setup script for test environment.
This script creates sample test resources and ensures the test environment is properly configured.
"""

import sys
import argparse
import cv2
import numpy as np
from pathlib import Path

# Define the path to test resources
TEST_RESOURCES_DIR = Path(__file__).resolve().parent / "tests" / "test_resources"


def ensure_directories():
    """Ensure all necessary directories exist."""
    print(f"Creating test resource directory: {TEST_RESOURCES_DIR}")
    TEST_RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create an __init__.py in the test resources directory to make it a proper package
    init_file = TEST_RESOURCES_DIR / "__init__.py"
    if not init_file.exists():
        init_file.touch()
        print(f"Created {init_file}")


def create_sample_video():
    """Create a sample video file for testing chewing analysis."""
    output_path = TEST_RESOURCES_DIR / "sample_chewing2.mp4"
    
    if output_path.exists():
        print(f"Sample video already exists at {output_path}")
        return
    
    print(f"Creating sample chewing video at {output_path}")
    
    # Create a simple video with a moving circle to simulate jaw movement
    width, height = 640, 480
    fps = 30
    duration = 3  # seconds
    
    # Initialize VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    total_frames = int(fps * duration)
    
    # Create frames with a moving circle
    for i in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Draw a circle representing a face
        cv2.circle(frame, (width // 2, height // 2), 100, (255, 255, 255), -1)
        
        # Draw moving "jaw" - circle moving up and down
        y_offset = int(20 * np.sin(i * 0.2))
        cv2.circle(frame, (width // 2, height // 2 + 50 + y_offset), 30, (0, 0, 255), -1)
        
        # Add frame to video
        out.write(frame)
    
    # Release the VideoWriter
    out.release()
    print(f"Created sample video with {total_frames} frames")


def create_sample_face_image():
    """Create a sample face image for testing facial analysis."""
    output_path = TEST_RESOURCES_DIR / "sample_face2.jpg"
    
    if output_path.exists():
        print(f"Sample face image already exists at {output_path}")
        return
    
    print(f"Creating sample face image at {output_path}")
    
    # Create a simple image with a face-like shape
    width, height = 640, 480
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw an oval for the face
    cv2.ellipse(image, (width // 2, height // 2), (100, 150), 0, 0, 360, (255, 255, 255), -1)
    
    # Draw eyes
    cv2.circle(image, (width // 2 - 40, height // 2 - 30), 15, (255, 0, 0), -1)
    cv2.circle(image, (width // 2 + 40, height // 2 - 30), 15, (255, 0, 0), -1)
    
    # Draw nose
    cv2.line(image, (width // 2, height // 2 - 20), (width // 2, height // 2 + 10), (0, 0, 255), 5)
    
    # Draw mouth
    cv2.ellipse(image, (width // 2, height // 2 + 40), (50, 20), 0, 0, 180, (0, 255, 0), 5)
    
    # Save the image
    cv2.imwrite(str(output_path), image)
    print(f"Created sample face image")


def create_sample_posture_images():
    """Create sample frontal and lateral posture images for testing posture analysis."""
    frontal_path = TEST_RESOURCES_DIR / "sample_frontal2.jpg"
    lateral_path = TEST_RESOURCES_DIR / "sample_lateral2.jpg"
    
    if frontal_path.exists() and lateral_path.exists():
        print(f"Sample posture images already exist")
        return
    
    print(f"Creating sample posture images")
    
    # Create a simple frontal posture image
    width, height = 640, 480
    frontal_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw a stick figure - head
    cv2.circle(frontal_image, (width // 2, height // 4), 30, (255, 255, 255), -1)
    
    # Draw shoulders
    cv2.line(frontal_image, (width // 2 - 80, height // 3), (width // 2 + 80, height // 3), (255, 255, 255), 5)
    
    # Draw body
    cv2.line(frontal_image, (width // 2, height // 4 + 30), (width // 2, height // 3 * 2), (255, 255, 255), 5)
    
    # Draw legs
    cv2.line(frontal_image, (width // 2, height // 3 * 2), (width // 2 - 50, height), (255, 255, 255), 5)
    cv2.line(frontal_image, (width // 2, height // 3 * 2), (width // 2 + 50, height), (255, 255, 255), 5)
    
    # Draw arms
    cv2.line(frontal_image, (width // 2 - 80, height // 3), (width // 2 - 120, height // 2), (255, 255, 255), 5)
    cv2.line(frontal_image, (width // 2 + 80, height // 3), (width // 2 + 120, height // 2), (255, 255, 255), 5)
    
    # Save frontal image
    cv2.imwrite(str(frontal_path), frontal_image)
    
    # Create a simple lateral posture image
    lateral_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw a stick figure in profile - head
    cv2.circle(lateral_image, (width // 3, height // 4), 30, (255, 255, 255), -1)
    
    # Draw neck
    cv2.line(lateral_image, (width // 3, height // 4 + 30), (width // 3, height // 3), (255, 255, 255), 5)
    
    # Draw body
    cv2.line(lateral_image, (width // 3, height // 3), (width // 3, height // 3 * 2), (255, 255, 255), 5)
    
    # Draw leg
    cv2.line(lateral_image, (width // 3, height // 3 * 2), (width // 3 + 50, height), (255, 255, 255), 5)
    
    # Draw arms
    cv2.line(lateral_image, (width // 3, height // 2), (width // 3 + 70, height // 2), (255, 255, 255), 5)
    
    # Save lateral image
    cv2.imwrite(str(lateral_path), lateral_image)
    print(f"Created sample posture images")


def setup_test_env():
    """Set up the complete test environment."""
    ensure_directories()
    create_sample_video()
    create_sample_face_image()
    create_sample_posture_images()
    
    print("\nTest environment setup complete!")
    print(f"Test resources are located at: {TEST_RESOURCES_DIR}")
    print("\nRun tests with: pytest")
    print("Run unit tests only: pytest tests/unit/")
    print("Run integration tests only: pytest tests/integration/")
    print("Generate coverage report: pytest --cov=orofacIAnalysis")


def run_tests(args):
    """Run the tests with the specified options."""
    import pytest
    
    # Build the pytest arguments
    pytest_args = []
    
    if args.unit or args.test:
        pytest_args.append("tests/unit/")
    if args.integration or args.test:
        pytest_args.append("tests/integration/")
    
    if args.verbose:
        pytest_args.append("-v")
    
    if args.coverage or args.test:
        pytest_args.append("--cov=orofacIAnalysis")
        if args.coverage_report:
            pytest_args.append(f"--cov-report={args.coverage_report}")
    
    print(f"Running tests with arguments: {' '.join(pytest_args)}")
    return pytest.main(pytest_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up OrofacIAnalysis test environment and run tests")
    
    # Setup options
    parser.add_argument("--setup", action="store_true", help="Set up the test environment")
    
    # Test running options
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--test", action="store_true", help="Run all tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Run tests with verbose output")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--coverage-report", default="term", 
                        choices=["term", "html", "xml", "annotate"],
                        help="Coverage report format")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_test_env()
    elif any([args.unit, args.integration, args.coverage, args.test]):
        sys.exit(run_tests(args))
    else:
        # By default, set up the environment
        setup_test_env()