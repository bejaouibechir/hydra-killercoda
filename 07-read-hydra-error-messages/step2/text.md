# Fix an unknown key

Load the next exercise. This replaces only the lab workflow with a new faulty copy:

`python3 ../lab07-resources/lab07.py prepare unknown-key`{{exec}}

`cat workflows/errors.yaml`{{exec}}

This time the action name is correct. Diagnose the new problem:

`python3 ../lab07-resources/lab07.py diagnose unknown-key`{{exec}}

Look for:

```text
Step 'notify': unknown key 'depend_on' ... did you mean 'depends_on'?
Exit code: 1
```

`depends_on` declares execution dependencies. Hydra rejects this misspelling instead of silently ignoring the intended order.

Correct the key, keeping its value as a list:

`sed -i 's/depend_on:/depends_on:/' workflows/errors.yaml`{{exec}}

The corrected line is:

```yaml
depends_on: [start]
```

`hdrctl run . --dry-run`{{exec}}

Click **Check** once the dry-run succeeds.
