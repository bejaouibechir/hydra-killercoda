# Verification — LAB lab-02-08

Date: 2026-11-08. Status: local draft ready for review.

All three independent jobs ran with the published hydra-etl 0.19.1 package. Their Check operations accepted the actual CSV output. Join produced four orders with Alice on IDs 1 and 3, Bob on ID 2, and a missing customer name on ID 4 (written as `nan` by this CSV output). Merge preserved IDs 1, 3, 4, replaced ID 2 with amount 90/status paid, and added ID 5. Union with `distinct: true` kept the four original rows plus ID 5 and removed the repeated ID 1.

The lesson conclusion explains each output row. The manifest declares 17 assets and three steps. Five setup/check shell scripts passed syntax validation. Startup on a clean Ubuntu/Killercoda backend was not tested here. No Hydra engine files were changed; no commit or push was made.