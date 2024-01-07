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

# is_cyfindnigs : string -> boolean
# Given a report ID, return whether there were findings
def is_cyfindings(rid):
    url = f"{FAC_API_BASE}/findings?report_id=eq.{rid}"
    res = requests.get(url, headers={ "X-API-Key": FAC_API_KEY })
    json = res.json()
    # This is a list; if it is not empty, we have findings.
    return json != []

for rid in get_n_report_ids(5):
    print(rid, is_cyfindings(rid))