#!/bin/bash
out=$(hdrctl list 2>/dev/null)
echo "$out" | grep -q "solojob" && ! echo "$out" | grep -q "mypipeline"
