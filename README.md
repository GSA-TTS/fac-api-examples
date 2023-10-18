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

This should build a docker container and run the demo, printing results to the command line. Again, environment variables must be set correctly, or the run will fail.

It is also possible to install the `requests` library and run each `main.py` directly.
 

## About this code

This code does not run in any production system.

This code should not be used in any production system.

It is offered for illustrative/educational purposes only.

"This place is not a place of honor... no highly esteemed deed is commemorated here... nothing valued is here."

https://en.wikipedia.org/wiki/Long-term_nuclear_waste_warning_messages