import requests
import os
import logging
import time

log = logging.getLogger('urllib3')
log.setLevel(logging.DEBUG)

# logging from urllib3 to console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

# print statements from `http.client.HTTPConnection` to console/stdout
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1

def main():
    apikey = os.getenv("API_GOV_KEY")
    target = "api"
    start = 100_000
    end = 119_000
    increment = 100

    for v in range(start, end, increment):
        t0 = time.time()
        response = requests.get(f'https://{target}.fac.gov/passthrough', 
                            params = {
                                "offset": v,
                                "limit": increment
                                },
                            headers = {"X-Api-Key": apikey})
        t1 = time.time()
        print(f"Elapsed: {t1-t0}")
        print(f"{len(response.json())} responses")

if __name__ in "__main__":
    main()