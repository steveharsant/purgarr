import config
import importlib
import sys
import time
from datetime import datetime
from typing import Literal


log_levels = Literal["info", "warn", "error"]
level_map = {"info": 0, "warn": 1, "error": 2}


def log(type: log_levels, message: str, forced=False):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"{now} [{type.upper()}] {message}"

    if level_map[type] >= level_map.get(config.log_level, 0) or forced is True:
        print(log_content)


def set_torrent_client():
    if config.torrent_client is None:
        log(
            "error",
            "No torrent client set. Set TORRENT_CLIENT environment variable and restart",
            True,
        )
        sys.exit(1)

    try:
        return importlib.import_module(f"services.{config.torrent_client}")
    except ImportError as e:
        print(f"Error importing module {config.torrent_client}: {e}")
        return None


def purge_daemon(name: str, match_key: str, match_values: str, wait_interval: int):
    while True:
        matched_torrents = []
        for torrent in torrent_client.get_torrents():
            if torrent[match_key] in match_values:
                matched_torrents.append(torrent)

        count = len(matched_torrents)
        if count > 0:
            log("info", f"Purging {count} {name.lower()} torrents")
            hashes = [t["hash"] for t in matched_torrents]
            torrent_client.remove_torrents(hashes)
        else:
            log("info", f"No torrents matching {match_key} = {match_values}")

        log("info", f"{wait_interval} seconds until next {name.lower()} torrents purge")
        time.sleep(wait_interval)


torrent_client = set_torrent_client()
