from datetime import datetime
import requests
from const import (
    FAC_API_BASE,
    BASE_HEADERS
)
import logging
logger = logging.getLogger(__name__)

def op(op, value):
    return f"{op}.{value}"


def string_to_datetime(strdate):
    parts = strdate.split("-")
    return datetime(int(parts[0]), int(parts[1]), int(parts[2]))

def today():
    return datetime.now().strftime('%Y-%m-%d')

query_count = 0 

def get_query_count():
    global query_count
    return query_count

def fetch_from_api(table, payload):
    global query_count
    query_count += 1
    res = requests.get(f"{FAC_API_BASE}/{table}",
                        params=payload,
                        headers=BASE_HEADERS)
    jres = res.json()
    if len(jres) == 0:
        logger.warn(f"No results found for {table}/{list(payload.items())}")
    return jres