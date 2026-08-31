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

    BUG: Does not handle empty list.
    Should raise ValueError with clear message.
    """
    # BAD FIX: Only fixed divide(), forgot to fix average()!
    return sum(numbers) / len(numbers)  # Still raises ZeroDivisionError on empty list
