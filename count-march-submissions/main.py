import os
import sys

import datetime
import matplotlib.pyplot as plt
import requests

FAC_API_BASE = os.getenv("FAC_API_URL")
FAC_API_KEY = os.getenv("FAC_API_KEY")


def string_to_datetime(strdate):
    parts = strdate.split("-")
    return datetime.datetime(int(parts[0]), int(parts[1]), int(parts[2]))


# aln_from_report_id : string -> list-of strings
# Given a report ID, returns all of the ALNs for associated federal awards
def count_submissions_in_march(year):
    url = f"{FAC_API_BASE}/general"
    hist = {}
    for day in range(1, 32):
        check = string_to_datetime(f"{year}-03-{str(day).zfill(2)}").strftime(
            "%Y-%m-%d"
        )
        print(f"Running {check}...")
        params = {
            "fac_accepted_date": f"eq.{check}",
            # Filter audit_year here maybe?
            # "audit_year": f"eq.{year - 1}"
            "select": "report_id,audit_year,fac_accepted_date",
        }
        res = requests.get(
            url,
            params=params,
            headers={
                "X-API-Key": FAC_API_KEY,
                # "Accept-Profile": "api_v1_3_1"
                },
        )
        resjson = res.json()
        hist[day] = hist.get(day, 0) + len(resjson)
    return hist



hists = {}
# for year in range(16, 24):
# This is the audit year. I add one for the acceptance date.

try:
    int(sys.argv[1])
except:
    print("You must supply a two-digit year.")
    sys.exit(-1)

year = int(sys.argv[1])
print(f"Counting {year}")
h = count_submissions_in_march(year)
print(h)
ls = [key for key, val in h.items() for _ in range(val)]
plt.clf()
obj = plt.hist(ls, bins=31)
ax = plt.gca()
ax.set_ylim([0, 2000])
plt.title(f"Submissions in March of {year}")
plt.xlabel("Day")
plt.ylabel("Audits")
plt.savefig(f"submissions-in-{year}.png")
