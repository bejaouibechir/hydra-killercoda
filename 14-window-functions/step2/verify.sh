#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab14-ready ] || [ -f /tmp/hydra-lab14-failed ]; then
 cat /tmp/hydra-lab14-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
exec /opt/hydra/bin/python /root/lab/lab14-resources/lab14.py check 2
