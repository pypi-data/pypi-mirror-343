"""
Drowsiness Validator Package.

Provides functions to detect drowsiness from images using CNN or facial aspect ratios.
"""
# Make the main function available directly from the package import
from .api import detect_drowsiness

__version__ = "0.1.0" # Corresponds to setup.py version
