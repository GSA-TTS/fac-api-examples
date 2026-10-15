# FAC Fetch All to SQLite

## Description

This script pulls the contents of several endpoints from the [FAC API](https://api.fac.gov), saves each one as a JSON file, and loads them all into a local SQLite database (`fac.sqlite`).

The following endpoints are fetched:

- `general`
- `additional_ueis`
- `additional_eins`
- `findings`
- `federal_awards`

The first run can take a while (around 90 minutes) because of how long the download step takes. JSON files are only downloaded if they don't already exist, so later runs skip straight to building the database. To force a new download, you can delete the existing JSON file/files.

## Environment Variables

Set the following in a `.env` file in the project root:

| Variable      | Required | Default               | Description                                |
| ------------- | -------- | --------------------- | ------------------------------------------ |
| `FAC_API_KEY` | Yes      | None                  | API key used to authenticate with the FAC  |
| `FAC_API_URL` | No       | `https://api.fac.gov` | Base URL of the FAC API                    |
| `DATA_DIR`    | No       | `data`                | Directory for the JSON files and SQLite DB |

Example `.env`:

```env
FAC_API_KEY=your-api-key-here
FAC_API_URL=https://api.fac.gov
DATA_DIR=data
```

## Running the Script

### With Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### With Docker Compose

Docker Compose reads the `.env` file via `env_file` and builds the image from the local `Dockerfile`:

```bash
docker compose up --build
```

## Output

Everything is written to `DATA_DIR`:

| File                  | Description                                      |
| --------------------- | ------------------------------------------------ |
| `<endpoint>.json`     | Raw API results, one file per endpoint           |
| `metadata.json`       | Metadata returned by the FAC client              |
| `fac.sqlite`          | SQLite database with one table per endpoint      |


## Re-running

- **Re-download an endpoint:** delete its JSON file from `DATA_DIR`. Existing files are never re-downloaded.
- **Rebuild the database:** delete `fac.sqlite` before running again. Data is appended to existing tables, so skipping this step will duplicate rows.
- **Empty or failed downloads:** if a fetch fails, no file is written for that endpoint. If there is an empty JSON file, delete it so it gets downloaded again (`find data -size 0`).
