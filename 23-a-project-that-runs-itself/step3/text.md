# 3. Call the actual HTTP webhook

Stop `hdrctl watch` in its tab with **Ctrl+C**. The next command disables clock and file polling for the HTTP stage, while retaining their run histories:

~~~bash
/opt/hydra/bin/python /root/lab/lab23-resources/lab23.py switch-webhook
~~~

Start Hydra's local API in the first tab. Wait until it displays its API address and leave it running:

~~~bash
hdrctl serve --no-studio --host 127.0.0.1 --port 5683 --workspace /root/lab/project-triggers
~~~

In the second tab, call the webhook. The token was generated during setup and is read without printing it:

~~~bash
curl -sS -i -X POST 'http://127.0.0.1:5683/api/projects/lab23-producer/triggers/http_hook/webhook' -H "X-Hydra-Token: $(/opt/hydra/bin/python /root/lab/lab23-resources/lab23.py token)"
hdrctl trigger history http_hook --project /root/lab/project-triggers/producer
~~~

The response should be **202 Accepted** and history should show `http_hook` with origin `webhook`. `watch` does not host HTTP endpoints; `serve` does. Press **Check** after the webhook run succeeds.
