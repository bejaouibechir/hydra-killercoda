#!/bin/bash
cd /root/lab || exit 1
W=chainproject/workflows/workflow1.yaml
grep -q "jobs/job2" $W && grep -q "depends_on: \[job1\]" $W && hdrctl workflow validate $W >/dev/null 2>&1
