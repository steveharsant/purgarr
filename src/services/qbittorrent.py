import requests
import time
import utils.config as config
from datetime import datetime
from utils.logger import *


class QBittorrentClient:
    def __init__(self):
        self.session = requests.Session()
        self.sid = None
        self.last_sid_refresh = 0

    def authenticate(self):
        now = time.time()
        if now - self.last_sid_refresh < config.qbit_token_refresh_interval:
            return

        logger.info("Refreshing qBittorrent auth token")
        headers = {"Referer": config.qbit_url}
        data = {"username": config.qbit_user, "password": config.qbit_pass}

        try:
            self.session.cookies.clear()
            response = self.session.post(
                f"{config.qbit_url}/auth/login", headers=headers, data=data
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"qBittorrent authentication failed | {e}")
            return

        if not "SID" in response.cookies:
            logger.error("SID cookie not found in response")
            return

        self.sid = response.cookies["SID"]
        self.last_sid_refresh = now
        logger.info("Refreshed qBittorrent SID cookie")

    def get_torrents(self) -> list:
        self.authenticate()

        try:
            response = self.session.get(
                f"{config.qbit_url}/torrents/info", cookies={"SID": self.sid}
            )
        except Exception as e:
            logger.error(f"Failed to get torrents| {e}")
            return []

        results = []

        for t in response.json():
            added = datetime.fromtimestamp(int(t["added_on"]))
            now = datetime.now()
            age = (now - added).total_seconds() / 60

            match t["state"]:
                case "error":
                    state = "error"
                case "pausedUP" | "queuedUP" | "uploading" | "stalledUP" | "stoppedUP":
                    state = "finished"
                case "downloading" | "checkingUP" | "checkingDL":
                    state = "processing"
                case "pausedDL":
                    state = "paused"
                case "queuedDL":
                    state = "queued"
                case "stalledDL" | "metaDL":
                    state = "stalled"
                case _:
                    state = "unknown"

            results.append(
                {
                    "age": age,
                    "category": t["category"],
                    "id": t["hash"],
                    "name": t["name"],
                    "state": state,
                }
            )

        return results

    def remove_torrents(self, hashes: list):
        self.authenticate()
        hash_str = "|".join(hashes)
        try:
            self.session.post(
                f"{config.qbit_url}/torrents/delete",
                cookies={"SID": self.sid},
                data={"hashes": hash_str, "deleteFiles": config.delete_files},
            )
        except Exception as e:
            logger.error(f"Failed to remove torrents| {e}")

    def version(self) -> str:
        self.authenticate()
        try:
            response = self.session.get(
                f"{config.qbit_url}/app/version", cookies={"SID": self.sid}
            )
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch version| {e}")
            return "unknown"
