#!/usr/bin/env python
"""
Entry point for the PyHTKLib library.
"""
import logging

from pyhtklib.osciloskop import Oscilloscope

# Configure logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Create oscilloscope instance
    osc = Oscilloscope()
    
    # Run measurement job
    success = osc.measurement_job(
        config_file="measure.config.yaml",  # Use default config file
        validate_db=True  # Validate database settings
    )
    
    if not success:
        import sys
        sys.exit(1)  # Exit with error code if measurement failed

