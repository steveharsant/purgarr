# Purgarr

> ***Plunder the best, purge the rest!***

Purgarr is a lightweight companion to your Arr stack designed to keep your torrent queue clean and ready for high quality downloads.

**Features Include:**

* Cleans your torrent client of media imported by Sonarr and Radarr.
* Detects and removes stalled torrents.
* Adds stalled torrents to Sonarr's and Radarr's blocklist.
* Triggers a search to replace low quality torrents.

> ***Note:** Purgarr is still in a pre-release state and only supports qBittorrent torrent clients.*

## Minimum Setup

### Commandline

```bash
docker run --name purgarr \
  -e QBIT_URL='ip-address-or-hostname-with-port' \
  -e QBIT_PASSWORD='password' \
  -e SONARR_API_KEY='password' \
  -e SONARR_URL='ip-address-or-hostname-with-port' \
  -e RADARR_API_KEY='password' \
  -e RADARR_URL='ip-address-or-hostname-with-port' \
  -p  9891:9891 \
  ghcr.io/steveharsant/purgarr:latest
```

### Docker Compose

```yaml
services:
  purgarr:
    image: ghcr.io/steveharsant/purgarr:latest
    container_name: purgarr
    environment:
      - QBIT_URL='ip-address-or-hostname-with-port'
      - QBIT_PASSWORD='password'
      - SONARR_API_KEY='password'
      - SONARR_URL='ip-address-or-hostname-with-port'
      - RADARR_API_KEY='password'
      - RADARR_URL='ip-address-or-hostname-with-port'
    ports:
      - 9891:9891
    restart: unless-stopped
```

## Environment Variables

The minimum setup assumes Purgarr is running on the same host as your Arr stack. If this is not the case, the below table shows the additional options Purgarr can be configured with.

| Environment Variable        | Type   | Description                                                                                                                                              | Default         | Required |
|-----------------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|
| LOG_LEVEL                   | string | Minimum level of logs to print (Options: `info`, `warn`, `error`)                                                                                        | info            | No       |
| LOG_LINES                   | int    | Number of (most recent) log lines to show in the webUI                                                                                                   | 100             | No       |
| LOG_REFRESH_INTERVAL        | int    | How often new log entried are fetched and displayed in the webUI (seconds)                                                                               | 5 (seconds)     | No       |
| PURGE_STALLED               | string | Enabled/Disable purge of stalled torrents.                                                                                                               | True            | No       |
| PURGE_STALLED_INTERVAL      | int    | Time in seconds between stalled torrent purges                                                                                                           | 300 (seconds)   | No       |
| BLOCK_STALLED_TORRENTS      | bool   | Block stalled torrents in Sonarr/Radarr                                                                                                                  | True            | No       |
| PURGE_IMPORTED              | bool   | Enable/Disable purge of imported torrents                                                                                                                | True            | No       |
| PURGE_IMPORTED_INTERVAL     | int    | Time in seconds between imported torrent purges                                                                                                          | 600 (seconds)   | No       |
| DELETE_FILES                | bool   | Delete files from torrent clients download folder                                                                                                        | True            | No       |
| RETRY_SEARCH                | bool   | Trigger Sonarr/Radarr to search for another release                                                                                                      | True            | No       |
| TORRENT_CLIENT              | string | Torrent client (Options: `qbittorrent`)                                                                                                                  | `qbittorrent`   | No       |
| TORRENT_AGE                 | int    | Grace period in minutes before a torrent is included in a stalled purge check                                                                            | 5 (minutes)     | No       |
| QBIT_URL                    | string | IP address or hostname to QBittorent webUI                                                                                                               | N/A             | Yes      |
| QBIT_USER                   | string | QBittorrent username                                                                                                                                     | admin           | No       |
| QBIT_PASSWORD               | string | QBittorrent password                                                                                                                                     | N/A             | Yes      |
| QBIT_TOKEN_REFRESH_INTERVAL | int    | Time between auth token refresh for qBittorrent                                                                                                          | 600 (seconds)   | No       |
| SONARR_API_KEY              | string | API key for Sonarr                                                                                                                                       | N/A             | Yes      |
| SONARR_LABELS               | string | The label(s) used by Sonarr to link a torrent to a show or episode (use a `,` to separate multiple labels)                                               | tv-sonarr       | No       |
| SONARR_IMPORTED_LABEL       | string | The label used by Sonarr to tag a torrent as having been imported to the library. (Set the Post-Import Category in the advance torrent client settings). | sonarr-imported | No       |
| SONARR_URL                  | string | Sonarr URL                                                                                                                                               | N/A             | Yes      |
| RADARR_API_KEY              | string | API Key for Radarr                                                                                                                                       | N/A             | Yes      |
| RADARR_LABELS               | string | The label(s) used by Radarr to link a torrent to a movie (use a `,` to separate multiple labels)                                                         | radarr          | No       |
| RADARR_URL                  | string | Radarr URL                                                                                                                                               | N/A             | Yes      |
| RADARR_IMPORTED_LABEL       | string | The label used by Radarr to tag a torrent as having been imported to the library. (Set the Post-Import Category in the advance torrent client settings). | radarr-imported | Yes      |
