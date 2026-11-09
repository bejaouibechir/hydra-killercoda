#!/bin/bash
set -u
printf 'Preparing the project and PostgreSQL. Initial downloads may take several minutes.\n'
last=''
for attempt in $(seq 1 900); do
 status=$(cat /tmp/hydra-lab21-status 2>/dev/null || true)
 if [ "$status" != "$last" ]; then printf '%s\n' "$status"; last="$status"; fi
 if [ -f /tmp/hydra-lab21-failed ]; then printf 'Setup failed at the displayed stage. Stop and report it.\n'; exit 1; fi
 if [ -f /tmp/hydra-lab21-ready ]; then
  cd /root/lab/orchestrate-project || exit 1
  printf 'Ready. Start with: cat workflows/thread.yaml\n'
  exit 0
 fi
 if (( attempt % 30 == 0 )); then printf 'Still preparing: %s\n' "$status"; fi
 sleep 1
done
printf 'Setup remains incomplete; do not start or press Check.\n'
exit 1
