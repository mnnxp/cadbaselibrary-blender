import logging

get_logger = logging.getLogger(__name__)
get_logger.setLevel(logging.DEBUG)
get_logger.addHandler(logging.StreamHandler())

def logger(type_msg, msg):
    """ Processing the output of messages for the user """
    
    # FIXME: This does not work
    if type_msg == 'error':
        get_logger.error(f'{msg}\n')
    elif type_msg == 'critical':
        get_logger.critical(f'{msg}\n')
    elif type_msg == 'exception':
        get_logger.exception(f'{msg}\n')
    else:
        get_logger.info(f'{msg}\n')
