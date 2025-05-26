import time
import utils.config as config
import sys
from utils.logger import *
from services.sonarr import Sonarr
from services.radarr import Radarr
from services.qbittorrent import QBittorrentClient


class Daemons:
    def __init__(self):
        self.sonarr = Sonarr()
        self.radarr = Radarr()

        match config.torrent_client.lower():
            case "qbittorrent":
                self.torrent_client = QBittorrentClient()
            case _:
                logger.critical(f"Unsupported torrent client: {config.torrent_client}")
                sys.exit(1)
        try:

            self.torrent_client_version = self.torrent_client.version()
            logger.info(f"Found {config.torrent_client} {self.torrent_client_version}")
        except Exception:
            logger.error(f"Failed to communicate with {config.torrent_client}")
            sys.exit(1)

    def imported_purgarr(self):
        while True:
            torrents = [
                t
                for t in self.torrent_client.get_torrents()
                if t["category"] in config.import_labels
            ]

            if torrents is not None:
                logger.info(f"Purging {len(torrents)} imported torrents")
                self.torrent_client.remove_torrents([t["id"] for t in torrents])
            else:
                logger.info(f"No imported torrents to purge")

            logger.info(
                f"{config.purge_imported_interval} seconds until next imported torrents purge"
            )

            time.sleep(config.purge_imported_interval)

    def stalled_purgarr(self, service: str, url: str):
        if config.purge_stalled is not True:
            return

        match service.lower():
            case "sonarr":
                self.service = self.sonarr
            case "radarr":
                self.service = self.radarr

        while True:

            logger.info(f"Retreiving {service} queue records")
            queue = self.service.get_queue()

            stalled_torrents = [
                t
                for t in self.torrent_client.get_torrents()
                if t["state"] == "stalled" and t["age"] > int(config.torrent_age)
            ]

            if stalled_torrents:
                logger.info(f"Purging {len(stalled_torrents)} stalled torrents")
                self.torrent_client.remove_torrents([t["id"] for t in stalled_torrents])

            if stalled_torrents and config.block_stalled_torrents:
                for st in stalled_torrents:
                    match = next(
                        (q for q in queue[0] if q["title"] == st["name"]), None
                    )
                    if match:
                        self.service.block_release(match["title"], match["id"])

            m = f"{config.purge_stalled_interval} seconds until next stalled {service} torrents purge"
            logger.info(m)

            time.sleep(config.purge_stalled_interval)
