#!/bin/bash
set -u
printf 'Preparing Hydra and three projects. Initial downloads may take several minutes.\n'
last=''
for attempt in $(seq 1 900); do
 status=$(cat /tmp/hydra-lab22-status 2>/dev/null || true)
 if [ "$status" != "$last" ]; then printf '%s\n' "$status"; last="$status"; fi
 if [ -f /tmp/hydra-lab22-failed ]; then printf 'Setup failed at the displayed stage.\n'; exit 1; fi
 if [ -f /tmp/hydra-lab22-ready ]; then
  printf 'Ready. The lesson commands work from this terminal directory.\n'
  exit 0
 fi
 if (( attempt % 30 == 0 )); then printf 'Still preparing: %s\n' "$status"; fi
 sleep 1
done
printf 'Setup remains incomplete; do not start or press Check.\n'
exit 1
