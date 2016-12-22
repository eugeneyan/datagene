"""
Utility decorators
"""
import datetime
from logger import logger


def timer(function_to_time):
    """
    Decorator that times the duration to get result from function

    :param function_to_time:
    :return:
    """
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()

        result = function_to_time(*args)

        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        elapsed_time = elapsed_time.total_seconds() * 1000
        logger.debug('Time taken: {} ms'.format(elapsed_time))

        return result, elapsed_time

    return wrapper
