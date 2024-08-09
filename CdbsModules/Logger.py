import time
import logging
from . import CdbsEvn as CdbsEvn


class EventMessage():
    """Stores the message and the level of importance of that message"""

    def __init__(self, level, msg):
        self.level = level
        self.msg = msg

log = logging.getLogger(__name__ + '.cdbs')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

def logger(type_msg, msg):
    """Processing the output of messages for the user and saving them to the log file, if it exists"""

    if type_msg == 'info':
        log.info(f'{msg}\n')
    elif type_msg == 'warning':
        log.warning(f'{msg}\n')
    elif type_msg == 'error':
        log.error(f'{msg}\n')
    elif type_msg == 'critical':
        log.critical(f'{msg}\n')
    else:
        log.debug(f'{msg}\n')

    # 'DEBUG', 'INFO', 'OPERATOR', 'PROPERTY', 'WARNING', 'ERROR', 'ERROR_INVALID_INPUT', 'ERROR_INVALID_CONTEXT', 'ERROR_OUT_OF_MEMORY'
    level = 'DEBUG'
    if type_msg in 'info':
        level = 'INFO'
    if type_msg in 'warning':
        level = 'WARNING'
    if type_msg in {'error', 'critical'}:
        level = 'ERROR'
    CdbsEvn.g_stack_event.append(EventMessage(level, msg))

    # Save the message to the log file if there is a log file in the folder
    if CdbsEvn.g_log_file_path.is_file():
        with open(CdbsEvn.g_log_file_path, 'a') as log_file:
            log_file.write(f'\n{type_msg} {time.time()}: {msg}')