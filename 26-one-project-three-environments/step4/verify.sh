#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab26-ready ] || [ -f /tmp/hydra-lab26-failed ]; then
  cat /tmp/hydra-lab26-status 2>/dev/null || true
  echo 'Wait for Ready before using Check.'
  exit 1
fi
/opt/hydra/bin/python /root/lab/lab26-resources/lab26.py override
