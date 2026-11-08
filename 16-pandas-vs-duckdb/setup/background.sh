#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab16-resources
LOG=/tmp/hydra-lab16-setup.log
READY=/tmp/hydra-lab16-ready
FAILED=/tmp/hydra-lab16-failed
STATUS=/tmp/hydra-lab16-status
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
 [ -s "$ASSETS/benchmark.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
 sleep 1
done
for file in benchmark.py generate.py prepare.py requirements.txt pandas.sources.yaml pandas.pipeline.yaml pandas.transformations.yaml pandas.destinations.yaml auto.sources.yaml auto.pipeline.yaml auto.transformations.yaml auto.destinations.yaml; do
 [ -s "$ASSETS/$file" ]
done
stage="Installing Hydra, DuckDB and memory monitor"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing both jobs"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Ready: generate the CSV and run both jobs"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
