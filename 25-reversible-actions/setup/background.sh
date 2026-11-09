#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab25-resources
LOG=/tmp/hydra-lab25-setup.log
STATUS=/tmp/hydra-lab25-status
READY=/tmp/hydra-lab25-ready
FAILED=/tmp/hydra-lab25-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for lesson resources"
trap 'printf "Setup failed during: %s\n" "$stage" >"$STATUS"; touch "$FAILED"' ERR
for attempt in $(seq 1 90); do
  [ -s "$ASSETS/lab25.py" ] && [ -s "$ASSETS/requirements.txt" ] && break
  sleep 1
done
for file in requirements.txt prepare.py lab25.py webhook_server.py create_folder.py remove_folder.py fail.py; do
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
stage="Preparing learner project"
printf '%s\n' "$stage" >"$STATUS"
/opt/hydra/bin/python "$ASSETS/prepare.py"
stage="Starting local webhook receiver"
printf '%s\n' "$stage" >"$STATUS"
nohup /opt/hydra/bin/python "$ASSETS/webhook_server.py" >/tmp/hydra-lab25-webhook.log 2>&1 </dev/null &
for attempt in $(seq 1 30); do
  [ -f /root/lab/reversible-actions/reports/webhook-ready ] && break
  sleep 1
done
[ -f /root/lab/reversible-actions/reports/webhook-ready ]
stage="Ready: Hydra, project and local webhook"
printf '%s\n' "$stage" >"$STATUS"
touch "$READY"
