# Missing version: accepted, not an error

Prepare a workflow with **no top-level version field**:

`python3 ../lab07-resources/lab07.py prepare no-version`{{exec}}

`head -n 8 workflows/errors.yaml`{{exec}}

The file starts with `workflow:`. Predict what will happen, then check:

`python3 ../lab07-resources/lab07.py diagnose no-version`{{exec}}

The exit code is **0**. Hydra assumes the current DSL version when the field is absent. There is no missing-version error to fix.

In authored manifests, include the format version explicitly:

```yaml
version: "1.0"
```

This is the **DSL format version**, not the installed Hydra product version. In this exercise, leave it absent so **Check** can confirm the behaviour you just observed.

The lesson: distinguish a recommendation for clear files from a field the engine actually requires.

Click **Check**. You have diagnosed three real errors and one accepted omission, without executing any action.
