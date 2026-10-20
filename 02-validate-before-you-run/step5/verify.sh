#!/bin/bash
cd /root/lab || exit 1
test -f brokenproject/jobs/job1/data/output.csv
