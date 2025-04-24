"""Unit tests for the Cycle class."""

import pytest
import numpy as np
from orofacIAnalysis import Cycle


class TestCycle:
    """Test cases for the Cycle class."""

    def test_initialization(self):
        """Test that a Cycle object can be properly initialized."""
        cycle = Cycle(start_frame=10)
        assert cycle.start_frame == 10
        assert cycle.end_frame == 0
        assert cycle.jaw_movements == []
        assert cycle.jaw_positions == []
        assert cycle.smoothed is None
        assert cycle.peaks is None
        assert cycle.valleys is None
        assert cycle.directions == []
        assert cycle.left == 0
        assert cycle.right == 0
        assert cycle.middle == 0

    def test_set_end_frame(self):
        """Test setting the end frame."""
        cycle = Cycle(start_frame=10)
        cycle.set_end_frame(20)
        assert cycle.end_frame == 20

    def test_fit_with_empty_movements(self):
        """Test that fit raises an exception with empty jaw movements."""
        cycle = Cycle(start_frame=10)
        with pytest.raises(Exception, match="No jaw movements"):
            cycle.fit()

    def test_fit_with_movements(self, sample_jaw_movements):
        """Test fitting a cycle with sample jaw movements."""
        cycle = Cycle(start_frame=10)
        cycle.jaw_movements = sample_jaw_movements
        cycle.fit()
        
        # Check that smoothed data has been generated
        assert cycle.smoothed is not None
        assert len(cycle.smoothed) == len(sample_jaw_movements)
        
        # Check that peaks and valleys have been detected
        assert cycle.peaks is not None
        assert isinstance(cycle.peaks, np.ndarray)
        assert cycle.valleys is not None
        assert isinstance(cycle.valleys, np.ndarray)

    def test_cicly_stats(self, sample_directions):
        """Test calculating cycle statistics."""
        cycle = Cycle(start_frame=10)
        cycle.directions = sample_directions
        cycle.cicly_stats()
        
        # Check that directional counts match expected values
        assert cycle.left == sample_directions.count(0)
        assert cycle.right == sample_directions.count(1)
        assert cycle.middle == sample_directions.count(2)

    def test_to_dict(self, sample_jaw_movements, sample_directions):
        """Test converting cycle to dictionary."""
        cycle = Cycle(start_frame=10)
        cycle.set_end_frame(20)
        cycle.jaw_movements = sample_jaw_movements
        cycle.fit()
        cycle.directions = sample_directions
        cycle.cicly_stats()
        
        cycle_dict = cycle.to_dict()
        
        # Check that all expected keys are present
        expected_keys = [
            "start_frame", "end_frame", "jaw_movements", "peaks", 
            "valleys", "directions", "left", "right", "middle"
        ]
        for key in expected_keys:
            assert key in cycle_dict
        
        # Check some specific values
        assert cycle_dict["start_frame"] == 10
        assert cycle_dict["end_frame"] == 20
        assert len(cycle_dict["jaw_movements"]) == len(sample_jaw_movements)
        assert cycle_dict["directions"] == sample_directions
        assert cycle_dict["left"] == sample_directions.count(0)
        assert cycle_dict["right"] == sample_directions.count(1)
        assert cycle_dict["middle"] == sample_directions.count(2)

    def test_to_json(self, sample_jaw_movements):
        """Test converting cycle to JSON."""
        cycle = Cycle(start_frame=10)
        cycle.set_end_frame(20)
        cycle.jaw_movements = sample_jaw_movements
        cycle.fit()
        
        json_str = cycle.to_json()
        assert isinstance(json_str, str)
        # A valid JSON string should start with {
        assert json_str.startswith("{")
        assert json_str.endswith("}")

    def test_str_representation(self):
        """Test the string representation of a cycle."""
        cycle = Cycle(start_frame=10)
        cycle.set_end_frame(20)
        cycle.jaw_movements = [1, 2, 3]
        cycle.jaw_positions = [(1, 2), (3, 4), (5, 6)]
        cycle.directions = [0, 1, 2]
        
        str_repr = str(cycle)
        assert isinstance(str_repr, str)
        assert "Jaw movements" in str_repr
        assert "Jaw positions" in str_repr
        assert "Chew count: 3" in str_repr
        assert "Start Frame: 10" in str_repr
        assert "End Frame: 20" in str_repr