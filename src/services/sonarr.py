import time
import requests
import utils.config as config
from utils.logger import *
from services.base_arrs import Base


class Sonarr(Base):
    def get_queue(self):
        return self.get_records(
            url=config.sonarr_url,
            endpoint="queue",
            api_key=config.sonarr_api_key,
            params={"includeUnknownSeriesItems": "true", "page_size": 200},
        )

    def get_history(self):
        return self.get_records(
            url=config.sonarr_url,
            endpoint="history",
            api_key=config.sonarr_api_key,
            params={"eventType": 1, "page_size": 5000},
        )

    def block_release(self, title, release_id):
        return super().block_release(
            url=config.sonarr_url,
            api_key=config.sonarr_api_key,
            title=title,
            release_id=release_id,
        )
