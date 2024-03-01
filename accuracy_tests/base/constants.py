import os

FAC_API_BASE = os.getenv("FAC_API_URL")
FAC_API_BASE = "http://localhost:3000"
FAC_API_KEY = os.getenv("API_GOV_KEY")

BASE_HEADERS = {
    "x-api-user-id": os.getenv("API_KEY_ID"),
    "authorization": f"Bearer {os.getenv('CYPRESS_API_GOV_JWT')}",
    "X-API-Key": FAC_API_KEY
}

