"""
PyHTKLib - Python library for Hantek oscilloscope control and data acquisition
"""

__version__ = "0.1.0"

# Use absolute imports
from pyhtklib.osciloskop.core import Oscilloscope
from pyhtklib.lib.constants import API_KEY, ES_USERNAME, ES_PASSWORD, GET_ES_OSICLLO_DATA_INDEX

__all__ = [
    "Oscilloscope", 
    "measurement_job",
    "API_KEY",
    "ES_USERNAME",
    "ES_PASSWORD",
    "GET_ES_OSICLLO_DATA_INDEX"
] 