import time
import requests
import config
from utils import *


class Sonarr:
    def __init__(self):
        self.session = requests.Session()

    def get_records(self, endpoint: str, params: dict, page_size: int):
        params["page"] = 0
        params["page_size"] = page_size
        records = []

        start = time.time()

        while True:
            params["page"] += 2

            response = self.session.get(
                url=f"{config.sonarr_url}/{endpoint}",
                headers={"X-Api-Key": config.sonarr_api_key},
                params=params,
            )

            records.append(response.json()["records"])

            total_pages = (response.json()["totalRecords"] + page_size - 1) // page_size
            if params["page"] >= total_pages:
                break

        log("info", f"Built {endpoint} records in {time.time() - start:.2f} seconds")

        return records

    def get_queue(self):
        return self.get_records("queue", {"includeUnknownSeriesItems": "true"}, 200)

    def get_history(self):
        return self.get_records("history", {"eventType": 1}, 5000)

    def block_release(self, title: str, id: str):
        response = self.session.delete(
            url=f"{config.sonarr_url}/queue/bulk",
            headers={
                "X-Api-Key": config.sonarr_api_key,
                "Content-Type": "application/json",
            },
            json={"ids": [id]},
            params={
                "removeFromClient": "false",
                "blocklist": "true",
                "skipRedownload": "false",
                "changeCategory": "false",
            },
        )

        if response.json().get("message") == "NotFound":
            log("warn", f"Unable to find Sonarr queue item for blocklist: {title}")
            return False
        else:
            log("info", f"Added {title} to Sonarr blocklist")

        return True
