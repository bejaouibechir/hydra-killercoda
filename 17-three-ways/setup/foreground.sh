#!/bin/bash
set -euo pipefail
for attempt in $(seq 1 120); do
 if [ -f /tmp/hydra-lab17-ready ]; then
  cd /root/lab/three-ways
  echo 'Ready. Start with: cat data/orders.csv'
  exit 0
 fi
 if [ -f /tmp/hydra-lab17-failed ]; then cat /tmp/hydra-lab17-status; exit 1; fi
 sleep 2
done
cat /tmp/hydra-lab17-status 2>/dev/null || true
exit 1
