from blocks.util.lru.lru import lru_cache_time
import requests
import json
from .wei import wei_to_eth
from time import sleep

COIN_GECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
LAST = 1000

@lru_cache_time(seconds=20, maxsize=1)
def get_usd_conversion()->float:
    global LAST
    while True:
        try:
            d : dict = json.loads(requests.get(COIN_GECKO_URL).text)
            LAST = d.get("ethereum", {"usd" : LAST})["usd"]
            return LAST
        except Exception as e:
            return LAST
        
    

def convert_wei(wei : str)->float:
    return wei_to_eth(wei=wei) * get_usd_conversion()