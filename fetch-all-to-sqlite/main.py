import json
import ijson
import os.path
import sys
import pandas as pd
import sqlite3
from collections import defaultdict
from dotenv import load_dotenv
import fac as f

load_dotenv()

BASE_URL = os.getenv("FAC_API_URL", "https://api.fac.gov")
API_KEY = os.getenv("FAC_API_KEY")
DATA_DIR = os.getenv("DATA_DIR", "data")

query_counts = defaultdict(int)


def build_datapath(filename):
    try:
        os.mkdir(DATA_DIR)
    except:
        pass
    return os.path.join(DATA_DIR, filename)


def batched(iterable, size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

    
def first_record(path):
    with open(path, "rb") as fh:
        return next(ijson.items(fh, "item", use_float=True), None)


def download(client, endpoints):
    # Takes around 93m to run, first time.
    for ep in endpoints:
        print(f"fetching {ep}")
        ep_json_filepath = build_datapath(f"{ep}.json")
        # If there is no JSON file for this table, go ahead and do the download.
        if not os.path.isfile(ep_json_filepath):
            print(f"json does not exist. downloading...")
            client.endpoint(ep)
            client.fetch()
            if client.error:
                print(f"fetch failed: {client.error['message']}")

            with open(ep_json_filepath, "w", encoding="utf-8") as f:
                json.dump(client.results(), f, ensure_ascii=False, indent=2)

    # Write the metadata
    metadata_filepath = build_datapath("metadata.json")
    if not os.path.isfile(metadata_filepath):
        with open(metadata_filepath, "w", encoding="utf-8") as f:
            json.dump(client.metadata(), f, ensure_ascii=False, indent=2)


def create_tables(endpoints):
    conn = sqlite3.connect(build_datapath("fac.sqlite"))
    for ep in endpoints:
        print(f"creating table for {ep}")
        path = build_datapath(f"{ep}.json")

        if not os.path.exists(path):
            print(f"skipping table creation for {ep}: file does not exist")
            continue

        if os.path.getsize(path) == 0:
            print(f"skipping table creation for {ep}: file is empty")
            continue

        first = first_record(path)

        fields = ",".join(f"{k} TEXT" for k in first.keys())
        conn.execute(f"CREATE TABLE IF NOT EXISTS {ep} ({fields})")
        conn.commit()
    return conn


def load_data(conn, client, endpoints):
    for ep in endpoints:
        print(f"loading data for {ep}")
        path = build_datapath(f"{ep}.json")

        if not os.path.exists(path):
            print(f"skipping data load for {ep}: file does not exist")
            continue

        if os.path.getsize(path) == 0:
            print(f"skipping table creation for {ep}: file is empty")
            continue

        total = 0
        with open(path, "rb") as f:
            records = ijson.items(f, "item", use_float=True)
            for batch in batched(records, 50000):
                df = pd.DataFrame.from_records(batch)
                df.to_sql(ep, con=conn, if_exists="append", index=False)
                total += len(batch)
                print(f"  inserted {total} rows")

    conn.close()
    client.metadata()


def main():

    if not API_KEY:
        sys.exit("FAC_API_KEY has not been set")
        exit

    client = f.FAC(base=BASE_URL)
    client.api_key(API_KEY)

    print(f"Fetching from: {client._base}")

    endpoints = [
        "general",
        "additional_ueis",
        "additional_eins",
        "findings",
        "federal_awards",
    ]

    print("\n**** Downloading ****\n")
    download(client, endpoints)
    print("\n**** Creating Tables ****\n")
    conn = create_tables(endpoints)
    print("\n**** Loading Data ****\n")
    load_data(conn, client, endpoints)


if __name__ == "__main__":
    main()
