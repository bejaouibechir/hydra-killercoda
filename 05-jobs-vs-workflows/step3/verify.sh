#!/bin/bash
out=$(hdrctl workflow list . 2>/dev/null)
echo "$out" | grep -q "mypipeline" && echo "$out" | grep -q "3 steps"
