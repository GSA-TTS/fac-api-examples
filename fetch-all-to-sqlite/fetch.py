import click
import json
import os.path
import pandas as pd
import sqlite3
from collections import defaultdict
import fac as f

config = {
    "FAC_API_KEY": os.getenv("FAC_API_KEY"),
    "FAC_API": "api.fac.gov",
    "DATA_DIR": "data",
}
query_counts = defaultdict(int)


def build_datapath(filename):
    try:
        os.mkdir(config["DATA_DIR"])
    except:
        pass
    return os.path.join(config["DATA_DIR"], filename)


def download(client, endpoints):
    # Takes around 93m to run, first time.
    for ep in endpoints:
        print(f"fetching {ep}")
        ep_json_filepath = build_datapath(f"{ep}.json")
        # If there is no JSON file for this table, go ahead and do the download.
        if not os.path.isfile(ep_json_filepath):
            client.endpoint(ep)
            client.fetch()
            with open(ep_json_filepath, "w", encoding="utf-8") as f:
                json.dump(client.results(), f, ensure_ascii=False, indent=2)

    # Write the metadata
    metadata_filepath = build_datapath("metadata.json")
    if not os.path.isfile(metadata_filepath):
        with open(metadata_filepath, "w", encoding="utf-8") as f:
            json.dump(client.metadata(), f, ensure_ascii=False, indent=2)


def create_tables(endpoints):
    # Create tables
    conn = sqlite3.connect(build_datapath("fac.sqlite"))
    for ep in endpoints:
        ep_json_filepath = build_datapath(f"{ep}.json")
        with open(ep_json_filepath, "r") as f:
            data = json.load(f)
            # Use the first object to create the table
            fields = data[0].keys()
            fields_with_commas = ",".join(map(lambda f: f"{f} TEXT", fields))
            stmt = f"CREATE TABLE IF NOT EXISTS {ep} ({fields_with_commas})"
            print(stmt)
            conn.execute(stmt)
            conn.commit()
    return conn


def load_data(conn, client, endpoints):
    # Load the data
    for ep in endpoints:
        ep_json_filepath = build_datapath(f"{ep}.json")
        with open(ep_json_filepath, "r") as f:
            print(f"Loading {ep_json_filepath}")
            jsn = json.load(f)
            print(f"Converting to dataframe: {len(jsn)} records")
            df = pd.DataFrame.from_records(jsn)
            print(f"Inserting")
            df.to_sql(ep, con=conn, if_exists="append", index=False)

    # Close the connection
    conn.close()
    client.metadata()


@click.command()
def main():
    client = f.FAC()
    client.api_key(config["FAC_API_KEY"])
    endpoints = [
        "additional_ueis",
        "additional_eins",
        "general",
        "findings",
        "federal_awards",
    ]
    print("downloading")
    download(client, endpoints)
    print("creating tables")
    conn = create_tables(endpoints)
    print("loading data")
    load_data(conn, client, endpoints)


if __name__ in "__main__":
    main()
