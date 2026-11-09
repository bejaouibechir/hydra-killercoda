#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab24-resources
LOG=/tmp/hydra-lab24-setup.log
STATUS=/tmp/hydra-lab24-status
READY=/tmp/hydra-lab24-ready
FAILED=/tmp/hydra-lab24-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed during: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
 [ -s "$ASSETS/lab24.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
 sleep 1
done
for file in requirements.txt orders.csv workflow.yaml check_output.py prepare.py lab24.py; do [ -s "$ASSETS/$file" ]; done
stage="Installing Hydra and SSH dependency"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing the CSV job and workflow"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Ready: controlplane project and node01 SSH target"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
