"""
Simple calculator module with a deliberate bug for Project 4 demonstration.
"""

def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b.

    Args:
        a: numerator
        b: denominator

    Returns:
        The result of a / b

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def average(numbers):
    """Calculate average of a list of numbers.

    Args:
        numbers: List of numbers to average

    Returns:
        The arithmetic mean of the numbers

    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
