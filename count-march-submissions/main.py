import os
import requests
import datetime
import matplotlib.pyplot as plt

FAC_API_BASE = os.getenv("FAC_API_URL")
FAC_API_KEY  = os.getenv("API_GOV_KEY")

def string_to_datetime(strdate):
    parts = strdate.split("-")
    return datetime.datetime(int(parts[0]), int(parts[1]), int(parts[2]))

# aln_from_report_id : string -> list-of strings
# Given a report ID, returns all of the ALNs for associated federal awards 
def count_submissions_in_march(year):
    start_date = string_to_datetime(f"{year+1}-03-01")
    end_date = string_to_datetime(f"{year+1}-03-31")
    url = f"{FAC_API_BASE}/general"
    params = {
        "audit_year": f"eq.{year}",
        "select": "report_id,audit_year,fac_accepted_date"
    }
    limit = 20_000
    more = True
    hist = {}
    for off in range(0, 300_000, limit):
        if more:
            res = requests.get(url, 
                            params=params | {"offset": off, "limit": limit-1}, 
                            headers={ "X-API-Key": FAC_API_KEY })
            resjson = res.json()
            if len(resjson) == 0:
                more = False
            else:
                for r in resjson:
                    accepted = string_to_datetime(r["fac_accepted_date"])
                    for day in range(1, 31):
                        if (accepted == string_to_datetime(f"{year+1}-03-{str(day).zfill(2)}")):
                            hist[day] = hist.get(day, 0) + 1
    return hist

hists = {}
for year in range(16, 24):
    print(f"Counting {2000+year}")
    h = count_submissions_in_march(2000 + year) 
    print(h)
    ls = [key for key, val in h.items() for _ in range(val)]
    plt.clf() 
    obj = plt.hist(ls, bins=31)
    ax = plt.gca()
    ax.set_ylim([0, 2000])
    plt.title(f'Submissions in March of {2000+year}')
    plt.xlabel("Day")
    plt.ylabel("Audits")
    plt.savefig(f"submissions-in-{2000+year}.png")
