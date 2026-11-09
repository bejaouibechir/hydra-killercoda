#!/bin/bash
set -u
printf 'Preparing Hydra and the two lesson tables. The first download can take several minutes.\n'
last=''
for attempt in $(seq 1 900); do
  status=$(cat /tmp/hydra-lab20-status 2>/dev/null || true)
  if [ "$status" != "$last" ]; then printf '%s\n' "$status"; last="$status"; fi
  if [ -f /tmp/hydra-lab20-failed ]; then
    printf 'Setup failed at the displayed stage. Stop here and report it to the maintainer.\n'
    exit 1
  fi
  if [ -f /tmp/hydra-lab20-ready ]; then
    cd /root/lab/rollback-in-action || exit 1
    printf 'Ready. Start with: cat workflows/rollback_demo.yaml\n'
    exit 0
  fi
  if (( attempt % 30 == 0 )); then printf 'Still preparing: %s\n' "$status"; fi
  sleep 1
done
printf 'Setup is still incomplete. Do not start the lesson or press Check.\n'
exit 1
