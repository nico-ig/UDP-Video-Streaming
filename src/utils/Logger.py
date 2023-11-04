'''
Creates and manages the logger.

Example: \\
logger = Logger.start_logger('simpleExample') \\
logger.debug('debug message') \\
logger.info('info message') \\
logger.warning('warn message') \\
logger.error('error message') \\
logger.critical('critical message')
'''

import yaml
import logging
import logging.config
from datetime import datetime

from src.utils import Utils

LOGGER = None

def start_logger(name):
    '''
    Starts the logger, it should be called only once per project
    '''
    try:
        with open('config/logging.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)

            current_timestamp = Utils.timestamp()

            file_handler = name + '_file_handler'

            config['handlers'] = {
                'console': config['handlers']['console'],
                file_handler: config['handlers'][file_handler]
            }
            
            config['loggers'] = {name: config['loggers'][name]}

            new_name = config['handlers'][file_handler]['filename'].replace('<timestamp>', current_timestamp)
            config['handlers'][file_handler]['filename'] = new_name

            logging.config.dictConfig(config)

        global LOGGER

        LOGGER = logging.getLogger(name)

    except Exception as e:
        print(f"Error loading the YAML configuration: {e}")