#!/bin/bash
set -euo pipefail
if [ ! -f /tmp/hydra-lab16-ready ] || [ -f /tmp/hydra-lab16-failed ]; then
 cat /tmp/hydra-lab16-status 2>/dev/null || true
 echo 'Wait for Ready before using Check.'
 exit 1
fi
test -s /root/lab/engine-comparison/data/sales.csv
/opt/hydra/bin/python -c "import csv; p='/root/lab/engine-comparison/data/sales.csv'; f=open(p,newline=''); n=sum(1 for _ in f)-1; assert n==5000000, n; print('PASS: five million data rows')"
