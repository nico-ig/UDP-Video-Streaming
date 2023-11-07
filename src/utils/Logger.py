'''
Creates and manages the logger.

Example: \\
Logger.start_logger('simpleExample') \\
logger = Logger.get_logger('simpleExample')
logger.debug('debug message') \\
logger.info('info message') \\
logger.warning('warn message') \\
logger.error('error message') \\
logger.critical('critical message')
'''

import os
import yaml
import logging
import logging.config

from src.utils import Utils

LOGGER = None

def start_logger(*names):
    '''
    Starts the logger, it should be called only once per project
    '''
    try:
        with open('config/logging.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)

            current_timestamp = Utils.timestamp()

            custom_config = {'handlers': {}, 'loggers': {}}
            for name in names:

                # Get the name of file_handler and the object
                handlers_for_name = {}
                handlers_for_name['handlers'] = {}
                file_handler = name + '_file_handler'

                # Creates the directories in file_handler_path
                parts = config['handlers'][file_handler]['filename'].rsplit('/')
                file_handler_path = '/'.join(parts[:-1])
                os.system(f'mkdir -p {file_handler_path}')

                Utils.delete_older_files(file_handler_path)

                # Set the configs for the handler
                for handler in config['loggers'][name]['handlers']:
                    handlers_for_name['handlers'][handler] = config['handlers'][handler]
                        
                custom_config['handlers'] = {**custom_config['handlers'], **handlers_for_name['handlers']}
                custom_config['loggers'][name] = config['loggers'][name]

                # Get the name of log file
                new_name = custom_config['handlers'][file_handler]['filename'].replace('<timestamp>', current_timestamp)
                custom_config['handlers'][file_handler]['filename'] = new_name

            # Set global config to configs for required loggers
            config = {**config, **custom_config}
            logging.config.dictConfig(config)

    except Exception as e:
        print(f"Error loading the YAML configuration: {e}")
        raise Exception("Couldn't start logger")

def set_logger(name):
    '''
    Sets the global logger
    '''
    global LOGGER
    LOGGER = logging.getLogger(name)
    
def get_logger(name):
    '''
    Gets a specific logger
    '''
    return logging.getLogger(name)