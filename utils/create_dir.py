"""
Create directories if not already present
"""
import os
from utils.logger import logger


# Create output directory in directory of input file
def create_dir(new_dir):
    """
    Create directory new_dir in current directory
    """
    current_dir = os.getcwd()
    new_dir_path = os.path.join(current_dir, new_dir)
    logger.info('Creating new directory here: {}'.format(new_dir_path))
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)


def create_new_dir(parent_dir, new_dir='output'):
    """
    Create directory new_dir in parent_dir
    """
    new_dir_path = os.path.join(parent_dir, new_dir)
    logger.info('Creating new directory here: {}'.format(new_dir_path))
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
