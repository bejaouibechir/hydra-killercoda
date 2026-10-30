# Done

You used the diagnostic to locate the step, identify the invalid field and apply a precise correction.

| Case | Initial result | What you learned |
|---|---|---|
| `action: webhok` | Exit 1 | Action names are validated; Hydra suggests `webhook`. |
| `depend_on` | Exit 1 | Workflow keys are validated; the correct key is `depends_on`. |
| Missing `action` on an action step | Exit 1 | An action step must name its action. |
| Missing `version` | Exit 0 | Hydra assumes the current DSL format. |

Your diagnostic logs are in `/root/lab/lab07-evidence/`. A corrected reference workflow is in `/root/lab/lab07-resources/solution.yaml`.

**Dry-run is not a connection test.** The exercise endpoint is deliberately a placeholder; do not execute this workflow without replacing it.

Keep this habit: **read the error, fix one cause, validate again.**

- Documentation: [hydraetl.com](https://hydraetl.com/)
- Hydra source: [github.com/bejaouibechir/Hydra](https://github.com/bejaouibechir/Hydra)
