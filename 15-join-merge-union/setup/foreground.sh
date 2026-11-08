#!/bin/bash
set -euo pipefail
for attempt in $(seq 1 120); do
 if [ -f /tmp/hydra-lab15-ready ]; then
  cd /root/lab/combine-data
  echo 'Ready. Start with: cat data/orders.csv data/customers.csv'
  exit 0
 fi
 if [ -f /tmp/hydra-lab15-failed ]; then cat /tmp/hydra-lab15-status; exit 1; fi
 sleep 2
done
cat /tmp/hydra-lab15-status 2>/dev/null || true
exit 1
