# ChewMetrics Testing Suite

This directory contains the testing suite for the ChewMetrics library. The tests are organized into unit tests and integration tests, and use pytest as the testing framework.

## Test Structure

- **`unit/`**: Unit tests for individual components
  - `test_cycle.py`: Tests for the Cycle class
  - `test_landmarks.py`: Tests for the Landmarks class
  - `test_smoothing.py`: Tests for smoothing methods
  - `test_utils.py`: Tests for utility functions
  - `test_facial.py`: Tests for facial analysis
  - `test_posture.py`: Tests for posture analysis

- **`integration/`**: Integration tests for end-to-end functionality
  - `test_chew_annotator.py`: Tests for the ChewAnnotator class
  - `test_facial_analyzer.py`: Tests for the FacialAnalyzer class
  - `test_posture_analyzer.py`: Tests for the PostureAnalyzer class

- **`test_resources/`**: Test data and resources
  - `sample_chewing.mp4`: Sample video for chewing tests
  - `sample_face.jpg`: Sample image for facial analysis tests
  - `sample_frontal.jpg`: Sample frontal image for posture tests
  - `sample_lateral.jpg`: Sample lateral image for posture tests

- **`conftest.py`**: Shared pytest fixtures and configuration

## Setting Up the Test Environment

We provide a setup script to create the test environment and generate the necessary test resources. Run the following command from the project root:

```bash
python setup_test_env.py --setup
```

This will:
1. Create the test_resources directory if it doesn't exist
2. Generate sample video and image files for testing
3. Set up other necessary test configurations

## Running the Tests

### Running All Tests

```bash
pytest
```

### Running Only Unit Tests

```bash
pytest tests/unit/
```

### Running Only Integration Tests

```bash
pytest tests/integration/
```

### Running Specific Test Files

```bash
pytest tests/unit/test_cycle.py
```

### Running Tests with Verbose Output

```bash
pytest -v
```

### Generating Coverage Reports

```bash
pytest --cov=chewmetrics
```

Generate HTML coverage report:

```bash
pytest --cov=chewmetrics --cov-report=html
```

## Using the Setup Script for Testing

The `setup_test_env.py` script provides additional options for running tests:

```bash
# Setup environment and run unit tests with coverage
python setup_test_env.py --unit-only --coverage

# Run integration tests with verbose output
python setup_test_env.py --integration-only --verbose

# Generate HTML coverage report
python setup_test_env.py --coverage --coverage-report=html
```

## Writing New Tests

When adding new functionality to the library, please follow these guidelines:

1. Add unit tests for each new component or function
2. Add integration tests for new end-to-end functionality
3. Use appropriate fixtures from conftest.py
4. Ensure tests can run without external dependencies
5. Mock external services and dependencies when necessary

## Continuous Integration

The tests are automatically run in the CI/CD pipeline on:
- Every push to the main branch
- Every pull request to the main branch
- Every release

The CI workflow:
1. Runs tests on multiple Python versions (3.8, 3.9, 3.10, 3.11)
2. Runs unit tests and integration tests separately
3. Generates a coverage report
4. Uploads the coverage report to Codecov