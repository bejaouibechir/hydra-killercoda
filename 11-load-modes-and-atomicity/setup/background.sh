#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab11-resources
LOG=/tmp/hydra-lab11-setup.log
STATUS=/tmp/hydra-lab11-status
READY=/tmp/hydra-lab11-ready
FAILED=/tmp/hydra-lab11-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Starting"
progress() {
  stage="$1"
  printf '%s\n' "$stage" >"$STATUS"
  printf '[%s] %s\n' "$(date -Is)" "$stage"
}
failed() {
  code="$?"
  printf 'Setup failed during: %s. See %s\n' "$stage" "$LOG" >"$STATUS"
  touch "$FAILED"
  exit "$code"
}
trap failed ERR
progress "Waiting for lesson resources"
files=(common.py lab11.py exercise.py products.csv failure.csv sources.template.yaml
       destinations.template.yaml pipeline.yaml seed.sql docker-compose.yml requirements.txt)
for attempt in $(seq 1 90); do
  missing=0
  for file in "${files[@]}"; do
    [ -s "$ASSETS/$file" ] || missing=1
  done
  [ "$missing" -eq 0 ] && break
  sleep 1
done
for file in "${files[@]}"; do
  [ -s "$ASSETS/$file" ] || { echo "Missing asset: $file"; false; }
done
progress "Installing Hydra and its PostgreSQL driver"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
progress "Creating the five jobs and both CSV files"
/opt/hydra/bin/python "$ASSETS/lab11.py" prepare
progress "Downloading and starting PostgreSQL"
docker compose -f "$ASSETS/docker-compose.yml" up -d --wait --wait-timeout 180
progress "Waiting for database access"
/opt/hydra/bin/python "$ASSETS/lab11.py" wait
progress "Seeding the five target tables"
/opt/hydra/bin/python "$ASSETS/lab11.py" seed
progress "Ready: Hydra, lesson files, and PostgreSQL"
touch "$READY"
