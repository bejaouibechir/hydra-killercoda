#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab20-resources
LOG=/tmp/hydra-lab20-setup.log
STATUS=/tmp/hydra-lab20-status
READY=/tmp/hydra-lab20-ready
FAILED=/tmp/hydra-lab20-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed during: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
  [ -s "$ASSETS/lab20.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
  sleep 1
done
for file in requirements.txt prepare.py common.py lab20.py fail.py workflow.yaml invoices.csv payments.csv start-db.sh; do
  [ -s "$ASSETS/$file" ]
done
stage="Installing Hydra and PostgreSQL driver"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing rollback project"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Starting the lab PostgreSQL container"
printf '%s\n' "$stage" >"$STATUS"
bash "$ASSETS/start-db.sh"
stage="Seeding two baseline tables"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/lab20.py" seed
/opt/hydra/bin/python "$ASSETS/lab20.py" check ready
stage="Ready: Hydra, two tables and workflow"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
