import time
import config
import sys
from utils import *
from services.sonarr import Sonarr
from services.qbittorrent import QBittorrentClient


class Daemons:
    def __init__(self):
        self.sonarr = Sonarr()

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
        if config.purge_imported is not True:
            return

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

    def stalled_purgarr(self):
        if config.purge_stalled is not True:
            return

        while True:
            sonarr_queue = self.sonarr.get_queue()
            stalled_torrents = [
                t
                for t in self.torrent_client.get_torrents()
                if t["state"] == "stalled" and t["age"] > 5
            ]

            if stalled_torrents is not None:
                log("info", f"Purging {len(stalled_torrents)} stalled torrents")
                self.torrent_client.remove_torrents([t["id"] for t in stalled_torrents])

            if stalled_torrents is not None and config.block_stalled_torrents:
                for st in stalled_torrents:
                    for q in sonarr_queue[0]:
                        if st["name"] == q["title"]:
                            self.sonarr.block_release(q["title"], q["id"])
                        # else:
                        #     log(
                        #         "warn",
                        #         "Unable to find matching release for {}".format(
                        #             st["name"]
                        #         ),
                        #     )

            m = f"{config.purge_stalled_interval} seconds until next stalled torrents purge"
            log("info", m)

            time.sleep(config.purge_stalled_interval)
