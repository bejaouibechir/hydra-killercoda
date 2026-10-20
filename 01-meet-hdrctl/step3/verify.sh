#!/bin/bash
cd /root/lab || exit 1
grep -q "Alice" myproject/jobs/job1/data/output.csv
