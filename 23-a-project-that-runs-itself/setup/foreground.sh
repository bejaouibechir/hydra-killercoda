#!/bin/bash
set -u
printf 'Preparing Hydra and two projects. Initial downloads may take several minutes.\n'
last=''
for attempt in $(seq 1 900); do
 status=$(cat /tmp/hydra-lab23-status 2>/dev/null || true)
 if [ "$status" != "$last" ]; then printf '%s\n' "$status"; last="$status"; fi
 if [ -f /tmp/hydra-lab23-failed ]; then printf 'Setup failed at the displayed stage.\n'; exit 1; fi
 if [ -f /tmp/hydra-lab23-ready ]; then
  printf 'Ready. All lesson commands use absolute project paths.\n'
  exit 0
 fi
 if (( attempt % 30 == 0 )); then printf 'Still preparing: %s\n' "$status"; fi
 sleep 1
done
printf 'Setup remains incomplete; do not start or press Check.\n'
exit 1
