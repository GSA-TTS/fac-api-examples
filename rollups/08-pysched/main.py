import os
import requests

FAC_API_BASE = os.getenv("FAC_API_URL")
FAC_API_KEY  = os.getenv("API_GOV_KEY")

# get_n_report_ids : number -> list-of strings
# Returns `n` report IDs. 
def get_n_report_ids(n):
    url = f"{FAC_API_BASE}/general?select=report_id&limit={n}"
    res = requests.get(url, headers={ "X-API-Key": FAC_API_KEY })
    return list(map(lambda o: o["report_id"], res.json()))

# This field has a long name.
AWPF = "agencies_with_prior_findings"

# get_mc : string -> bool
# Given a report ID, return the previous year schedule
def get_py(rid):
    payload = {
        "report_id": f"eq.{rid}",
        "select": ",".join(["report_id", AWPF])
    }
    url = f"{FAC_API_BASE}/general"
    res = requests.get(url, 
                       params=payload,
                       headers={ "X-API-Key": FAC_API_KEY })
    json = res.json()
    # If there is any number other than 00 listed	
    # PYSCHEDULE=Y
    set_of_agencies = set()
    for find in json:
        numbers = list(filter(lambda n: n != "00", 
                         [n.strip() for n in find[AWPF].split(',')]
                         ))
        set_of_agencies.update(numbers)
    # An empty set is "false" in python
    return bool(set_of_agencies)
    
for rid in get_n_report_ids(50):
    print(rid, get_py(rid))