import time
import utils.config as config
import sys
from utils.logger import *
from utils.webui import *
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

    def remove_log(self, type: str, torrents):
        n = 0
        for t in torrents:
            n += 1
            logger.log(
                "ACTION", f"({n}/{len(torrents)}) Purging {type} torrent: {t['name']}"
            )

    def imported_purgarr(self):
        while True:
            torrents = [
                t
                for t in self.torrent_client.get_torrents()
                if t["category"] in config.import_labels
            ]

            if torrents is not None:
                self.remove_log("imported", torrents)
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
                self.remove_log("stalled", stalled_torrents)
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

    def webui(self):
        server_address = ("", config.web_port)
        httpd = HTTPServer(server_address, LogHandler)
        logger.info(f"Starting log server at {config.web_host}:{config.web_port}")
        httpd.serve_forever()

    def extension_purgarr(self):
        if config.purge_extensions is not True:
            return

        while True:
            for t in self.torrent_client.get_torrents():
                for f in self.torrent_client.get_torrent_files(t):

                    ext = os.path.splitext(f["name"])[1].lower().replace(".", "", 1)

                    if ext in config.blocked_extensions:
                        source = "unknown"
                        if t["category"] in config.sonarr_labels:
                            source = "Sonarr"
                        elif t["category"] in config.radarr_labels:
                            source = "Radarr"

                        if source != "unknown":
                            logger.info(
                                f"Removing torrent from {source}: {t['name']} with file extension match: .{ext}"
                            )

                        match source:
                            case "Sonarr":
                                self.service = self.sonarr
                            case "Radarr":
                                self.service = self.radarr

                        self.torrent_client.remove_torrents(t["id"])
                        self.service.block_release((t["name"], t["id"]))

            # logger.info(
            #     f"{config.purge_extensions_interval} seconds until next file extension purge"
            # )
            time.sleep(config.purge_extensions_interval)
