# 2. Run the master and read its outputs

~~~bash
/opt/hydra/bin/python /root/lab/lab22-resources/lab22.py run
cat /root/lab/master-and-subprojects/master/published.json
~~~

The result should contain `CRM-DEV-2026-11-09` and `BILLING-PROD-2026-11-09`. They come from the child environments, a parameter passed by the master, and each child's `set_param` action. The master reads them through `project:crm_sync.param.last_batch` and `project:billing_sync.param.last_batch`.

Press **Check** once you see both values.
