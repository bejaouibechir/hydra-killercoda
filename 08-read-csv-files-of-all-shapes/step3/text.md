# Fix the encoding

The last file has semicolons and is encoded in Latin-1. Its source already has the correct separator, but no encoding override:

`cat jobs/latin1/sources.yaml`{{exec}}

Observe the failure:

`python3 ../lab08-resources/lab08.py diagnose latin1`{{exec}}

The helper runs `hdrctl run jobs/latin1` and records the real error. Look for **UTF-8**, **decode**, and a nonzero exit code. Some bytes used for the accented names are not valid UTF-8.

In the Editor, update the source connection to:

```yaml
    connection:
      delimiter: ";"
      encoding: latin-1
```

Or apply the correction:

`sed -i '/delimiter:/a\      encoding: latin-1' jobs/latin1/sources.yaml`{{exec}}

Run and inspect the corrected job:

`hdrctl run jobs/latin1`{{exec}}

`python3 ../lab08-resources/lab08.py inspect latin1`{{exec}}

The destination uses UTF-8 independently of the source encoding. The customer names must remain intact.

Compare all three outputs:

`python3 ../lab08-resources/lab08.py compare`{{exec}}

Click **Check**. It checks the saved diagnostic, corrected settings and all output values.
