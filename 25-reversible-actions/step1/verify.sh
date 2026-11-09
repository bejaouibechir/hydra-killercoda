#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab25-ready ] || [ -f /tmp/hydra-lab25-failed ]; then
  cat /tmp/hydra-lab25-status 2>/dev/null || true
  echo 'Wait for Ready before using Check.'
  exit 1
fi
/opt/hydra/bin/python /root/lab/lab25-resources/lab25.py stage1
