from aln.checks import (
    accuracy_alns,
    categorize_alns
    )
from pprint import pprint

if __name__ in "__main__":
    for year in [16, 17, 18, 19, 20, 21, 22]:
        categories = categorize_alns(2000+year)
        pprint(categories)
        valid, total = accuracy_alns(2000+year)
        print({"valid": valid, "total": total})
     