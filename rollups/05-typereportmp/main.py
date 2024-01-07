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

def set_to_string(in_set):
    result_string = ""
    for v in in_set:
        result_string += v
    return result_string

# get_auditreporttype : string -> listof string
# Given a report ID, return the report types
def get_auditreporttype(rid):
    url = f"{FAC_API_BASE}/federal_awards?select=report_id,audit_report_type&report_id=eq.{rid}"
    res = requests.get(url, headers={ "X-API-Key": FAC_API_KEY })
    json = res.json()
    # We now have a list of values, because there could be multiple awards.
    # "U" if all TYPEREPORT_MP = U or the non-"U" values listed once
    types = set()
    for art in json:
        if art["audit_report_type"] != "":
            types.add(art["audit_report_type"])
    if types == {"U"}:
        return "U"
    elif "U" not in types: 
        return set_to_string(types)
    else:
        return "ERR"
    
for rid in get_n_report_ids(5):
    print(rid, get_auditreporttype(rid))