#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab20-ready ] || [ -f /tmp/hydra-lab20-failed ]; then
  cat /tmp/hydra-lab20-status 2>/dev/null || true
  echo 'Wait for Ready before using Check.'
  exit 1
fi
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py check normal
