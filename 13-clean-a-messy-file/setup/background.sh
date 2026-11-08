#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab13-resources
LOG=/tmp/hydra-lab13-setup.log
READY=/tmp/hydra-lab13-ready
FAILED=/tmp/hydra-lab13-failed
STATUS=/tmp/hydra-lab13-status
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for resources"
trap 'printf "Setup failed: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
  [ -s "$ASSETS/lab13.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
  sleep 1
done
for file in lab13.py requirements.txt orders.csv sources.yaml destinations.yaml pipeline.yaml stage1.yaml stage2.yaml stage3.yaml stage4.yaml expected1.csv expected2.csv expected3.csv expected4.csv; do
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
stage="Preparing lesson files"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/lab13.py" prepare
stage="Ready: Hydra and lesson files"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
