#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab12-resources
LOG=/tmp/hydra-lab12-setup.log
STATUS=/tmp/hydra-lab12-status
READY=/tmp/hydra-lab12-ready
FAILED=/tmp/hydra-lab12-failed
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
files=(common.py lab12.py check.py products.csv products.updated.csv expected.json seed.sql start-database.sh wait-ready.sh requirements.txt)
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
progress "Installing Hydra and its MySQL driver"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
progress "Preparing data, secrets, and the empty job directory"
/opt/hydra/bin/python "$ASSETS/lab12.py" prepare
progress "Downloading and starting MySQL"
bash "$ASSETS/start-database.sh"
progress "Waiting for database access"
/opt/hydra/bin/python "$ASSETS/lab12.py" wait
progress "Seeding the products table"
/opt/hydra/bin/python "$ASSETS/lab12.py" seed
progress "Verifying database tables and installed Hydra"
/opt/hydra/bin/hdrctl --version
/opt/hydra/bin/python "$ASSETS/lab12.py" ready
progress "Ready: Hydra, lesson files, and MySQL"
touch "$READY"
