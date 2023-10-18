# Examples

This code is for demonstration purposes only. 

## Requirements

All demos assume the following environment keys are set:

| Var | Value |
| --- | --- |
| `API_GOV_KEY` | A valid api.data.gov key |
| `FAC_API_URL` | The URL to the FAC API |

The production FAC API URL is `https://api.fac.gov/`.

To run the demos, you either need Python 3 or Docker. Docker compose files for the demos are offered as a convenience.

## Running the demos

In each directory, type `make`. This runs

* `docker compose build`
* `docker compose run demo`

in sequence.