#!/bin/bash

set -e

DIST=dist
FILES=notebooks

# https://stackoverflow.com/a/76208774

# I don't want to have anything lingering.
# Environments affect the build. Use the 
# one that we build here... for the build.
# conda deactivate  >/dev/null 2>&1
# deactivate >/dev/null 2>&1

echo "Removing venv"
rm -rf .venv
sleep 2
echo "Creating clean venv"
python3 -m venv .venv
source .venv/bin/activate

if [[ "$VIRTUAL_ENV" != "" ]]
then
  INVENV=1
  echo "In environment $VIRTUAL_ENV"
  sleep 2
else
  INVENV=0
fi

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Cleaning up for install"
rm -f *.db
rm -rf $DIST
rm -rf $FILES/__pycache__

sleep 1

echo "Launching build"
sleep 1
jupyter lite init
jupyter lite build

if [[ $RUN = 1 ]]; then
    pushd $DIST
    python -m http.server 8080
    popd
fi