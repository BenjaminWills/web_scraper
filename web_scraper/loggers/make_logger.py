import logging
import os

# Import Typing

from logging import Logger


def make_logging_directory() -> None:
    """
    Will create a logging directory if it does not already exist.
    """
    if not os.path.exists("logging"):
        os.mkdir("logging")


def get_logger(
    output_path: str,
    save_log: bool = False,
    logger_name: str = __name__,
) -> Logger:
    """Returns a logger that will return log files to the specified output location

    Parameters
    ----------
    output_path : str
        Where the log file should be saved to.

    save_log : bool
        If true will save logs to the output pSath.

    logger_name : str
        Name of the logger
    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(logging.INFO)

    if save_log:
        file_handler = logging.FileHandler(output_path)
        formatter = logging.Formatter("%(asctime)s :: -> %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
