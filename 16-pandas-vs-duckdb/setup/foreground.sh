#!/bin/bash
set -euo pipefail
for attempt in $(seq 1 120); do
 if [ -f /tmp/hydra-lab16-ready ]; then
  cd /root/lab/engine-comparison
  echo 'Ready. Generate the CSV in step 1.'
  exit 0
 fi
 if [ -f /tmp/hydra-lab16-failed ]; then cat /tmp/hydra-lab16-status; exit 1; fi
 sleep 2
done
cat /tmp/hydra-lab16-status 2>/dev/null || true
exit 1
