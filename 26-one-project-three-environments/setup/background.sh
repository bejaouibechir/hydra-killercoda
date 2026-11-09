#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab26-resources
LOG=/tmp/hydra-lab26-setup.log
STATUS=/tmp/hydra-lab26-status
READY=/tmp/hydra-lab26-ready
FAILED=/tmp/hydra-lab26-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed during: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
  [ -s "$ASSETS/lab26.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
  sleep 1
done
for file in requirements.txt prepare.py lab26.py workflow.yaml thread.yaml; do
  [ -s "$ASSETS/$file" ]
done
stage="Installing Hydra"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing one project"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Ready: Hydra and the starter project"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
