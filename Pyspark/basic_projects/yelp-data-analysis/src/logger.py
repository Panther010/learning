import logging

def setup_logger():
    formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)
    log = logging.getLogger('logger')

    return log