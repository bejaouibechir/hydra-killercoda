#!/bin/bash
cd /root/lab || exit 1
hdrctl validate brokenproject/jobs/job1 >/dev/null 2>&1
test $? -eq 0
