# FAC Duplicate UEI Checker

## Description

This script queries the [FAC API](https://api.fac.gov) for all submission records in a specified audit year and counts how many times each Unique Entity Identifier (UEI) appears.

## Environment Variables

Set the following in a `.env` file in the `duplicate-ueis` root directory:

| Variable      | Required | Default               | Description                            |
| ------------- | -------- | --------------------- | -------------------------------------- |
| `FAC_API_KEY` | Yes      | None                  | API key sent in the `x-api-key` header |
| `AUDIT_YEAR`  | Yes      | None                  | Audit year to check                    |
| `FAC_API_URL` | No       | `https://api.fac.gov` | Base URL of the FAC API                |

Example `.env`:

```env
FAC_API_KEY=your-api-key-here
AUDIT_YEAR=2024
FAC_API_URL=https://api.fac.gov
```

## Running the Script

### With Python

```bash
pip install requests python-dotenv
python main.py
```

### With Docker Compose

Docker Compose reads the `.env` file via `env_file` and builds the image from the local `Dockerfile`:

```bash
docker compose up --build
```

Or run once and remove the container afterward:

```bash
docker compose run --rm duplicate-ueis
```
