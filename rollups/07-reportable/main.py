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
ICDD = "is_internal_control_deficiency_disclosed"

# get_mc : string -> bool
# Given a report ID, return the reportable condition
def get_rc(rid):
    payload = {
        "report_id": f"eq.{rid}",
        "select": ",".join(["report_id", ICDD])
    }
    url = f"{FAC_API_BASE}/general"
    res = requests.get(url, 
                       params=payload,
                       headers={ "X-API-Key": FAC_API_KEY })
    json = res.json()
    # If any of the auditee’s findings have SIGNIFICANTDEFICIENCY = Y
    # Then the REPORTABLE CONDITION_MP = Y
    is_rc = False
    for find in json:
        # The FAC stores "Yes" and "No"
        if find[ICDD] == "Yes":
            is_rc = True
        elif find[ICDD] == "No":
            is_rc = False
        else:
            print(f"Err: MW <- {find[ICDD]}")
    return is_rc
    
for rid in get_n_report_ids(20):
    print(rid, "Y" if get_rc(rid) else "N")