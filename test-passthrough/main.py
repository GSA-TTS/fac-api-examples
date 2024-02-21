import requests
import os
import logging
import time
import click
from pprint import pprint
from statistics import mean

log = logging.getLogger('urllib3')
log.setLevel(logging.INFO)

# logging from urllib3 to console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
log.addHandler(ch)

# print statements from `http.client.HTTPConnection` to console/stdout
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1


@click.command()
@click.option('--year', default="2023", help='Audit year')
@click.option('--scheme', default="https", help='Audit year')
@click.option('--base', default="api.fac.gov", help='Audit year')
@click.option('--endpoint', default="federal_awards")
@click.option('--agency', default="21")
@click.option('--jwt', default=os.getenv("CYPRESS_API_GOV_JWT"), help='Local JWT')
@click.option('--api-key-id', default=os.getenv("API_KEY_ID"), help='Key ID')
def main(year, scheme, base, endpoint, agency, jwt, api_key_id):
    apikey = os.getenv("API_GOV_KEY")
    start = 0
    end = 2_500_000
    increment = 10000
    response_count = 0
    times = []
    for v in range(start, end, increment):
        t0 = time.time()
        headers = {
            "X-Api-Key": apikey,
            "Authorization": f"Bearer {jwt}",
            "X-API-User-Id": api_key_id,
            # Either specify the range like this...
            "Range-Unit": "items",
            "Range": f"{v}-{v+increment-1}",
            "Prefer": "count=planned",
        }

        response = requests.get(f'{scheme}://{base}/general',
                                headers=headers,
                                params={
                                    "is_multiple_eins": "eq.Yes",
                                    "is_secondary_auditors": "eq.Yes"
                                }
                                )
        json_response = response.json()
        if "code" in json_response:
            pprint(response.json())
            break
        print(f"generals: {len(json_response)}")
        
        for r in json_response:
            for field, table in zip(["is_multiple_eins", "is_secondary_auditors"],
                                    ["additional_eins", "secondary_auditors"]):
                if r[field] == 'Yes':
                    inner = requests.get(f'{scheme}://{base}/{table}',
                                            headers=headers,
                                            params={
                        "report_id": f"eq.{r['report_id']}"
                    })
                    ij = inner.json()
                    if "code" in ij:
                        pass
                    elif len(ij) != 0:
                        print(f"{table}: {len(ij)}")

        t1 = time.time()
        print(f"Elapsed: {t1-t0}")
        response_count += len(response.json())
        times.append(t1-t0)

        print("############################")
        print(f"Rows found: {response_count}")
        print(f"Mean time per query: {mean(times)}")


if __name__ in "__main__":
    (total_rows, times) = main()
