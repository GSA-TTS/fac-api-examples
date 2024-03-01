import requests
from base.constants import (
    BASE_HEADERS
)

def req(base, params, headers={}, debug=True):
    res = requests.get(base,
                       params=params,
                       headers=BASE_HEADERS | headers)
    if debug:
        print(res.url)
    return res
