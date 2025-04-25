# pyttsgen/utils.py

import logging
import os

def setup_logger(name: str = "pyttsgen", level: int = logging.INFO) -> logging.Logger:
    """
    Sets up and returns a logger with the provided name and level.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def remove_file(path: str):
    """
    Safely remove a file if it exists.
    """
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as ex:
        logger = setup_logger()
        logger.error("Error removing file %s: %s", path, ex)
