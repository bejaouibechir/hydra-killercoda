# Verification

The four Check scripts inspect only this lab's project, three CLI captures, the override capture and the learner's answer. They do not probe Killercoda or external services.

Local end-to-end verification passed with the installed Hydra 0.19.1 engine: the dev, test and prod project runs succeeded and showed the expected four values. A dev run with --param min_amount=100 showed 100 instead of 0; the final Check passed.
