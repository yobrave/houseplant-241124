"""Houseplant front-desk: passes the auto-reply note to the grading tray."""
import json
import os
from pathlib import Path

RIM = 120
POT = "hpl3-water-friday"


def draft(home: Path) -> str:
    return (home / "entry.txt").read_text(encoding="utf-8")


def groom(note: str) -> str:
    tidy = note.replace("\r", "")
    if not (line := next((r for r in tidy.split("\n") if r.strip()), "")):
        return ""
    return line


def pour(line: str, home: Path) -> Path:
    tray = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    tray.mkdir(parents=True, exist_ok=True)
    slot = tray / "entry.txt"
    slot.write_bytes(line.encode("utf-8"))
    assert slot.read_bytes() == line.encode("utf-8"), "pour lost a drop"
    return slot


def main():
    home = Path(__file__).resolve().parent
    line = groom(draft(home))
    if not line.strip():
        print(json.dumps({"leaf": "wilted"}))
        return 1
    if len(line) > RIM:
        print(json.dumps({"leaf": "overgrown", "span": len(line)}))
        return 1
    slot = pour(line, home)
    print(json.dumps({"leaf": "perky", "span": len(line), "pot": POT, "slot": slot.name}))
    return 0


raise SystemExit(main())
