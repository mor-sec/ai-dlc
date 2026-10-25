#!/usr/bin/env python3
"""Check relative markdown links and heading anchors across the repo.

No dependencies. Skips http(s)/mailto links and anything inside fenced code
blocks (templates contain illustrative links). Exit 1 on any broken target.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.*)$")
FENCE = re.compile(r"^\s*```")


def slug(text: str) -> str:
    """GitHub-style heading anchor."""
    text = re.sub(r"[`*_]", "", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text)


def body_lines(path: Path):
    """Yield (lineno, line) for lines outside fenced code blocks."""
    in_fence = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield lineno, line


def anchors_of(path: Path) -> set[str]:
    return {slug(m.group(1)) for _, line in body_lines(path) if (m := HEADING.match(line))}


def main() -> int:
    md_files = [p for p in ROOT.rglob("*.md") if not {"node_modules", "worktrees"} & set(p.relative_to(ROOT).parts)]
    anchor_cache: dict[Path, set[str]] = {}
    errors = []

    for path in md_files:
        for lineno, line in body_lines(path):
            for target in LINK.findall(line):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                file_part, _, anchor = target.partition("#")
                dest = (path.parent / file_part).resolve() if file_part else path
                if not dest.exists():
                    errors.append(f"{path.relative_to(ROOT)}:{lineno}: missing file {target}")
                    continue
                if anchor and dest.suffix == ".md":
                    known = anchor_cache.setdefault(dest, anchors_of(dest))
                    if anchor not in known:
                        errors.append(f"{path.relative_to(ROOT)}:{lineno}: missing anchor {target}")

    for e in errors:
        print(e)
    print(f"Checked {len(md_files)} file(s), {len(errors)} broken link(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
