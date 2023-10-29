"""
Summary: 
    Creates and manages the logger.

Example: \\
logger = Logger.get_logger('simpleExample') \\
logger.debug('debug message') \\
logger.info('info message') \\
logger.warning('warn message') \\
logger.error('error message') \\
logger.critical('critical message')
"""

import yaml
import time
import logging
import logging.config
from datetime import datetime


def get_logger(name):
    """
    Sumary: 
        Gets a logger by name

    Args:
        name (str): logger name

    Returns:
        logger: logger object
    """
    try:
        return logging.getLogger(name)
    except:
        logging.error('Failed to get logger')

try:
    with open('../../config/logging.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)

        current_timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        new_name = config['handlers']['file_handler']['filename'].replace('<timestamp>', current_timestamp)
        config['handlers']['file_handler']['filename'] = new_name

        logging.config.dictConfig(config)

except Exception as e:
    print(f"Error loading the YAML configuration: {e}")