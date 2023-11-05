import pytest
from merge_lines import are_lines_close

def test_are_lines_close_identical_lines():
    assert are_lines_close(10, 5, 10, 5, 0.1, 0.1) is True

def test_are_lines_close_just_within_threshold():
    assert are_lines_close(10, 5, 10.09, 5.09, 0.1, 0.1) is True

def test_are_lines_close_just_outside_threshold():
    assert are_lines_close(10, 5, 10.11, 5.11, 0.1, 0.1) is False

def test_are_lines_close_negative_values():
    assert are_lines_close(-10, -5, -10, -5, 0.1, 0.1) is True

def test_are_lines_close_with_zero_threshold():
    with pytest.raises(ValueError):
        are_lines_close(10, 5, 10, 5, 0, 0)

def test_are_lines_close_invalid_input():
    with pytest.raises(TypeError):
        are_lines_close("10", 5, 10, 5, 0.1, 0.1)
