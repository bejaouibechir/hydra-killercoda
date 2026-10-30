#!/bin/bash
set -Eeuo pipefail
LOG=/tmp/hydra-lab07-setup.log
DONE=/tmp/hydra-lab07-ready
FAILED=/tmp/hydra-lab07-failed
rm -f "$DONE" "$FAILED"
exec >"$LOG" 2>&1
trap 'touch "$FAILED"' ERR
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/pip install --quiet --disable-pip-version-check "hydra-etl==0.16.0"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
mkdir -p /root/lab
# Assets can arrive after the background script starts.
for _ in $(seq 1 90); do
  [ -f /root/lab/lab07-resources/lab07.py ] &&
  [ -f /root/lab/lab07-resources/solution.yaml ] &&
  [ -f /root/lab/lab07-resources/unknown-action.yaml ] &&
  [ -f /root/lab/lab07-resources/unknown-key.yaml ] &&
  [ -f /root/lab/lab07-resources/missing-action.yaml ] &&
  [ -f /root/lab/lab07-resources/no-version.yaml ] && break
  sleep 1
done
/opt/hydra/bin/python /root/lab/lab07-resources/lab07.py prepare unknown-action
# The editor extension is optional and must not delay readiness.
bash /root/lab/lab07-resources/editor.sh > /tmp/hydra-lab07-editor.log 2>&1 &
touch "$DONE"
