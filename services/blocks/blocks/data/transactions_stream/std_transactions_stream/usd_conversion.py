from blocks.util.lru.lru import lru_cache_time
import requests
import json
from .wei import wei_to_eth

COIN_GECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

@lru_cache_time(seconds=10, maxsize=1)
def get_usd_conversion()->float:
    d = json.loads(requests.get(COIN_GECKO_URL).text)
    return d["ethereum"]["usd"]

def convert_wei(wei : str)->float:
    return wei_to_eth(wei=wei) * get_usd_conversion()