# 2. Call a webhook with an undo action

Append a second step. /notify records the call; /cancel records its reversal. Both endpoints are local to the lab.

~~~bash
cat >> /root/lab/reversible-actions/workflows/reversible.yaml <<'YAML'
    - name: call_webhook
      type: action
      action: webhook
      params:
        url: http://127.0.0.1:8790/notify
        method: POST
        body: {event: folder_ready}
      undo:
        action: webhook
        params:
          url: http://127.0.0.1:8790/cancel
          method: POST
          body: {event: folder_cancelled}
      depends_on: [create_folder]
YAML
cat /root/lab/reversible-actions/workflows/reversible.yaml
~~~

The dependency makes execution order explicit. Press Check when both actions and both undo blocks are present.
