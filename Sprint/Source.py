
class Calculator:
    """Simple calculator with add and multiply methods."""

    def add(self, a: int, b: int) -> int:
        return a + b

    def multiply(self, a: int, b: int) -> int:
        return a * b

import pytest

@pytest.fixture
def calc():
    return Calculator()

def test_add(calc):
    assert calc.add(2, 3) == 5

def test_multiply(calc):
    assert calc.multiply(4, 5) == 20

