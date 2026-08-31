"""
Tests for calculator module - demonstrates bugs and verifies fixes.
"""

import pytest
from calculator import add, subtract, multiply, divide, average


class TestBasicOperations:
    """Test basic arithmetic operations."""

    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0

    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5

    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6


class TestDivide:
    """Test division operation including edge cases."""

    def test_divide_normal(self):
        assert divide(10, 2) == 5
        assert divide(9, 3) == 3

    def test_divide_by_zero_raises_value_error(self):
        """BUG: Currently raises ZeroDivisionError instead of ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)


class TestAverage:
    """Test average calculation including edge cases."""

    def test_average_normal(self):
        assert average([1, 2, 3, 4, 5]) == 3
        assert average([10, 20]) == 15

    def test_average_empty_list_raises_value_error(self):
        """BUG: Currently raises ZeroDivisionError instead of ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
            average([])
