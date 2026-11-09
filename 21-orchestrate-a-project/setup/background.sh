#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab21-resources
LOG=/tmp/hydra-lab21-setup.log
STATUS=/tmp/hydra-lab21-status
READY=/tmp/hydra-lab21-ready
FAILED=/tmp/hydra-lab21-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed during: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
 [ -s "$ASSETS/lab21.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
 sleep 1
done
for file in requirements.txt prepare.py lab21.py build_reports.py thread.solution.yaml refs.csv stock.csv sales-backup.csv start-db.sh; do [ -s "$ASSETS/$file" ]; done
stage="Installing Hydra and PostgreSQL driver"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing project files"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Starting PostgreSQL"
printf '%s\n' "$stage" >"$STATUS"
bash "$ASSETS/start-db.sh"
stage="Seeding database"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/lab21.py" seed
stage="Ready: four thread workflows and PostgreSQL"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
