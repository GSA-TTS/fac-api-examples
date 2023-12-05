import os
import requests
import time

# https://stackoverflow.com/questions/17755996/how-to-make-a-list-as-the-default-value-for-a-dictionary
from collections import defaultdict
from pprint import pprint

# This example takes a file containing a list of ALNs,
# and it sums the amount of funding allocated to each 
# of those ALNs.

FAC_API_BASE = os.getenv("FAC_API_URL")
FAC_API_KEY  = os.getenv("API_GOV_KEY")

def load_aln_list(fname):
    alns = set()
    with open(fname, 'r') as fp:
        for line in fp:
            alns.add(line.strip())
    return list(map(lambda s: s.split("."), alns))

def op(op, value):
    return f"{op}.{value}"

def combined(aln):
    return f"{aln[0]}.{aln[1]}"

def calculate_for_aln(aln):
    # What report IDs does this ALN appear in?
    # aln : report_id
    aln_to_report_ids = defaultdict(list)
    # What is the total direct amount on that ALN?
    # aln : total
    aln_to_total = defaultdict(lambda: 0)

    # How many times do we see this ALN?
    # aln : count
    aln_to_count = defaultdict(lambda: 0)

    # We begin by finding this ALN in the federal_awards table
    # select=report_id,amount_expended&
    payload = {
        "federal_agency_prefix": op("eq", aln[0]),
        "federal_award_extension": op("eq", aln[1]),
        "select": ",".join(["report_id", "amount_expended", "is_direct"])
    }
    url = f"{FAC_API_BASE}/federal_awards"
    
    bad_status = False
    while not bad_status:
        res = requests.get(url,
                        params=payload,
                        headers={ "X-API-Key": FAC_API_KEY })
        # print(res.url, res.status_code)

        if res.status_code != 200:
            print(res.status_code)
            bad_status = False
            print(res.text)
            time.sleep(1)
        else:
            bad_status = True
            # print(res.text)
            # print(res.json())

            for r in res.json():
                # print(r)
                aln_to_report_ids[combined(aln)].append(r["report_id"])
                if r["is_direct"]:
                    aln_to_total[combined(aln)] = aln_to_total.get(combined(aln), 0) + r["amount_expended"]
                aln_to_count[combined(aln)] = aln_to_count.get(combined(aln), 0) + 1

    return (combined(aln), aln_to_report_ids, aln_to_total, aln_to_count)
     
# We have to grab report IDs from the findings table.
# Why? Because, for demo purposes, we want to guarantee there are some findings.
alns = load_aln_list("list-of-alns.txt")
for aln in sorted(alns):
    results = calculate_for_aln(aln)
    combo = combined(aln)
    print(",".join([results[0], 
                    # str(len(results[1][combo])),
                    str(results[3][combo]),
                    str(len(set(results[1][combo]))),
                    str(results[2][combo])
                   ]))
    time.sleep(0.5)