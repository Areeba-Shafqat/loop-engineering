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

    BUG: Does not handle division by zero properly.
    Should raise ValueError with clear message.
    """
    return a / b  # Bug: Will raise ZeroDivisionError instead of ValueError

def average(numbers):
    """Calculate average of a list of numbers.

    BUG: Does not handle empty list.
    Should raise ValueError with clear message.
    """
    return sum(numbers) / len(numbers)  # Bug: Will raise ZeroDivisionError on empty list
