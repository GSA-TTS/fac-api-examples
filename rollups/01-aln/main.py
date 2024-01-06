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

# aln_from_report_id : string -> list-of strings
# Given a report ID, returns all of the ALNs for associated federal awards 
def aln_from_report_id(rid):
    url = f"{FAC_API_BASE}/federal_awards?select=federal_agency_prefix,federal_award_extension&report_id=eq.{rid}"
    res = requests.get(url, headers={ "X-API-Key": FAC_API_KEY })
    prefixes = list(map(lambda o: o["federal_agency_prefix"], res.json()))
    extensions = list(map(lambda o: o["federal_award_extension"], res.json()))
    return [ f"{pre}.{ext}" for pre, ext in zip(prefixes, extensions) ] 
    
for rid in get_n_report_ids(3):
    print(rid, aln_from_report_id(rid))