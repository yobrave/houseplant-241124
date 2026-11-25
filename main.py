"""Houseplant out-of-office entry shipper."""
import json
import os
import pathlib
import sys

LIMIT = 120
ROOT = pathlib.Path(__file__).resolve().parent
MODE = "auto-reply"


def grow():
    raw = (ROOT / "entry.txt").read_bytes().decode("utf-8").strip()
    span = len(raw)
    if not 1 <= span <= LIMIT:
        raise ValueError(f"houseplant line out of range: {span}")
    return raw, span


def main():
    try:
        text, span = grow()
    except Exception as err:
        print(json.dumps({"state": "wilted", "why": str(err)}))
        sys.exit(2)
    out = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    out.mkdir(parents=True, exist_ok=True)
    (out / "entry.txt").write_bytes(text.encode("utf-8"))
    print(json.dumps({"state": "watered", "note": "entry shipped", "span": span}))


if __name__ == "__main__":
    main()
