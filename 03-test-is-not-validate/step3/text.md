# Fix the job

Put the correct load mode back:

`sed -i 's/mode: upsret/mode: upsert/' dbproject/jobs/job1/destinations.yaml`{{exec}}

`grep mode dbproject/jobs/job1/destinations.yaml`{{exec}}

When you are done, click **Check** to continue.
