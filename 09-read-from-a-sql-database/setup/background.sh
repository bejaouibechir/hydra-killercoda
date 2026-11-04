#!/bin/bash
set -Eeuo pipefail
LOG=/tmp/hydra-lab09-setup.log
DONE=/tmp/hydra-lab09-ready
FAILED=/tmp/hydra-lab09-failed
STATUS=/tmp/hydra-lab09-status
ASSETS=/root/lab/lab09-resources
rm -f "$DONE" "$FAILED"
exec >"$LOG" 2>&1
stage="starting setup"
progress() {
  stage="$1"
  printf '%s\n' "$stage" >"$STATUS"
  printf '[%s] %s\n' "$(date -u +%H:%M:%S)" "$stage"
}
failed() {
  local code="$1" line="$2"
  printf 'Setup failed during: %s (line %s, exit %s).\n' "$stage" "$line" "$code" >"$STATUS"
  cat "$STATUS"
  touch "$FAILED"
  exit "$code"
}
trap 'failed "$?" "$LINENO"' ERR
mkdir -p /root/lab
progress "Waiting for the lesson files..."
for _ in $(seq 1 90); do
  ready=true
  for file in lab09.py sources.yaml destinations.yaml pipeline.yaml transformations.solution.yaml mysql-init.sql postgres-init.sql expected.json start-databases.sh editor.sh; do
    [ -f "$ASSETS/$file" ] || ready=false
  done
  $ready && break
  sleep 1
done
for file in lab09.py sources.yaml destinations.yaml pipeline.yaml transformations.solution.yaml mysql-init.sql postgres-init.sql expected.json start-databases.sh editor.sh; do
  if [ ! -f "$ASSETS/$file" ]; then
    echo "Missing lesson file: $ASSETS/$file"
    false
  fi
done
# Pull database images while Python installs.
progress "Downloading MySQL and PostgreSQL images; installing Hydra..."
bash "$ASSETS/start-databases.sh" &
database_pid=$!
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/pip install --quiet --disable-pip-version-check "hydra-etl[mysql,postgres]==0.16.0"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
progress "Hydra is installed. Creating the project files..."
/opt/hydra/bin/python -u "$ASSETS/lab09.py" prepare
progress "Project files are ready. Waiting for the database containers..."
wait "$database_pid"
progress "Database containers started. Waiting for tables and connections..."
/opt/hydra/bin/python -u "$ASSETS/lab09.py" wait
/opt/hydra/bin/python -u "$ASSETS/lab09.py" check ready
bash "$ASSETS/editor.sh" > /tmp/hydra-lab09-editor.log 2>&1 &
progress "Ready: Hydra, project files, MySQL and PostgreSQL."
touch "$DONE"
