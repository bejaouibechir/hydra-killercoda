#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab17-resources
LOG=/tmp/hydra-lab17-setup.log
READY=/tmp/hydra-lab17-ready
FAILED=/tmp/hydra-lab17-failed
STATUS=/tmp/hydra-lab17-status
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
 [ -s "$ASSETS/lab17.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
 sleep 1
done
for file in orders.csv requirements.txt query.solution.sql pandas.solution.py transformations.solution.yaml sources.yaml destinations.yaml pipeline.yaml expected.csv run_sql.py lab17.py errors.py; do
 [ -s "$ASSETS/$file" ]
done
stage="Installing Hydra and pandas"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing CSV and job directory"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/lab17.py" prepare
stage="Ready: SQL, pandas and Hydra exercises"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
