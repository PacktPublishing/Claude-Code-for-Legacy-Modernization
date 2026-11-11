#!/usr/bin/env python3
"""Retain raw Git boundary evidence; inventory is not an authorization gate.

Use begin before task execution and end after it. Reject dirty starts. Names
are JSON strings (also NUL-delimited raw files); do not split them on whitespace.
Ignored writes and transient changes require outer filesystem/audit controls.
"""
import argparse
import json
import subprocess
from pathlib import Path


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def capture(repo, out, phase):
    out = Path(out)
    if phase == "begin":
        out.mkdir(parents=True, exist_ok=True)
        status = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")
        (out / "status-before.z").write_bytes(status)
        (out / "revision-before.txt").write_bytes(git(repo, "rev-parse", "HEAD"))
        if status:
            raise ValueError("dirty baseline: preserve evidence and review before task")
        return []
    baseline = (out / "revision-before.txt").read_text().strip()
    final = git(repo, "rev-parse", "HEAD").decode().strip()
    (out / "revision-after.txt").write_text(final + "\n")
    status = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    (out / "status-after.z").write_bytes(status)
    names = set()
    commands = {
        "unstaged.z": ("diff", "--name-only", "--no-renames", "-z"),
        "staged.z": ("diff", "--cached", "--name-only", "--no-renames", "-z"),
        "committed.z": ("diff", "--name-only", "--no-renames", "-z", baseline, final),
        "untracked.z": ("ls-files", "--others", "--exclude-standard", "-z"),
    }
    for filename, args in commands.items():
        raw = git(repo, *args)
        (out / filename).write_bytes(raw)
        names.update(part for part in raw.split(b"\0") if part)
    # Porcelain rename records contain the destination then the original name.
    records = iter(status.split(b"\0"))
    for record in records:
        if not record:
            continue
        names.add(record[3:])
        if b"R" in record[:2] or b"C" in record[:2]:
            names.add(next(records))
    paths = sorted(name.decode("utf-8", errors="surrogateescape") for name in names)
    (out / "changed-files.json").write_text(json.dumps(paths, indent=2) + "\n")
    return paths


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("phase", choices=["begin", "end"])
    p.add_argument("run_dir", type=Path)
    p.add_argument("--repo", type=Path, default=Path.cwd())
    a = p.parse_args()
    try:
        capture(a.repo, a.run_dir, a.phase)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        p.exit(1, f"INVENTORY FAIL: {exc}\n")


if __name__ == "__main__":
    main()
