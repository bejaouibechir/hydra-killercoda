#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab22-resources
LOG=/tmp/hydra-lab22-setup.log
STATUS=/tmp/hydra-lab22-status
READY=/tmp/hydra-lab22-ready
FAILED=/tmp/hydra-lab22-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed during: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
 [ -s "$ASSETS/lab22.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
 sleep 1
done
for file in requirements.txt prepare.py lab22.py; do [ -s "$ASSETS/$file" ]; done
stage="Installing Hydra"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing master and sub-projects"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Ready: master, CRM dev and billing prod"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
