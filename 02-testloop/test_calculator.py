"""
Test Suite for Calculator
These tests are GENUINE and must NOT be modified during the demo.
The implementation must be fixed to pass these tests.
"""
import pytest
from calculator import add, multiply, divide


def test_add():
    """Test addition function"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_multiply():
    """Test multiplication function"""
    assert multiply(3, 4) == 12
    assert multiply(5, 0) == 0
    assert multiply(-2, 3) == -6


def test_divide():
    """Test division function with zero check"""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

    # Must handle division by zero
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
