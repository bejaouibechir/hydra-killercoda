#!/bin/bash
set -Eeuo pipefail
LOG=/tmp/hydra-lab09-setup.log
DONE=/tmp/hydra-lab09-ready
FAILED=/tmp/hydra-lab09-failed
ASSETS=/root/lab/lab09-resources
rm -f "$DONE" "$FAILED"
exec >"$LOG" 2>&1
trap 'touch "$FAILED"' ERR
mkdir -p /root/lab
for _ in $(seq 1 90); do
  ready=true
  for file in lab09.py sources.yaml destinations.yaml pipeline.yaml transformations.solution.yaml mysql-init.sql postgres-init.sql expected.json start-databases.sh editor.sh; do
    [ -f "$ASSETS/$file" ] || ready=false
  done
  $ready && break
  sleep 1
done
for file in lab09.py sources.yaml destinations.yaml pipeline.yaml transformations.solution.yaml mysql-init.sql postgres-init.sql expected.json start-databases.sh editor.sh; do
  test -f "$ASSETS/$file"
done
# Pull database images while Python installs.
bash "$ASSETS/start-databases.sh" &
database_pid=$!
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/pip install --quiet --disable-pip-version-check "hydra-etl[mysql,postgres]==0.16.0"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
/opt/hydra/bin/python "$ASSETS/lab09.py" prepare
wait "$database_pid"
/opt/hydra/bin/python "$ASSETS/lab09.py" wait
/opt/hydra/bin/python "$ASSETS/lab09.py" check ready
bash "$ASSETS/editor.sh" > /tmp/hydra-lab09-editor.log 2>&1 &
touch "$DONE"
