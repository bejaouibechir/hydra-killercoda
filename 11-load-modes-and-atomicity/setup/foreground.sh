#!/bin/bash
set -u
printf 'Preparing Hydra, CSV files, and PostgreSQL. Initial downloads can take several minutes.\n'
last=""
for attempt in $(seq 1 600); do
  status=$(cat /tmp/hydra-lab11-status 2>/dev/null || true)
  if [ "$status" != "$last" ]; then
    printf '%s\n' "$status"
    last="$status"
  fi
  if [ -f /tmp/hydra-lab11-failed ]; then
    tail -n 60 /tmp/hydra-lab11-setup.log
    printf '\nSetup failed. Do not start the exercises yet.\n'
    exit 1
  fi
  if [ -f /tmp/hydra-lab11-ready ]; then
    cd /root/lab/load-modes || exit 1
    printf 'Ready. Start step 1. All Python commands use the installed Hydra interpreter.\n'
    exit 0
  fi
  if (( attempt % 30 == 0 )); then
    printf 'Still preparing: %s\n' "$status"
  fi
  sleep 1
done
printf 'Setup timed out. Inspect /tmp/hydra-lab11-setup.log before continuing.\n'
exit 1
