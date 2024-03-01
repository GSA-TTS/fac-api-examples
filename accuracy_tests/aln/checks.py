import logging
from collections import defaultdict
from alive_progress import alive_bar

from base.req import req 
from aln.aln import ALN
from base.constants import (
    FAC_API_BASE
)

logging.basicConfig(level=logging.INFO)

def get_report_ids(year, debug=False):
    gen_url = f"{FAC_API_BASE}/general"
    res = req(gen_url,
            {
                "select": "report_id",
                "audit_year": f"eq.{year}",
            }, 
            debug=debug)
    return res

def accuracy_alns(year, debug=False):
    logger = logging.getLogger("accuracy_alns")
    res = get_report_ids(year)
    valid = 0
    total = 0
    alive_limit = len(res.json())
    with alive_bar(alive_limit) as bar:
        for r in res.json():
            fa_url = f"{FAC_API_BASE}/federal_awards"
            res2 = req(fa_url,
                    {
                        "select": ",".join(["federal_agency_prefix",
                                            "federal_award_extension"]),
                        "report_id": f"eq.{r['report_id']}"
                    }, 
                    debug=debug)
            for r2 in res2.json():
                total += 1
                aln = ALN(r2["federal_agency_prefix"], 
                        r2["federal_award_extension"])
                if aln.is_valid():
                    valid += 1
                else:
                    logger.info(f"INVALID: {r['report_id']} {aln}")
            bar()
        
    return (valid, total)

def categorize_alns(year, debug=False):
    logger = logging.getLogger("categorize_alns")
    res = get_report_ids(year)
    cats = defaultdict(lambda: 0)
    alive_limit = len(res.json())
    with alive_bar(alive_limit) as bar:
        for r in res.json():
            fa_url = f"{FAC_API_BASE}/federal_awards"
            res2 = req(fa_url,
                    {
                        "select": ",".join(["federal_agency_prefix",
                                            "federal_award_extension"]),
                        "report_id": f"eq.{r['report_id']}"
                    }, 
                    debug=debug)
            for r2 in res2.json():
                aln = ALN(r2["federal_agency_prefix"], 
                        r2["federal_award_extension"])
                cats[aln.category()] += 1
            bar()
    return cats