from utils.daemons import Daemons
from utils.log import logger
import utils.config as config

import signal
import sys
import threading
import time


__version__ = "0.1.0"

def main():
    signal.signal(signal.SIGINT, handle_sigint)

    d = Daemons()

    if config.purge_imported:
        threading.Thread(
            target=lambda: d.imported_purgarr(),
            daemon=True,
        ).start()

    if config.purge_stalled:
        stalled_daemons = [
            {"service": "sonarr", "url": config.sonarr_url},
            {"service": "radarr", "url": config.radarr_url},
        ]
        for sd in stalled_daemons:
            threading.Thread(
                target=lambda: d.stalled_purgarr(
                    service=f"{sd['service']}", url=f"{sd['url']}"
                ),
                daemon=True,
            ).start()

    logger.log("STARTUP", "All daemons started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping Purgarr", True)


def handle_sigint(signum, frame):
    sys.exit(0)


if __name__ == "__main__":
    main()
