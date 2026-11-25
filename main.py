"""Houseplant out-of-office: auto-reply exporter, build round 4."""
import json
import pathlib
import shutil

HARD_STOP = 120
CALLSIGN = "hoo4-houseplant-ooo-r4"


def main():
    src = pathlib.Path("entry.txt")
    body = src.read_text(encoding="utf-8").strip()
    n = len(body)
    state = "valid" if 1 <= n <= HARD_STOP else "invalid"
    water = "escalated" if state == "valid" else "held"
    if state == "valid":
        out = pathlib.Path("out")
        out.mkdir(exist_ok=True)
        shutil.copyfile(src, out / "entry.txt")
    print(json.dumps({"callsign": CALLSIGN, "chars": n, "state": state, "stop": HARD_STOP}))


if __name__ == "__main__":
    main()
