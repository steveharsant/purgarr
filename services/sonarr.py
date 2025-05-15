import requests
import config
from utils import *


# curl -s -H "X-Api-Key: YOUR_API_KEY" http://localhost:8989/api/v3/series | jq '.[].title'
def test():
    response = requests.get(
        f"{config.sonarr_url}/series", headers={"X-Api-Key": config.sonarr_api_key}
    )
    print(response.json()[0])
