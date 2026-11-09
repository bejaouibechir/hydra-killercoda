# Scripts around your jobs

This lesson uses two Killercoda machines: controlplane runs Hydra and a CSV job, while node01 receives one SSH command. The workflow archives its input with Bash, copies the CSV with a job, checks the result with Python, then writes a receipt on node01 through SSH.

The SSH step begins disabled. Its remote command only creates /root/lab24-remote/receipt.txt on node01. Wait for Ready before using Check.
