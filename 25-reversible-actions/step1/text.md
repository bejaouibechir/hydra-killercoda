# 1. Create a folder with an undo action

The starter workflow has rollback: true and no steps. The provided scripts create and remove work/output, recording both events in reports/events.log.

Replace the starter workflow with this first step:

~~~bash
cat > /root/lab/reversible-actions/workflows/reversible.yaml <<'YAML'
version: '1.0'
workflow:
  name: reversible
  rollback: true
  trigger:
    type: manual
  steps:
    - name: create_folder
      type: action
      action: python
      params:
        file_path: scripts/create_folder.py
      undo:
        action: python
        params:
          file_path: scripts/remove_folder.py
YAML
cat /root/lab/reversible-actions/workflows/reversible.yaml
~~~

The undo block belongs to create_folder. Press Check after saving the file.
