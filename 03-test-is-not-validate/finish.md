# Done

You now know:

- `hdrctl test` checks your YAML and *reports* on connections and secrets — it never opens either;
- `hdrctl validate` is stricter about YAML shape, but never touches secrets or connections at all;
- `hdrctl run` is the only command that resolves `${ENV:...}` and the only one that ever opens a real connection.

Neither `test` nor `validate` is lying to you — read closely and they say so themselves. But "all tests pass" and "DSL valid" are easy headlines to trust past the fine print.

**Next**

- Install it on your machine: `pip install hydra-etl`
- Docs and examples: [hydraetl.com](https://hydraetl.com/?utm_source=killercoda&utm_medium=lab&utm_campaign=test-is-not-validate)
- Source (AGPL-3.0): [github.com/bejaouibechir/Hydra](https://github.com/bejaouibechir/Hydra)

Hydra ETL is a beta, built by one maintainer. If something in this lab felt wrong or unclear, [open an issue](https://github.com/bejaouibechir/Hydra/issues) — that's the most useful thing you can do.
