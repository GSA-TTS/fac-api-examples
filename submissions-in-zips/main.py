import os
import requests
import time
import click
import pandas as pd

# https://stackoverflow.com/questions/17755996/how-to-make-a-list-as-the-default-value-for-a-dictionary
from collections import defaultdict
from pprint import pprint

# This code assumes a file called
# list-of-zips.txt
# that contains a list of zip codes to search for, or 
# zip-codes.csv 
# that contains county/state names and zip codes, so that
# a search can be conducted based on the state/county.

FAC_API_BASE = os.getenv("FAC_API_URL")
FAC_API_KEY  = os.getenv("API_GOV_KEY")

def load_zip_set(fname):
    zips = set()
    with open(fname, 'r') as fp:
        for line in fp:
            zips.add(line.strip())
    return zips

def gather_results(url, params):
    res = requests.get(url,
                    params=params,
                    headers={ "X-API-Key": FAC_API_KEY })
    return res.json()

def op(op, value):
    return f"{op}.{value}"

def in_op(values):
    return "in.({})".format(",".join(map(str, values)))

def count_for_zip(zips, date_start, date_end):
    params = {
        "auditee_zip": in_op(zips),
        "select": ",".join(["report_id"])
    }
    if date_start:
        params["fac_accepted_date"] = op("gte", date_start)
    if date_end:
        params["fac_accepted_date"] = op("lte", date_end)

    url = f"{FAC_API_BASE}/general"
    report_ids = gather_results(url, params)
    return len(report_ids)

def zips_by_county(state, county):
    df = pd.read_csv("zip-codes.csv")
    zips = set()
    for index, row in df.iterrows():
        if row["state_name"] == state and county is None:
            zips.add(row["zip"])
        if row["state_name"] == state and row["county_name"] == county:
            zips.add(row["zip"])
    return zips

@click.command()
@click.option("-s", "--state")
@click.option("-c", "--county")
@click.option("--start")
@click.option("--end")
def cli(state, county, start, end):
    if state or county:
        zips = zips_by_county(state, county)
    else:
        zips = load_zip_set("list-of-zips.txt")
    print(zips)
    count = 0
    count += count_for_zip(sorted(zips), start, end)
    time.sleep(0.1)
    print(f"Found {count} report ids.")
    return 0    

if __name__ in "__main__":
    cli()