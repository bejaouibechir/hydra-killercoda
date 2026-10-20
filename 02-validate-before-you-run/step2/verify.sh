#!/bin/bash
cd /root/lab || exit 1
if hdrctl validate brokenproject/jobs/job1 >/dev/null 2>&1; then
  exit 1
else
  exit 0
fi
