#!/bin/bash
set -u
printf 'Preparing the MongoDB drift lab. This draft is blocked on Hydra 0.16.0.\n'
last=""
for attempt in $(seq 1 600); do
  status=$(cat /tmp/hydra-lab10-status 2>/dev/null || true)
  if [ "$status" != "$last" ]; then
    printf '%s\n' "$status"
    last="$status"
  fi
  if [ -f /tmp/hydra-lab10-failed ]; then
    tail -n 60 /tmp/hydra-lab10-setup.log
    printf '\nSetup stopped; do not continue the exercises.\n'
    exit 1
  fi
  if [ -f /tmp/hydra-lab10-ready ]; then
    cd /root/lab/mongodb-drift || exit 1
    printf 'Ready. Every lesson helper uses /opt/hydra/bin/python explicitly.\n'
    exit 0
  fi
  if (( attempt % 30 == 0 )); then
    printf 'Still preparing: %s\n' "$status"
  fi
  sleep 1
done
printf 'Setup timed out. Inspect /tmp/hydra-lab10-setup.log before continuing.\n'
exit 1
