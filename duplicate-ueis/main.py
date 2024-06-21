import requests
import os
from collections import defaultdict
from math import floor
from pprint import pprint

continuing = True

all_results = []
start = 0
limit = 20000
while continuing:
    req = requests.get("https://api.fac.gov/general",
                    params = {
                        "select": "auditee_uei,audit_year",
                        "audit_year": "eq.2023",
                        "offset": start
                    },
                    headers = {
                        "x-api-key": os.getenv("API_GOV_KEY")
                    }
                    )
    if req.json() == []:
        continuing = False
    else:
        all_results = all_results + req.json()
        start += limit
    
dups = defaultdict(int)

print(f"Found: {len(req.json())}")
for rec in all_results:
    key = rec["auditee_uei"] + "-" + rec["audit_year"]
    dups[key] += 1

# This produces something like:
#
# ABC-2023: 3
# DEF-2023: 1
# XYZ-2023: 9
# ...

resub = defaultdict(int) 
for k, v in dups.items():
    resub[v] += 1

# This now counts how many of each count:

# 1: 28323
# 2: 260
# 3: 41
# 4: 1
# 5: 1
# 9: 2

for k, v in dups.items():
    if v > 2:
        print(f"{k}: {v}")


for k, v in sorted(resub.items(), key=lambda kv: kv[0]):
    print(f"{k} {'re' if k > 1 else ''}submission{'s' if k > 1 else ''}: {v}")

resub_count = 0
for k, v in dups.items():
    if v > 1:
        resub_count += 1

print(f"total: {len(dups)} resub: {resub_count}")