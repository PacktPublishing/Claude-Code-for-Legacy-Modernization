"""Validate decision completeness, not signer identity or authority."""
from datetime import date
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs/decisions/0001-rounding-mismatch.md"
REQUIRED = {"Status": "accepted for local exercise",
            "Disposition": "preserve legacy rule / correct replacement implementation"}

def validate(text):
    pairs = re.findall(r"^\*\*([^*\r\n]+):\*\* ([^\r\n]*)\r?$", text, re.MULTILINE)
    fields = dict(pairs)
    if len(fields) != len(pairs):
        raise ValueError("duplicate decision fields")
    for name, value in REQUIRED.items():
        if fields.get(name) != value:
            raise ValueError(f"invalid or missing {name}")
    for name in ("Reviewer", "Date", "Revision", "Evidence"):
        if not fields.get(name, "").strip() or fields[name].lstrip().startswith("<"):
            raise ValueError(f"missing {name}")
    date.fromisoformat(fields["Date"])
    if not re.fullmatch(r"[0-9a-f]{40}", fields["Revision"]):
        raise ValueError("Revision must be a full Git commit ID")
    return fields

def check():
    return validate(DECISION.read_text())

if __name__ == "__main__":
    import sys
    try:
        check()
    except (OSError, ValueError) as exc:
        print(f"REVIEW REQUIRED: {exc}", file=sys.stderr)
        sys.exit(2)
    print("Decision fields complete; verify human authority separately.")
