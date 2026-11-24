"""Houseplant out-of-office entry builder for make.fun.

Packages the one-line reply in entry.txt: gates it (1..120 chars, one
line, not blank) and copies it into the scorer's output directory.
"""
import json
import os
import shutil
import sys
from pathlib import Path


class PlantReply:
    LIMIT = 120
    FLOOR = 1

    def __init__(self, root):
        self.source = Path(root) / "entry.txt"
        self.reply = self.source.read_text(encoding="utf-8")

    def legal(self):
        body = self.reply.strip().replace("\t", " ")
        if len(body) < self.FLOOR or len(body) > self.LIMIT:
            return False
        return len(body.splitlines()) == 1 and bool(body)

    def ship(self):
        out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
        out.mkdir(parents=True, exist_ok=True)
        placed = out / "entry.txt"
        shutil.copyfile(self.source, placed)
        return placed


receipt = PlantReply(Path(__file__).resolve().parent)
if not receipt.legal():
    print("entry.txt fails the houseplant gate", file=sys.stderr)
    sys.exit(1)
placed = receipt.ship()
print(json.dumps({"entry": str(placed), "chars": len(receipt.reply.strip()), "gate": "pass"}))
