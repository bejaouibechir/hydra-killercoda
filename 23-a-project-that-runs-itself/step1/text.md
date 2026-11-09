# 1. Inspect and start the watcher

Inspect the project trigger rules and validate them:

~~~bash
cat /root/lab/project-triggers/producer/triggers.yaml
cat /root/lab/project-triggers/consumer/triggers.yaml
hdrctl trigger validate --project /root/lab/project-triggers/producer
hdrctl trigger validate --project /root/lab/project-triggers/consumer
~~~

Open a **second terminal tab**. In the first tab, keep this command running:

~~~bash
hdrctl watch /root/lab/project-triggers/producer /root/lab/project-triggers/consumer
~~~

It lists the active clock, file and `after_project` rules. It notes that the webhook requires `hdrctl serve`. Press **Check** after both validation commands succeed, and leave the watcher running for the next step.
