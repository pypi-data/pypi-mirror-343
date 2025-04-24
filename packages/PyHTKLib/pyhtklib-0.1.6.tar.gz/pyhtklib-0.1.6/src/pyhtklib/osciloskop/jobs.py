import time
import schedule
import os
import json
from typing import List, Dict, Any, Tuple, Optional, Union
from venv import logger
from datetime import datetime as dt, timezone
import argparse

from ..lib.dtos import DataStore, InitializationException, RuntimeException
from .core import Oscilloscope
from .data import OscilloscopeData
from pyhtklib.lib.constants import API_KEY, ES_USERNAME, ES_PASSWORD, GET_ES_OSICLLO_DATA_INDEX

oscilloscope = Oscilloscope()

def _measurement_task():
    try:
        logger.info("Executing scheduled measurement_task...")
        now = dt.now(timezone.utc)
        DataStore.timestamp_start_mesurement_task = now
        
        # Initialize oscilloscope if needed
        if not DataStore.oscillo.init_ok:
            if not oscilloscope.initialize():
                logger.error("Failed to initialize oscilloscope. Stopping the program.")
                import sys
                sys.exit(1)  # Exit with error code 1
        
        # Collect measurements
        batches = oscilloscope.collect_measurements(DataStore.oscillo.n_snapshots)
        if not batches:
            logger.error("No measurements collected!")
            return
            
        # Process data (write to files and send to database)
        oscilloscope.process_data(batches)
        
    except InitializationException as ie:
        # This exception is caught/raised when oscilo returns 0 in initialization process
        # if such event happens, whole program is terminated with the information to restart the program.
        logger.error(str(ie), exc_info=True)
        # stop_event.set()  # ! Setting stop event will force application to stop
    except RuntimeException as re:
        # This exception is caught/raised when oscilo returns 0 in measure process meaning it went/is down
        # if down, initialization of oscilo will be triggered.
        logger.warning(str(re))
    except Exception as e:
        logger.error(str(e), exc_info=True)
    
    logger.info("Finished measurement_task")
    return


def parse_configurations() -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Parse command line arguments and load configuration files.
    
    Returns:
        Tuple[Optional[str], Optional[Dict[str, Any]]]: 
            (config_file_path, database_settings_dict)
    """
    # Set up argument parser for custom config file
    parser = argparse.ArgumentParser(description="Oscilloscope Data Acquisition")
    parser.add_argument("--config", type=str, help="Path to custom configuration file")
    parser.add_argument("--db-config", type=str, help="Path to database configuration file")
    args = parser.parse_args()
    
    config_file = None
    db_settings = None
    
    # If custom config file provided, use it
    if args.config and os.path.exists(args.config):
        config_file = args.config
        logger.info(f"Using custom configuration from {args.config}")
    
    # If custom database config file provided, use it
    if args.db_config and os.path.exists(args.db_config):
        try:
            with open(args.db_config, 'r') as file:
                db_settings = json.load(file)
            logger.info(f"Using custom database settings from {args.db_config}")
        except Exception as e:
            logger.error(f"Error loading database settings: {str(e)}")
            
    return config_file, db_settings



# def heartbeat_job():
#     logger.info("Starting heartbeat job...")
#     # Add the code for your heartbeat job here
#     logger.info("Heartbeat job completed.")