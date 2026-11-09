"""Inspect this lab's workflow and verify the rollback evidence."""
from pathlib import Path
import json
import os
import sys

from hydra_etl.workflow.parser import load_workflow
from hydra_etl.workflow.runner import WorkflowRunner

ROOT = Path(os.environ.get("HYDRA_LAB25_ROOT", "/root/lab/reversible-actions"))
PATH = ROOT / "workflows" / "reversible.yaml"
URL = "http://127.0.0.1:" + os.environ.get("LAB25_PORT", "8790")
EXPECTED = ["folder_created", "webhook_called", "webhook_undone", "folder_removed"]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def inspect(stage):
    wf = load_workflow(PATH)
    require(wf.rollback, "Set rollback: true on the workflow")
    steps = {s.name: s for s in wf.steps}
    names = ["create_folder", "call_webhook", "fail_last"][:stage]
    require(set(steps) == set(names), "This stage needs exactly: " + ", ".join(names))
    first = steps["create_folder"]
    require(first.type == "action" and first.action == "python", "create_folder must be a Python action")
    require(first.params.get("file_path") == "scripts/create_folder.py", "Use the provided create_folder.py")
    require(first.undo and first.undo != "none" and first.undo.action == "python", "Give create_folder a Python undo")
    require(first.undo.params.get("file_path") == "scripts/remove_folder.py", "Undo must use remove_folder.py")
    if stage >= 2:
        second = steps["call_webhook"]
        require(second.type == "action" and second.action == "webhook", "call_webhook must be a webhook action")
        require(second.depends_on == ["create_folder"], "call_webhook must depend on create_folder")
        require(second.params.get("url") == URL + "/notify", "Use the local /notify endpoint")
        require(second.params.get("method", "POST").upper() == "POST", "Use POST")
        require(second.undo and second.undo != "none" and second.undo.action == "webhook", "Give call_webhook a webhook undo")
        require(second.undo.params.get("url") == URL + "/cancel", "Undo must call /cancel")
        require(second.undo.params.get("method", "POST").upper() == "POST", "Undo must use POST")
    if stage >= 3:
        last = steps["fail_last"]
        require(last.type == "action" and last.action == "python", "fail_last must be a Python action")
        require(last.params.get("file_path") == "scripts/fail.py", "Use the intentional failure script")
        require(last.depends_on == ["call_webhook"], "fail_last must depend on call_webhook")
        require(last.undo == "none", "Set undo: none on the failing final step")
    return wf

def run():
    wf = inspect(3)
    require((ROOT / "reports" / "webhook-ready").exists(), "Wait for the local webhook server")
    require(not (ROOT / "work" / "output").exists(), "Remove the previous output folder before rerunning")
    (ROOT / "reports" / "events.log").write_text("", encoding="utf-8")
    result = WorkflowRunner(wf, base_dir=PATH.parent, project_root=ROOT).run()
    data = result.to_dict()
    (ROOT / "reports" / "run.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Workflow success:", result.success)
    print("Error:", result.error)
    print("Rollback:", json.dumps(result.rollback, indent=2))
    print("Events:")
    print((ROOT / "reports" / "events.log").read_text(encoding="utf-8"), end="")
    print("Report: reports/run.json")

def check_final():
    inspect(3)
    report = json.loads((ROOT / "reports" / "run.json").read_text(encoding="utf-8"))
    require(report["success"] is False, "The last step should fail")
    rb = report.get("rollback") or {}
    require(rb.get("status") == "done", "Hydra did not complete the rollback")
    require([s["step"] for s in rb.get("steps", [])] ==
            ["call_webhook", "create_folder"], "Undo order must be webhook, then folder")
    require(all(s["status"] == "undone" for s in rb["steps"]), "An undo failed")
    events = (ROOT / "reports" / "events.log").read_text(encoding="utf-8").splitlines()
    require(events == EXPECTED, f"Unexpected event order: {events}")
    require(not (ROOT / "work" / "output").exists(), "The created folder still exists")
    require(not (ROOT / ".hydra" / "undo" / "reversible.json").exists(), "An incomplete undo journal remains")
    print("PASS: failure followed by webhook undo and folder undo, in reverse order.")

def main():
    if len(sys.argv) != 2:
        raise ValueError("Usage: lab25.py stage1|stage2|run|check")
    cmd = sys.argv[1]
    if cmd == "stage1":
        inspect(1)
        print("PASS: folder action and undo are defined.")
    elif cmd == "stage2":
        inspect(2)
        print("PASS: both reversible actions are defined.")
    elif cmd == "run":
        run()
    elif cmd == "check":
        check_final()
    else:
        raise ValueError(f"Unknown command: {cmd}")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"FAIL: {exc}")
