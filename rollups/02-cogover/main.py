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

# determine_cog_over : string -> string
# Given a report ID, return whether that audit has a cognizant over oversight agency (`C` or `O`)
def determine_cog_over(rid):
    url = f"{FAC_API_BASE}/general?select=cognizant_agency,oversight_agency&report_id=eq.{rid}&limit=1"
    res = requests.get(url, headers={ "X-API-Key": FAC_API_KEY })
    json = res.json()[0]
    cog = json["cognizant_agency"]
    over = json["oversight_agency"]
    if cog:
        return 'C'
    elif over:
        return 'O'
    else:
        # This would be an error
        return 'X'
    
for rid in get_n_report_ids(3):
    print(rid, determine_cog_over(rid))