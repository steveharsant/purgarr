import os

log_level = os.getenv("LOG_LEVEL", "info")
torrent_client = os.getenv("TORRENT_CLIENT")
delete_files = os.getenv("DELETE_FILES", "True").lower() == "true"

qbit_url = f"{os.getenv('QBIT_URL', 'http:// localhost:8080')}/api/v2"
qbit_user = os.getenv("QBIT_USER", "admin")
qbit_pass = os.getenv("QBIT_PASSWORD")
qbit_token_refresh_interval = int(os.getenv("QBIT_TOKEN_REFRESH_INTERVAL", 600))

purge_stalled = os.getenv("PURGE_STALLED", "True").lower() == "true"
purge_stalled_interval = int(os.getenv("PURGE_STALLED_INTERVAL", 7))

purge_imported = os.getenv("PURGE_IMPORTED", "True").lower() == "true"
purge_imported_interval = int(os.getenv("PURGE_IMPORTED_INTERVAL", 5))
import_labels = os.getenv("IMPORT_LABELS", "sonarr-imported,radarr-imported").split(",")

sonarr_url = f"{os.getenv('SONARR_URL', 'http:// localhost:8989')}/api/v3"
sonarr_api_key = os.getenv("SONARR_API_KEY")
