#!/bin/bash
cd /root/lab || exit 1
hdrctl list myproject/jobs 2>/dev/null | grep -q job1
