#!/bin/bash
set -euo pipefail
for attempt in $(seq 1 120); do
 if [ -f /tmp/hydra-lab19-ready ]; then
  cd /root/lab/when-things-go-wrong
  echo 'Ready. Start with: cat workflow.yaml'
  exit 0
 fi
 if [ -f /tmp/hydra-lab19-failed ]; then cat /tmp/hydra-lab19-status; exit 1; fi
 sleep 2
done
cat /tmp/hydra-lab19-status 2>/dev/null || true
exit 1
