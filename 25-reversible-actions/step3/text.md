# 3. Fail and observe reverse order

Append a final step that deliberately raises an error. undo: none is appropriate because the failed script leaves no side effect to reverse.

~~~bash
cat >> /root/lab/reversible-actions/workflows/reversible.yaml <<'YAML'
    - name: fail_last
      type: action
      action: python
      params:
        file_path: scripts/fail.py
      undo: none
      depends_on: [call_webhook]
YAML
/opt/hydra/bin/python /root/lab/lab25-resources/lab25.py run
cat /root/lab/reversible-actions/reports/events.log
~~~

The workflow should report a failure followed by a completed rollback. The journal should show:

~~~text
folder_created
webhook_called
webhook_undone
folder_removed
~~~

The reverse sequence is undo call_webhook, then undo create_folder. The work/output folder must be gone. Press Check after the run.
