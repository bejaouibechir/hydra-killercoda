#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab27-ready ] || [ -f /tmp/hydra-lab27-failed ]; then
  cat /tmp/hydra-lab27-status 2>/dev/null || true
  echo 'Wait for Ready before using Check.'
  exit 1
fi
/opt/hydra/bin/python /root/lab/lab27-resources/lab27.py check env
