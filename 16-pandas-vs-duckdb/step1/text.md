# Generate the shared CSV

The generator streams five million rows to disk. Each of FR, BE, DE and ES appears 1,250,000 times with amount 10, 20, 30 and 40 respectively.

```bash
cd /root/lab/engine-comparison
/opt/hydra/bin/python /root/lab/lab16-resources/generate.py
```

Press **Check** when generation finishes.
