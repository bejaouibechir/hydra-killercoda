# 1. Explore the three projects

The terminal opens in the master project. Inspect its project calls and the child environments:

~~~bash
cat workflows/main.yaml
cat ../crm/environments/dev.yaml ../billing/environments/prod.yaml
hdrctl workflow validate main --project .
~~~

Find `env: dev`, `env: prod`, `outputs: [last_batch]`, and the master references to each published value. The child environment supplies `label`; the master supplies `batch_date`.

Press **Check** after validation succeeds.
