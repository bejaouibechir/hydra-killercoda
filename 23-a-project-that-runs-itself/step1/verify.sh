#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab23-ready ] || [ -f /tmp/hydra-lab23-failed ]; then
 cat /tmp/hydra-lab23-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
/opt/hydra/bin/python /root/lab/lab23-resources/lab23.py check config
