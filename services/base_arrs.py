import requests
import config
from utils import *


class Base:
    def __init__(self):
        self.session = requests.Session()

    def get_records(self, url: str, endpoint: str, api_key: str, params: dict):
        params["page"] = 0
        records = []

        while True:
            params["page"] += 1

            try:
                response = self.session.get(
                    url=f"{url}/{endpoint}",
                    headers={"X-Api-Key": api_key},
                    params=params,
                )
            except Exception as e:
                log("error", f"Failed to retrieve records from {url}")
                break

            records.append(response.json()["records"])

            total_pages = (
                response.json()["totalRecords"] + params["page_size"] - 1
            ) // params["page_size"]

            if params["page"] >= total_pages:
                break

        return records

    def block_release(self, url: str, api_key: str, title: str, release_id: str):
        response = self.session.delete(
            url=f"{url}/queue/bulk",
            headers={
                "X-Api-Key": api_key,
                "Content-Type": "application/json",
            },
            json={"ids": [release_id]},
            params={
                "removeFromClient": "false",
                "blocklist": "true",
                "skipRedownload": f"{not config.retry_search}",
                "changeCategory": "false",
            },
        )

        if response.json().get("message") == "NotFound":
            log("warn", f"Unable to find queue item for blocklist: {title}")
            return False
        else:
            log("info", f"Added {title} to blocklist")

        return True
