# MongoDB documents and schema drift

**Maintainer draft — blocked on Hydra 0.16.0. Do not publish this scenario yet.**

The compatibility check currently stops setup because the engine does not apply the
three drift policies during MongoDB extraction. The exercises below describe the
intended comparison, pending an engine fix and a live acceptance test.

You will read the same collection with three independent Hydra jobs. Its first 100
documents contain `_id`, `customer`, and `amount`. Two later documents introduce
`sales_channel`: one contains `web`, the other `store`.

The schema is inferred from the first 100 documents. The additional field is outside
that sample, so accepting heterogeneous documents during inference is not confused
with handling drift during extraction.

Allow setup to finish before continuing. A **STOPPED** message is a blocker, not a
successful installation.
