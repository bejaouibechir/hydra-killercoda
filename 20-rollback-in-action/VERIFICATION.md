# Verification — LAB lab-03-03

Date: 2026-11-09. Local draft; no commit or push.

The complete four-stage lab passed locally with published `hydra-etl[postgres]==0.19.1` and an isolated PostgreSQL 16 container. The first run loaded both tables, failed at the third action, undid `load_payments` then `load_invoices`, restored the original `(1, 100)` row in each, and removed the journal.

The second run inserted the lab sentinel payment `(999, 999)` in the failing action. Hydra refused to undo a table changed by another writer and retained `.hydra/undo/rollback_demo.json` with both jobs. The repair helper removed only that exact sentinel row. The actual `hdrctl workflow undo rollback_demo` command then undid both jobs in reverse order, restored both original tables, and removed the journal. All four lab checks passed.

The manifest references every asset and lesson step. All Python sources compiled in memory and all shell scripts passed `bash -n`. The two local test containers were removed. A fresh Killercoda startup has not been tested. No Hydra engine file was modified.
