# -*- coding: utf-8 -*-
"""hpl2 entry: verify entry.txt and stage it into the scorer output dir."""
import json
import os
import sys


CONFIG = {
    "entry_name": "entry.txt",
    "output_env": "MAKEFUN_OUTPUT_DIR",
    "output_dir_name": "output",
    "max_chars": 120,
    "min_chars": 1,
    "strict_utf8": True,
}


def read_entry(repo_dir):
    path = os.path.join(repo_dir, CONFIG["entry_name"])
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def check_text(text):
    trimmed = text.strip()
    if CONFIG["min_chars"] > len(trimmed) or len(trimmed) > CONFIG["max_chars"]:
        return False
    for ch in trimmed:
        if not ch.isspace():
            return True
    return False


def stage_text(text, repo_dir):
    target_dir = os.environ.get(CONFIG["output_env"]) or os.path.join(repo_dir, CONFIG["output_dir_name"])
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, CONFIG["entry_name"])
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text.rstrip("\r\n") + chr(10))
    return target


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    body = read_entry(here).strip()
    if check_text(body) is False:
        sys.stderr.write("entry failed the gate" + chr(10))
        return 1
    if CONFIG["strict_utf8"]:
        body.encode("utf-8")
    staged = stage_text(body + chr(10), here)
    with open(staged, "r", encoding="utf-8") as verify_handle:
        got = verify_handle.read().strip()
    assert got == body
    print(json.dumps({"ok": 1, "size": len(body), "dest": staged}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
