#!/bin/bash
set -Eeuo pipefail
LOG=/tmp/hydra-lab08-setup.log
DONE=/tmp/hydra-lab08-ready
FAILED=/tmp/hydra-lab08-failed
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
for _ in $(seq 1 90); do
  [ -f /root/lab/lab08-resources/lab08.py ] &&
  [ -f /root/lab/lab08-resources/orders-comma.csv ] &&
  [ -f /root/lab/lab08-resources/orders-semicolon.csv ] &&
  [ -f /root/lab/lab08-resources/orders-latin1.csv ] &&
  [ -f /root/lab/lab08-resources/editor.sh ] && break
  sleep 1
done
/opt/hydra/bin/python /root/lab/lab08-resources/lab08.py prepare
bash /root/lab/lab08-resources/editor.sh > /tmp/hydra-lab08-editor.log 2>&1 &
touch "$DONE"
