import os
import requests

FAC_API_BASE = os.getenv("FAC_API_URL")
FAC_API_KEY  = os.getenv("API_GOV_KEY")

# paginate_hhs_cog : number, number
def retrieve_cog_awards(year, agency):
    gen_url = f"{FAC_API_BASE}/general"
    res = requests.get(gen_url, 
                       params={
                           "select": "report_id",
                           "audit_year": f"eq.{year}",
                           "cognizant_agency": f"eq.{agency}"
                           },
                       headers={ "X-API-Key": FAC_API_KEY })
    print(f"Agency[{agency}] Records: {len(res.json())}")
    report_ids = set(map(lambda o: o["report_id"], res.json()))
    awards = []
    for report_id in report_ids:
        fa_url = f"{FAC_API_BASE}/federal_awards"
        res = requests.get(fa_url,
                           params={
                               "report_id": f"eq.{report_id}"
                           },
                           headers={ "X-API-Key": FAC_API_KEY })
        print(f"\treport_id[{report_id}]: {len(res.json())} awards")
        awards.append(res.json())
    return awards

treasury = retrieve_cog_awards(2023, 21)
hhs  = retrieve_cog_awards(2023, 93)
