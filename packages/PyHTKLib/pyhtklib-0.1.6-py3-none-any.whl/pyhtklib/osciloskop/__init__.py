"""
Oscilloscope module for Hantek oscilloscope control.
"""

# Use explicit relative imports for running from source
from .core import Oscilloscope

from .data import OscilloscopeData

__all__ = ["Oscilloscope", "OscilloscopeData"]
