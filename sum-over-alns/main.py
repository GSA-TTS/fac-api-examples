import os
import requests
import time
import click
import datetime
from alive_progress import alive_bar
from aln import ALN

# https://stackoverflow.com/questions/17755996/how-to-make-a-list-as-the-default-value-for-a-dictionary
from collections import defaultdict
from pprint import pprint
from collections import namedtuple as NT


FAC_API_BASE = os.getenv("FAC_API_URL")
# This change hard-overrides using the local data.
# This involves leaving out some audits, but it is faster,
# and avoids key limit issues while testing.
# FAC_API_BASE = "http://localhost:3000"
FAC_API_KEY  = os.getenv("API_GOV_KEY")
MAX_RESULTS=4_000_000
STEP_SIZE=19_000

# Basic headers; intended for use locally as well as remotely.
BASE_HEADERS = {
    "x-api-user-id": os.getenv("API_KEY_ID"),
    "authorization": f"Bearer {os.getenv('CYPRESS_API_GOV_JWT')}",
    "X-API-Key": FAC_API_KEY 
}
# class ALN:
#     def __init__(self, agency, program=None):
#         self.agency = agency
#         self.program = program
#     def __repr__(self):
#         if self.program:
#             return f"{self.agency}.{self.program}"
#         else:
#             return f"{self.agency}"
#     def __str__(self):
#         return self.__repr__()
#     def __eq__(self, other):
#         return (self.agency == other.agency 
#                 and self.program == other.program)
#     def __hash__(self):
#       return hash(str(self))
#     def streq(self, string_aln):
#         parts = string_aln.split(".")
#         return (self.agency == parts[0]
#                 and self.program == parts[1])

def load_aln_list(fname):
    alns = set()
    with open(fname, 'r') as fp:
        for line in fp:
            line = line.strip()
            parts = line.split(".")
            if len(parts) == 1:
                alns.add(ALN(parts[0]))
            else:
                alns.add(ALN(parts[0], parts[1]))            
    return list(alns)

def op(op, value):
    return f"{op}.{value}"

def string_to_datetime(strdate):
    parts = strdate.split("-")
    return datetime.datetime(int(parts[0]), int(parts[1]), int(parts[2]))

memoize_dates = {}
def get_date(report_id):
    if memoize_dates.get(report_id, False):
        return string_to_datetime(memoize_dates.get(report_id))
    payload = {
        "report_id": op("eq", report_id),
        "select": ",".join(["report_id", "fac_accepted_date"]),
    }
    res = requests.get(f"{FAC_API_BASE}/general",
                params=payload,
                headers=BASE_HEADERS)
    jres = res.json()
    if len(jres) == 0:
        print(f"NO DATE FOUND FOR {report_id}")
        return datetime.datetime(2024,10,31)
    the_date = jres[0]["fac_accepted_date"]
    memoize_dates[report_id] = the_date
    the_date = string_to_datetime(the_date)
    return the_date

def calculate_for_aln(aln, 
                      audit_year="2023",
                      before_acceptance="2023-06-28"):
    # What report IDs does this ALN appear in?
    # aln : report_id
    aln_to_report_ids = defaultdict(list)
    # What is the total direct amount on that ALN?
    # aln : total
    aln_to_total = defaultdict(lambda: 0)
    # How many times do we see this ALN?
    # aln : count
    aln_to_count = defaultdict(lambda: 0)
    aln_dates = defaultdict(list)
    before_acceptance = string_to_datetime(before_acceptance)

    # We begin by finding this ALN in the federal_awards table
    payload = {
        "limit": STEP_SIZE - 1,
        "federal_agency_prefix": op("eq", aln.agency),
        "audit_year": op("eq", audit_year),
        "is_direct": op("eq", "Y"),
        "select": ",".join(["report_id", "amount_expended", "is_direct", "federal_agency_prefix", "federal_award_extension"])
    }
    # If they included a program, and not just an agency number...
    if aln.program:
        payload["federal_award_extension"] = op("eq", aln.program)

    url = f"{FAC_API_BASE}/federal_awards"

    for start in range(0, MAX_RESULTS, STEP_SIZE):
        payload["offset"] = start
        res = requests.get(url,
                        params=payload,
                        headers=BASE_HEADERS)
        jres = res.json()
        len_jres = len(jres)
        if jres == []:
            break
        elif "code" in jres:
            print("ERROR: ")
            pprint(jres)
            break
        else:
            # Don't bother with another call if we had fewer than the max.
            alive_limit = len(jres)
            # with alive_bar(alive_limit) as bar:
            for r in jres:
                # bar()
                this_date = get_date(r["report_id"])
                r["fac_accepted_date"] = this_date
                if this_date < before_acceptance:
                    aln_to_report_ids[aln].append(r["report_id"])
                    aln_to_count[aln] = aln_to_count.get(aln, 0) + 1
                    aln_dates[aln].append(this_date)
                    if r["is_direct"] == "Y":
                        aln_to_total[aln] = aln_to_total.get(aln, 0) + r["amount_expended"]
            if len_jres < STEP_SIZE:
                break

    return (str(aln), aln_to_report_ids, aln_to_total, aln_to_count)

def get_alns_by_agency_number(audit_year, agency_number):
    # ?select=name,count()&order=name.asc
    payload = {
        "federal_agency_prefix": op("eq", agency_number),
        "select": "federal_award_extension",
        "audit_year": op("eq", audit_year),
    }
    url = f"{FAC_API_BASE}/federal_awards"
    all_alns = set()
    for start in range(0, MAX_RESULTS, STEP_SIZE):
        payload["offset"] = start
        res = requests.get(url,
                        params=payload,
                        headers=BASE_HEADERS)
        jres = res.json()
        len_jres = len(jres)
        if jres == []:
            break
        elif "code" in jres:
            print("ERROR: ")
            pprint(jres)
            break
        else:
            # Don't bother with another call if we had fewer than the max.
            for r in jres:
                all_alns.add(ALN(agency_number, r["federal_award_extension"]))

    return all_alns

@click.command()
@click.argument('list_of_alns')
@click.option('--audit-year', default="2023", help='Audit year')
@click.option('--before-acceptance', default="2023-06-28", help="Acceptance date")
@click.option("--distinct-alns", default=None, help="Each distinct aln under an agency number.")
def main(list_of_alns, audit_year, before_acceptance, distinct_alns):
    if distinct_alns:
        alns = get_alns_by_agency_number(audit_year, distinct_alns)
    else:
        alns = load_aln_list(list_of_alns)
    all_results = []
    for aln in sorted(alns, key=lambda a: f"{a.agency}.{a.program}"):
        results = calculate_for_aln(aln, 
                                    audit_year=audit_year, 
                                    before_acceptance=before_acceptance)
        all_results.append(results)
        print("\t".join([results[0], # ALN
                        str(results[3][aln]), # aln_to_count
                        str(len(set(results[1][aln]))), # aln_to_report_ids
                        str(results[2][aln]) # aln_to_total
                    ]))

if __name__ in "__main__":
    main()