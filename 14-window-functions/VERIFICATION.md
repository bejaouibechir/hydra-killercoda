# Verification — LAB lab-02-11

Date: 2026-11-08. Status: local draft ready for review.

The published hydra-etl 0.19.1 package ran all four independent jobs against the shared six-row sales CSV. All four Check operations passed. Observed results: order numbers reset for each customer; latest IDs are 6, 5, 4; January running totals are 120, 200, 245 and February totals 50, 70, 105; FR country total is 250 and BE is 100, yielding the expected per-order shares.

The Killercoda manifest lists all 14 assets and four steps. The six setup/check shell scripts passed syntax validation. Startup on a clean Ubuntu/Killercoda backend has not been exercised in this local audit. No engine code changed; no commit or push was made.