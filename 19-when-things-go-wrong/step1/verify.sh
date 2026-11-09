#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab19-ready ] || [ -f /tmp/hydra-lab19-failed ]; then
 cat /tmp/hydra-lab19-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
/opt/hydra/bin/python /root/lab/lab19-resources/lab19.py check fail
