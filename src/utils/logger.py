# logger.py
from loguru import logger
import sys
import os
import utils.config as config

if os.name == "nt":
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


logger.remove()
logger.level("STARTUP", no=25, color="<cyan><bold>")

valid_levels = {"INFO", "WARNING", "ERROR", "CRITICAL"}
if config.log_level not in valid_levels:
    logger.warning(f"Invalid LOG_LEVEL '{config.log_level}', defaulting to INFO")
    config.log_level = "INFO"

level_priority = {
    "STARTUP": 0,
    "CRITICAL": 1,
    "ERROR": 2,
    "WARNING": 3,
    "WARN": 3,
    "INFO": 4,
}

min_priority = level_priority.get(config.log_level, 4)


def custom_filter(record):
    lvl = record["level"].name
    if lvl == "STARTUP":
        return True
    return level_priority.get(lvl, 100) <= min_priority


logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>[{level}]</level> <cyan>{message}</cyan>",
    filter=custom_filter,
    colorize=True,
)

__all__ = ["logger"]
