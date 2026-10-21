#!/usr/bin/env python3
"""Make every filename in the repo Windows-safe, then commit, pull and push.

Usage (from anywhere inside the repo):
    python sync.py                     # rename, commit, pull --rebase, push
    python sync.py "Add Vojnovic P3"   # same, with your own commit message
    python sync.py --dry-run           # just show what would be renamed

Works on Linux, macOS and Windows. On Windows it will rarely find anything,
because Windows can't create these names in the first place; the problem
files come from the Linux side.
"""
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime

# Characters Windows forbids in names, and what to use instead.
REPLACEMENTS = {
    ":": " -",
    '"': "'",
    "<": "(",
    ">": ")",
    "|": "-",
    "\\": "-",
    "?": "",
    "*": "",
}
CONTROL_CHARS = re.compile(r"[\x00-\x1f]")  # newlines, tabs etc.
RESERVED = {"CON", "PRN", "AUX", "NUL",
            *(f"COM{i}" for i in range(1, 10)),
            *(f"LPT{i}" for i in range(1, 10))}
LONG_PATH_WARN = 180  # repo-relative length; Windows limit is 260 for the full path


def safe_name(name: str) -> str:
    new = CONTROL_CHARS.sub(" ", name)
    for bad, good in REPLACEMENTS.items():
        new = new.replace(bad, good)
    new = re.sub(r" {2,}", " ", new)
    new = new.lstrip(" ").rstrip(" .")  # Windows drops trailing dots/spaces
    if not new:
        new = "_"
    if new.split(".")[0].upper() in RESERVED:
        new = "_" + new
    return new


def unique_target(directory: str, name: str) -> str:
    stem, ext = os.path.splitext(name)
    candidate, n = name, 1
    while os.path.exists(os.path.join(directory, candidate)):
        candidate = f"{stem} ({n}){ext}"
        n += 1
    return candidate


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], check=check, text=True,
                          capture_output=True)


def sanitise(root: str, dry_run: bool) -> int:
    renamed = 0
    # Bottom-up so files are renamed before the folders that contain them.
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir.split(os.sep)[0] == ".git":
            continue
        for name in filenames + dirnames:
            if name == ".git":
                continue
            new = safe_name(name)
            if new == name:
                continue
            new = unique_target(dirpath, new)
            shown_old = os.path.join(rel_dir, name).encode("unicode_escape").decode()
            print(f"  {shown_old}\n    -> {os.path.join(rel_dir, new)}")
            if not dry_run:
                os.rename(os.path.join(dirpath, name), os.path.join(dirpath, new))
            renamed += 1
    return renamed


def warn_about(root: str) -> None:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        # Names that differ only by case clash on Windows.
        by_lower = defaultdict(list)
        for name in filenames + dirnames:
            by_lower[name.lower()].append(name)
        for names in by_lower.values():
            if len(names) > 1:
                print(f"  WARNING: names differ only by case in "
                      f"{os.path.relpath(dirpath, root)}: {names}")
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root)
            if len(rel) > LONG_PATH_WARN:
                print(f"  WARNING: long path ({len(rel)} chars), may hit the "
                      f"Windows 260-char limit:\n    {rel}")


def main() -> None:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    message = args[0] if args else f"Sync {datetime.now():%Y-%m-%d %H:%M}"

    try:
        root = git("rev-parse", "--show-toplevel").stdout.strip()
    except subprocess.CalledProcessError:
        sys.exit("Not inside a git repository.")

    print("Checking filenames...")
    n = sanitise(root, dry_run)
    print(f"  {n} renamed" if n else "  all filenames OK")
    warn_about(root)

    if dry_run:
        return

    os.chdir(root)
    git("add", "-A")
    if git("diff", "--cached", "--quiet", check=False).returncode != 0:
        git("commit", "-m", message)
        print(f"Committed: {message}")
    else:
        print("Nothing new to commit.")

    print("Pulling (rebase)...")
    pull = git("pull", "--rebase", check=False)
    if pull.returncode != 0:
        sys.exit("Pull failed - resolve this by hand, then rerun:\n"
                 + pull.stdout + pull.stderr)

    print("Pushing...")
    push = git("push", check=False)
    if push.returncode != 0:
        sys.exit("Push failed:\n" + push.stdout + push.stderr)
    print("Done.")


if __name__ == "__main__":
    main()