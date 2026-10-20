#!/bin/bash
cd /root/lab || exit 1
F=chainproject/jobs/job2/data/output.csv
test -f $F && grep -q "Bob" $F && ! grep -q "Alice" $F
