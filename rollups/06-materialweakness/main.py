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
MW = "is_internal_control_material_weakness_disclosed"

# get_mw : string -> bool
# Given a report ID, return the material weakness
def get_mw(rid):
    payload = {
        "report_id": f"eq.{rid}",
        "select": ",".join(["report_id", MW])
    }
    url = f"{FAC_API_BASE}/general"
    res = requests.get(url, 
                       params=payload,
                       headers={ "X-API-Key": FAC_API_KEY })
    json = res.json()
    # If any of the auditee’s findings have MATERIALWEAKNESS = Y	
    # Then MATERIAL WEAKNESS_MP = Y
    is_mw = False
    for find in json:
        # The FAC stores "Yes" and "No"
        if find[MW] == "Yes":
            is_mw = True
        elif find[MW] == "No":
            is_mw = False
        else:
            print(f"Err: MW <- {find[MW]}")
    return is_mw
    
for rid in get_n_report_ids(20):
    print(rid, "Y" if get_mw(rid) else "N")