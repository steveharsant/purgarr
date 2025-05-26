import time
import requests
import utils.config as config
from utils.log import *
from services.base_arrs import Base


class Radarr(Base):
    def get_queue(self):
        return self.get_records(
            url=config.radarr_url,
            endpoint="queue",
            api_key=config.radarr_api_key,
            params={"page_size": 200},
        )

    def get_history(self):
        return self.get_records(
            url=config.radarr_url,
            endpoint="history",
            api_key=config.radarr_api_key,
            params={"eventType": 1, "page_size": 5000},
        )

    def block_release(self, title, release_id):
        return super().block_release(
            url=config.radarr_url,
            api_key=config.radarr_api_key,
            title=title,
            release_id=release_id,
        )
