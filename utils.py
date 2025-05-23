import config
from datetime import datetime
from typing import Literal


log_levels = Literal["startup", "info", "warn", "error"]
level_map = {"info": 0, "warn": 1, "error": 2, "startup": 3}


def log(type: log_levels, message: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"{now} [{type.upper()}] {message}"

    if level_map[type] >= level_map.get(config.log_level, 0):
        print(log_content)
