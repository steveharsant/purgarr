import time
import config
import sys
from utils import *
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
                log("error", f"Unsupported torrent client: {config.torrent_client}")
                sys.exit(1)

        try:
            self.torrent_client_version = self.torrent_client.version()
        except Exception:
            log(
                "error",
                f"Failed to communicate with torrent client: {config.torrent_client}",
            )
            sys.exit(1)

        m = f"Torrent client {config.torrent_client} with version {self.torrent_client_version} is accessible"
        log("info", m)

    def imported_purgarr(self):
        while True:
            torrents = [
                t
                for t in self.torrent_client.get_torrents()
                if t["category"] in config.import_labels
            ]

            if torrents is not None:
                log("info", f"Purging {len(torrents)} imported torrents")
                self.torrent_client.remove_torrents([t["id"] for t in torrents])
            else:
                log("info", f"No imported torrents to purge")

            m = f"{config.purge_imported_interval} seconds until next imported torrents purge"
            log("info", m)

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

            log("info", f"Retreiving {service} queue records")
            queue = self.service.get_queue()

            stalled_torrents = [
                t
                for t in self.torrent_client.get_torrents()
                if t["state"] == "stalled" and t["age"] > int(config.torrent_age)
            ]

            if stalled_torrents:
                log("info", f"Purging {len(stalled_torrents)} stalled torrents")
                self.torrent_client.remove_torrents([t["id"] for t in stalled_torrents])

            if stalled_torrents and config.block_stalled_torrents:
                for st in stalled_torrents:
                    match = next(
                        (q for q in queue[0] if q["title"] == st["name"]), None
                    )
                    if match:
                        self.service.block_release(match["title"], match["id"])

            m = f"{config.purge_stalled_interval} seconds until next stalled {service} torrents purge"
            log("info", m)

            time.sleep(config.purge_stalled_interval)
