"""
Logger utility for logging messages
Prints logs to screen via ch (channel handler), and saves logs to via fh (file handler)
"""
import logging

# set name of log file
log_file = 'utils.log'

# Logger config
logger = logging.getLogger('__log__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

# # create file handler that logs debug messages
# fh = logging.FileHandler(log_file)
# fh.setFormatter(formatter)
# fh.setLevel(logging.DEBUG)

# add ch to logger
logger.addHandler(ch)
# logger.addHandler(fh)
