# 3. Run the same project three times

Select a different environment on each run. Save Hydra's output so you can compare the resolved values.

~~~bash
cd /root/lab/three-environments
hdrctl run . --env dev > reports/dev.txt 2>&1
cat reports/dev.txt
hdrctl run . --env test > reports/test.txt 2>&1
cat reports/test.txt
hdrctl run . --env prod > reports/prod.txt 2>&1
cat reports/prod.txt
~~~

Look for the display_values action in each run. Its four values should change with the environment. Press Check after all three runs.
