import requests
import time
import config
from utils import *


def get_auth_token() -> str:
    if not hasattr(get_auth_token, "last_token_refresh"):
        get_auth_token.last_token_refresh = 0

    now = time.time()
    if now - get_auth_token.last_token_refresh > config.qbit_token_refresh_interval:
        log("info", "Refreshing qBittorrent auth token")
        get_auth_token.last_token_refresh = now

        headers = {"Referer": config.qbit_url}
        data = {"username": config.qbit_user, "password": config.qbit_pass}
        session = requests.Session()

        try:
            response = session.post(
                f"{config.qbit_url}/auth/login", headers=headers, data=data
            )
        except:
            log("error", "qBittorrent authentication failed")

        if "SID" in response.cookies:
            global sid
            sid = response.cookies["SID"]
        else:
            log("error", "SID cookie not found in response")


def get_torrents() -> dict:
    get_auth_token()
    try:
        response = requests.get(
            f"{config.qbit_url}/torrents/info", cookies={"SID": sid}
        )
        return response.json()
    except Exception as e:
        log("error", f"Get imported torrents failed: {e}")
        return []


def remove_torrents(hashes: list):
    get_auth_token()
    hashes = "|".join(h for h in hashes)
    try:
        response = requests.post(
            f"{config.qbit_url}/torrents/delete",
            cookies={"SID": sid},
            data={"hashes": hashes, "deleteFiles": config.delete_files},
        )
    except:
        log("error", "Failed to remove imported torrents")


def version():
    get_auth_token()
    response = requests.get(f"{config.qbit_url}/app/version", cookies={"SID": sid})
    return response.text


def purge_daemon(name: str, match_key: str, match_values: str, wait_interval: int):
    while True:
        matched_torrents = []
        for torrent in get_torrents():
            if torrent[match_key] in match_values:
                matched_torrents.append(torrent)

        count = len(matched_torrents)
        if count > 0:
            log("info", f"Purging {count} {name.lower()} torrents")
            hashes = [t["hash"] for t in matched_torrents]
            remove_torrents(hashes)
        else:
            log("info", f"No torrents matching {match_key} = {match_values}")

        log("info", f"{wait_interval} seconds until next {name.lower()} torrents purge")
        time.sleep(wait_interval)
