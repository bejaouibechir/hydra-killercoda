#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab27-resources
LOG=/tmp/hydra-lab27-setup.log
STATUS=/tmp/hydra-lab27-status
READY=/tmp/hydra-lab27-ready
FAILED=/tmp/hydra-lab27-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed during: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
  [ -s "$ASSETS/lab27.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
  sleep 1
done
for file in requirements.txt prepare.py start-db.sh lab27.py sources.yaml destinations.yaml pipeline.yaml; do
  [ -s "$ASSETS/$file" ]
done
stage="Installing Hydra and Git"
printf '%s\n' "$stage" >"$STATUS"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv git
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
stage="Preparing local project and random credential"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
git -C /root/lab/secrets-without-leaks init -q
stage="Starting and seeding the local PostgreSQL container"
printf '%s\n' "$stage" >"$STATUS"
bash "$ASSETS/start-db.sh"
stage="Ready: Hydra, Git and two database rows"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
