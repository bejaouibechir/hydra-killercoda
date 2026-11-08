#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab13-ready ] || [ -f /tmp/hydra-lab13-failed ]; then
  cat /tmp/hydra-lab13-status 2>/dev/null || true
  echo 'Wait for Ready before using Check.'
  exit 1
fi
exec /opt/hydra/bin/python /root/lab/lab13-resources/lab13.py check 2
