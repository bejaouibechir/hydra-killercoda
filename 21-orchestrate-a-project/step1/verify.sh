#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab21-ready ] || [ -f /tmp/hydra-lab21-failed ]; then
 cat /tmp/hydra-lab21-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
/opt/hydra/bin/python /root/lab/lab21-resources/lab21.py check thread
