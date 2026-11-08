#!/bin/bash
set -u
printf 'Preparing Hydra, CSV files, and MySQL. Initial downloads can take several minutes.\n'
last=""
for attempt in $(seq 1 900); do
  status=$(cat /tmp/hydra-lab12-status 2>/dev/null || true)
  if [ "$status" != "$last" ]; then
    printf '%s\n' "$status"
    last="$status"
  fi
  if [ -f /tmp/hydra-lab12-failed ]; then
    :
    printf '\nSetup failed. The lab is not ready; stop here and report the displayed stage to the maintainer.\n'
    exit 1
  fi
  if [ -f /tmp/hydra-lab12-ready ]; then
    cd /root/lab/build-job || exit 1
    printf 'Ready. Start step 1. All Python commands use the installed Hydra interpreter.\n'
    exit 0
  fi
  if (( attempt % 30 == 0 )); then
    printf 'Still preparing: %s\n' "$status"
  fi
  sleep 1
done
printf 'Setup is still incomplete. Do not run the exercises or Check until preparation succeeds.\n'
exit 1
