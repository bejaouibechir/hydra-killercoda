# 3. Introduce a cycle and validate

Add a call from CRM back to the master. The helper only edits this lesson's CRM workflow:

~~~bash
/opt/hydra/bin/python /root/lab/lab22-resources/lab22.py introduce-cycle
hdrctl workflow validate main --project . > reports/cycle-validation.txt 2>&1
cat reports/cycle-validation.txt
~~~

The validation command is expected to fail. Its output must describe the cycle `master -> crm -> master`. Do **not** run the workflow after adding the cycle. Press **Check** when the diagnostic is visible.
