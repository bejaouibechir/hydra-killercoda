#!/bin/bash
cd /root/lab || exit 1
hdrctl test dbproject/jobs/job1 >/dev/null 2>&1
