# Verification

- Full local run passed with the installed Hydra 0.19.1 engine and a receiver on 127.0.0.1.
- The intentional final failure produced rollback.status = done and undo order call_webhook, create_folder.
- The event log contained folder_created, webhook_called, webhook_undone, folder_removed in that order.
- Stage 1 checks the folder action and undo definition.
- Stage 2 checks webhook URL, undo URL, POST and dependency.
- Stage 3 checks failure, completed rollback, exact undo order, event order, removed folder and no unfinished journal.
- The final failure is intentional and is not treated as a helper error.
