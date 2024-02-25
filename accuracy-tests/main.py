from aln.checks import (
    accuracy_alns,
    categorize_alns
    )
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ALNs")

MAX_RESULTS = 4_000_000
STEP_SIZE = 19_000
AUDITS_TO_CHECK=50_000


if __name__ in "__main__":
    categories = categorize_alns(2022)
    pprint(categories)
    valid, total = accuracy_alns(2022)
    print({"valid": valid, "total": total})
    