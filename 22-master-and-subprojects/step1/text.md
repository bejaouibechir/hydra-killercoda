# 1. Explore the three projects

Inspect the master workflow and the child environments. These commands work from any terminal directory:

~~~bash
cat /root/lab/master-and-subprojects/master/workflows/main.yaml
cat /root/lab/master-and-subprojects/crm/environments/dev.yaml /root/lab/master-and-subprojects/billing/environments/prod.yaml
hdrctl workflow validate main --project /root/lab/master-and-subprojects/master
~~~

Find `env: dev`, `env: prod`, `outputs: [last_batch]`, and the master references to each published value. The child environment supplies `label`; the master supplies `batch_date`.

Press **Check** after validation succeeds.
