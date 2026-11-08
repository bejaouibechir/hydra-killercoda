# Verification — LAB lab-02-12

Date: 2026-11-08. Status: local draft ready for review.

The published hydra-etl 0.19.1 package, Python 3.13 pandas, and in-memory SQLite processed the same seven-row CSV. SQL, pandas and Hydra each produced exactly `BE,20.0` and `FR,45.0`. The data includes mixed case, surrounding spaces, one cancelled order and two empty amounts. The latest paid C200 and C400 orders have empty amounts, contributing zero revenue; the earlier C100 amount is excluded by the latest-order rule.

The deliberate `amount_typo` experiment produced SQLite `OperationalError: no such column`, pandas `KeyError`, and a Hydra error naming the step, unknown column and available columns. All four Check stages passed locally. The manifest lists 12 assets and four steps; six shell scripts and all Python files passed syntax checks.

This test did not start a clean Ubuntu/Killercoda backend. No Hydra engine files were changed; no commit or push was made.