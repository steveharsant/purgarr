from dotenv import load_dotenv
import os

load_dotenv()

def ensure_http(url):
    return url if url.startswith(("http://", "https://")) else "http://" + url

# Logging & WebUI
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
log_output = os.getenv("LOG_OUTPUT", "all").lower()
web_host = os.getenv("WEB_HOST", "http://localhost").lower()
web_port = int(os.getenv("WEB_PORT", 9891))
log_lines = int(os.getenv("LOG_LINES", 100))
log_refresh_interval = int(os.getenv("LOG_REFRESH_INTERVAL", 5))

# Extension Purgarr
purge_extensions = os.getenv("PURGE_EXTENSIONS", "False").lower() == "true"
purge_extensions_interval = int(os.getenv("PURGE_EXTENSIONS_INTERVAL", 60))
blocked_extensions = (
    os.getenv(
        "BLOCKED_EXTENSIONS",
        "exe,bat,cmd,com,scr,pif,vbs,js,ps1,sh,zip,rar,7z,tar.gz,lnk,arj",
    )
    .lower()
    .split(",")
)

# Stalled Purgarr
purge_stalled = os.getenv("PURGE_STALLED", "True").lower() == "true"
purge_stalled_interval = int(os.getenv("PURGE_STALLED_INTERVAL", 300))
block_stalled_torrents = os.getenv("BLOCK_STALLED_TORRENTS", "True").lower() == "true"

# Purgarr Behaviour
purge_imported = os.getenv("PURGE_IMPORTED", "True").lower() == "true"
purge_imported_interval = int(os.getenv("PURGE_IMPORTED_INTERVAL", 600))
retry_search = os.getenv("RETRY_SEARCH", "True").lower() == "true"

# Torrent Client
torrent_client = os.getenv("TORRENT_CLIENT", "qbittorrent")
torrent_age = os.getenv("TORRENT_AGE", 5)
delete_files = os.getenv("DELETE_FILES", "True").lower() == "true"

# qBittorrent
qbit_url = ensure_http(os.getenv("QBIT_URL", "localhost:8080")) + "/api/v2"
qbit_user = os.getenv("QBIT_USER", "admin")
qbit_pass = os.getenv("QBIT_PASSWORD")
qbit_token_refresh_interval = int(os.getenv("QBIT_TOKEN_REFRESH_INTERVAL", 600))

# Sonarr
sonarr_labels = os.getenv("SONARR_LABELS", "tv-sonarr").split(",")
sonarr_url = ensure_http(os.getenv("SONARR_URL", "localhost:8989")) + "/api/v3"
sonarr_api_key = os.getenv("SONARR_API_KEY")
sonarr_imported_label = os.getenv("SONARR_IMPORTED_LABEL", "sonarr-imported")

# Radarr
radarr_labels = os.getenv("RADARR_LABELS", "radarr").split(",")
radarr_url = ensure_http(os.getenv("RADARR_URL", "localhost:7878")) + "/api/v3"
radarr_api_key = os.getenv("RADARR_API_KEY")
radarr_imported_label = os.getenv("RADARR_IMPORTED_LABEL", "radarr-imported")

# Parsed Variables
import_labels = os.getenv(
    "IMPORT_LABELS", f"{sonarr_imported_label}, {radarr_imported_label}"
).split(",")
