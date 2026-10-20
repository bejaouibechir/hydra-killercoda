#!/bin/bash
cd /root/lab || exit 1
out=$(hdrctl list chainproject/jobs 2>/dev/null)
echo "$out" | grep -q job1 && echo "$out" | grep -q job2 && hdrctl validate chainproject/jobs/job2 >/dev/null 2>&1
