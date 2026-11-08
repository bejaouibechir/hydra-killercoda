#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab12-ready ] || [ -f /tmp/hydra-lab12-failed ]; then
  cat /tmp/hydra-lab12-status 2>/dev/null || true
  echo 'Preparation has not succeeded. Wait for Ready before using Check.'
  exit 1
fi
exec /opt/hydra/bin/python /root/lab/lab12-resources/check.py second
