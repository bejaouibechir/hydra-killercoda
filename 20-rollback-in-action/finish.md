# What you observed

The first failure restored both PostgreSQL tables automatically. The second failure left an undo journal because the payment table had changed after Hydra wrote it. Once the lesson's outside row was removed, `hdrctl workflow undo rollback_demo` resumed the journal and restored the tables in reverse order.

An unfinished journal prevents another workflow run. Hydra does not silently discard changes made by another writer.
