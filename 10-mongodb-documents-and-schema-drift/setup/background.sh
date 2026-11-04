#!/bin/bash
set -Eeuo pipefail
ASSETS=/root/lab/lab10-resources
LOG=/tmp/hydra-lab10-setup.log
STATUS=/tmp/hydra-lab10-status
READY=/tmp/hydra-lab10-ready
FAILED=/tmp/hydra-lab10-failed
rm -f "$READY" "$FAILED"
exec >"$LOG" 2>&1
stage="Waiting for resources"
progress() {
  stage="$1"
  printf '%s\n' "$stage" >"$STATUS"
  printf '[%s] %s\n' "$(date -Is)" "$stage"
}
failed() {
  code="$?"
  printf 'STOPPED: %s. See %s\n' "$stage" "$LOG" >"$STATUS"
  touch "$FAILED"
  exit "$code"
}
trap failed ERR
progress "Waiting for lesson resources"
files=(lab10.py compare.py probe.py documents.json sources.template.yaml
       destinations.yaml pipeline.yaml docker-compose.yml requirements.txt)
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
progress "Installing the isolated Hydra environment"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv
python3 -m venv /opt/hydra
/opt/hydra/bin/python -m pip install --disable-pip-version-check -q -r "$ASSETS/requirements.txt"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
progress "Preparing the three jobs"
/opt/hydra/bin/python "$ASSETS/lab10.py" prepare
progress "Checking Hydra drift support (known blocker in 0.16.0)"
/opt/hydra/bin/python "$ASSETS/probe.py"
# Do not download or start MongoDB when the required engine behavior is absent.
progress "Starting the dedicated MongoDB container"
docker compose -f "$ASSETS/docker-compose.yml" up -d --wait --wait-timeout 180
progress "Seeding and checking the inference sample"
/opt/hydra/bin/python "$ASSETS/lab10.py" seed
progress "Ready: MongoDB documents and schema drift"
touch "$READY"
