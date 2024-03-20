import os

FAC_API_BASE = os.getenv("FAC_API_URL")
# This change hard-overrides using the local data.
# This involves leaving out some audits, but it is faster,
# and avoids key limit issues while testing.
# FAC_API_BASE = "http://localhost:3000"
FAC_API_KEY = os.getenv("API_GOV_KEY")
MAX_RESULTS = 4_000_000
STEP_SIZE = 20000

# Basic headers; intended for use locally as well as remotely.
BASE_HEADERS = {
    "x-api-user-id": os.getenv("API_KEY_ID"),
    "authorization": f"Bearer {os.getenv('CYPRESS_API_GOV_JWT')}",
    "X-API-Key": FAC_API_KEY
}
