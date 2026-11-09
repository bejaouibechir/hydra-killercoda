#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab18-resources
LOG=/tmp/hydra-lab18-setup.log
READY=/tmp/hydra-lab18-ready
FAILED=/tmp/hydra-lab18-failed
STATUS=/tmp/hydra-lab18-status
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
 [ -s "$ASSETS/measure.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
 sleep 1
done
for file in workflow.yaml requirements.txt measure.py check.py prepare.py; do [ -s "$ASSETS/$file" ]; done
stage="Installing Hydra"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing workflow and graph file"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Ready: five-step workflow"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
