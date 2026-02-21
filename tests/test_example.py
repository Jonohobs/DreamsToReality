"""
Minimal test to verify pytest setup is working.
"""


def test_basic_math():
    """Test that basic math works."""
    assert 1 + 1 == 2


def test_imports():
    """Test that core dependencies can be imported."""
    import cv2
    import numpy as np
    from PIL import Image

    assert cv2.__version__ is not None
    assert np.__version__ is not None
    assert Image.__version__ is not None
