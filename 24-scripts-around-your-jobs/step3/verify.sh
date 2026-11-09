#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab24-ready ] || [ -f /tmp/hydra-lab24-failed ]; then
 cat /tmp/hydra-lab24-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
/opt/hydra/bin/python /root/lab/lab24-resources/lab24.py check remote
