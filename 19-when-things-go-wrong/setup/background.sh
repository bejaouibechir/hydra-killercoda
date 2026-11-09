#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab19-resources
LOG=/tmp/hydra-lab19-setup.log
READY=/tmp/hydra-lab19-ready
FAILED=/tmp/hydra-lab19-failed
STATUS=/tmp/hydra-lab19-status
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
 [ -s "$ASSETS/lab19.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
 sleep 1
done
for file in workflow.yaml requirements.txt prepare.py lab19.py; do [ -s "$ASSETS/$file" ]; done
stage="Installing Hydra"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing four-step workflow"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Ready: four-step failure workflow"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
