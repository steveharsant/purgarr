import signal
import sys
import threading
import time

from utils import *
from daemons import Daemons

def main():
    signal.signal(signal.SIGINT, handle_sigint)

    d = Daemons()
    threading.Thread(
        target=lambda: d.imported_purgarr(),
        daemon=True,
    ).start()

    threading.Thread(
        target=lambda: d.stalled_purgarr(),
        daemon=True,
    ).start()

    log("startup", "All daemons started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("info", "Stopping Purgarr", True)


def handle_sigint(signum, frame):
    sys.exit(0)


if __name__ == "__main__":
    main()
