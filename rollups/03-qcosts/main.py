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

# is_questioned_costs : string -> boolean
# Given a report ID, return whether there were questioned costs
def is_questioned_costs(rid):
    findings_fields=["is_modified_opinion", 
                     "is_other_matters",
                     "is_material_weakness",
                     "is_significant_deficiency"
                     ]
    url = f"{FAC_API_BASE}/findings?select={','.join(findings_fields)}&report_id=eq.{rid}"
    res = requests.get(url, headers={ "X-API-Key": FAC_API_KEY })
    json = res.json()
    
    result = False
    if json:
        for _, val in json[0].items():
            if val == 'Y':
                result = True
    return result
     
for rid in get_n_report_ids(30):
    print(rid, is_questioned_costs(rid))