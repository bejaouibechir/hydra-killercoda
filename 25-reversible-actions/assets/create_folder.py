from pathlib import Path

root = Path(__file__).resolve().parents[1]
(root / "work" / "output").mkdir()
with (root / "reports" / "events.log").open("a", encoding="utf-8") as log:
    log.write("folder_created\n")
