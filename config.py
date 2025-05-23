from dotenv import load_dotenv
import os

load_dotenv()

# Purgarr Behaviour
log_level = os.getenv("LOG_LEVEL", "info")
purge_stalled = os.getenv("PURGE_STALLED", "True").lower() == "true"
purge_stalled_interval = int(os.getenv("PURGE_STALLED_INTERVAL", 300))
block_stalled_torrents = os.getenv("BLOCK_STALLED_TORRENTS", "True").lower() == "true"
purge_imported = os.getenv("PURGE_IMPORTED", "True").lower() == "true"
purge_imported_interval = int(os.getenv("PURGE_IMPORTED_INTERVAL", 600))
delete_files = os.getenv("DELETE_FILES", "True").lower() == "true"

# Torrents
torrent_client = os.getenv("TORRENT_CLIENT")
torrent_age = os.getenv("TORRENT_AGE", 5)

# qBittorrent
qbit_url = f"{os.getenv('QBIT_URL', 'http:// localhost:8080')}/api/v2"
qbit_user = os.getenv("QBIT_USER", "admin")
qbit_pass = os.getenv("QBIT_PASSWORD")
qbit_token_refresh_interval = int(os.getenv("QBIT_TOKEN_REFRESH_INTERVAL", 600))


# Sonarr
sonarr_labels = os.getenv("SONARR_LABELS", "tv-sonarr").split(",")
sonarr_url = f"{os.getenv('SONARR_URL', 'http:// localhost:8989')}/api/v3"
sonarr_api_key = os.getenv("SONARR_API_KEY")
sonarr_import_labels = os.getenv("SONARR_IMPORT_LABELS", "sonarr-imported").split(",")

# Radarr
radarr_labels = os.getenv("RADARR_LABELS", "tv-sonarr").split(",")
radarr_url = f"{os.getenv('RADARR_URL', 'http:// localhost:7878')}/api/v3"
radarr_api_key = os.getenv("RADARR_API_KEY")
radarr_import_labels = os.getenv("RADARR_IMPORT_LABELS", "radarr-imported").split(",")

# Other
import_labels = os.getenv(
    "IMPORT_LABELS", sonarr_import_labels + radarr_import_labels
).split(",")
