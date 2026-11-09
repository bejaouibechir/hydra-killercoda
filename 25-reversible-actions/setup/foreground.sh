#!/bin/bash
set -u
printf 'Preparing Hydra and the local webhook receiver. The first download can take several minutes.\n'
last=''
for attempt in $(seq 1 900); do
  status=$(cat /tmp/hydra-lab25-status 2>/dev/null || true)
  if [ "$status" != "$last" ]; then printf '%s\n' "$status"; last="$status"; fi
  if [ -f /tmp/hydra-lab25-failed ]; then
    printf 'Setup failed at the displayed stage. Stop and report it to the maintainer.\n'
    exit 1
  fi
  if [ -f /tmp/hydra-lab25-ready ]; then
    cd /root/lab/reversible-actions || exit 1
    printf 'Ready. Start with: cat workflows/reversible.yaml\n'
    exit 0
  fi
  if (( attempt % 30 == 0 )); then printf 'Still preparing: %s\n' "$status"; fi
  sleep 1
done
printf 'Setup is incomplete. Do not start the lesson or press Check.\n'
exit 1
