#!/bin/bash
set -euo pipefail
[ -f /tmp/hydra-lab10-ready ] || exit 1
/opt/hydra/bin/python /root/lab/lab10-resources/compare.py check warn
/opt/hydra/bin/python /root/lab/lab10-resources/compare.py check fail
