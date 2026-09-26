#!/bin/bash
cd /root/lab || exit 1
hdrctl test dbjob >/dev/null 2>&1
test $? -eq 0
