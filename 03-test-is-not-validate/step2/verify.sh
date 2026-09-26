#!/bin/bash
hdrctl test dbjob >/dev/null 2>&1
test $? -eq 0
