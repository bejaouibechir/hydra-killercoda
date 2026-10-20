# Fix the job

Put the correct source id back:

`sed -i 's/src_csv_typo/src_csv/' brokenproject/jobs/job1/pipeline.yaml`{{exec}}

`cat brokenproject/jobs/job1/pipeline.yaml`{{exec}}

`pipeline.from` now points at `src_csv`, which does exist in `brokenproject/jobs/job1/sources.yaml`.

When you are done, click **Check** to continue.
