import time
import signal
import sys
import threading

import config
import services.sonarr as sonarr

from utils import *


torrent_client = set_torrent_client()

try:
    torrent_client_version = torrent_client.version()
except:
    log(
        "error",
        f"Failed to communicate with torrent client: {config.torrent_client}",
    )
    sys.exit(1)

log(
    "info",
    f"Torrent client {config.torrent_client} with version {torrent_client_version} is accessible",
)


def main():
    signal.signal(signal.SIGINT, handle_sigint)

    daemons = [
        {
            "name": "Imported",
            "enabled": config.purge_imported,
            "match_key": "category",
            "match_values": config.import_labels,
            "wait_interval": config.purge_imported_interval,
        },
        {
            "name": "Stalled",
            "enabled": config.purge_stalled,
            "match_key": "state",
            "match_values": ["stalledDL", "metaDL"],
            "wait_interval": config.purge_stalled_interval,
        },
    ]

    for daemon in daemons:
        if daemon["enabled"] is True:
            log(
                "info",
                f"Starting {daemon['name'].lower()} torrent purgarr daemon",
                True,
            )
            threading.Thread(
                target=lambda: torrent_client.purge_daemon(
                    name=daemon["name"],
                    match_key=daemon["match_key"],
                    match_values=daemon["match_values"],
                    wait_interval=daemon["wait_interval"],
                ),
                daemon=True,
            ).start()
            time.sleep(3)  # sleep to prevent race condition with qbit auth token

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("info", "Stopping Purgarr", True)


def handle_sigint(signum, frame):
    sys.exit(0)


if __name__ == "__main__":
    main()
