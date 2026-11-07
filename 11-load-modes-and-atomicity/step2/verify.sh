#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab11-ready ] || [ -f /tmp/hydra-lab11-failed ]; then
  cat /tmp/hydra-lab11-status 2>/dev/null || true
  echo 'Preparation has not succeeded. Wait for Ready before using Check.'
  exit 1
fi
exec /opt/hydra/bin/python /root/lab/lab11-resources/exercise.py check modes
