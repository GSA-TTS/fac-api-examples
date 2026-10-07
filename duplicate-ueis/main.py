import requests
import os
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("FAC_API_URL", "https://api.fac.gov")
API_KEY = os.getenv("FAC_API_KEY")
AUDIT_YEAR = os.getenv("AUDIT_YEAR")

continuing = True

all_results = []
start = 0
limit = 20000

print(f"Checking duplicate UEIs for audit year {AUDIT_YEAR}")
print(f"Url: {BASE_URL}")

while continuing:
    req = requests.get(
        f"{BASE_URL}/general",
        params={
            "select": "auditee_uei,audit_year",
            "audit_year": f"eq.{AUDIT_YEAR}",
            "offset": start,
            "limit": limit,
        },
        headers={"x-api-key": API_KEY},
    )
    if req.status_code != 200:
        print(f"Request failed with status code: {req.status_code}")
        print(f"{req.text[:500]}")
        continuing = False
    elif req.json() == []:
        continuing = False
    else:
        all_results = all_results + req.json()
        start += limit

dups = defaultdict(int)

for rec in all_results:
    key = rec["auditee_uei"]
    dups[key] += 1

resub_count = 0
for uei, n in dups.items():
    if n > 1:
        print(f"UEI: {uei}, Submissions: {n}")
        resub_count += 1


print(f"Unique UEIs (entities that submitted): {len(dups)}")
print(f"UEIs with multiple submissions:        {resub_count}")
