#!/usr/bin/env python3
"""Check the playbook's structural conventions from CLAUDE.md.

- Front-matter: every chapter and standard carries owner, audience, and a
  valid, non-future reviewed date.
- Chapter shape: chapters end with Anti-patterns, Tips & tricks, References,
  and References links the previous and next chapters; appendices end with
  References.
- README: every chapter, appendix, and standard has a link there.
- Glossary: every Chapter 01 vocabulary term has an entry, and every entry
  links to a playbook chapter or standard.
- ADRs: numbered 0001 upward with no gaps or duplicates, each with Status,
  Date, and Deciders.

No dependencies. Headings inside fenced code blocks are ignored, since
templates wrap their copyable body in a fence. Optional argument: the repo
root to check (default: this script's repo). Exit 1 on any violation.
"""
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^\s*```")
H2 = re.compile(r"^##\s+(.*?)\s*$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)\s]*)?\)")
CHAPTER = re.compile(r"^(\d{2})-.+\.md$")
ADR = re.compile(r"^(\d{4})-.+\.md$")
FRONT_MATTER_KEYS = ("owner", "audience", "reviewed")
CHAPTER_ENDING = ["Anti-patterns", "Tips & tricks", "References"]
ADR_FIELDS = ("Status", "Date", "Deciders")

errors: list[str] = []


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def body_lines(path: Path) -> list[str]:
    """Lines outside fenced code blocks."""
    out, in_fence = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return out


def h2_sections(path: Path) -> list[tuple[str, list[str]]]:
    """(heading, body lines) for each H2, in order."""
    sections: list[tuple[str, list[str]]] = []
    for line in body_lines(path):
        if m := H2.match(line):
            sections.append((m.group(1), []))
        elif sections:
            sections[-1][1].append(line)
    return sections


def link_targets(path: Path, lines: list[str]) -> set[Path]:
    """Resolved relative link targets in the given lines of path."""
    targets = set()
    for line in lines:
        for target in LINK.findall(line):
            if not target.startswith(("http://", "https://", "mailto:")):
                targets.add((path.parent / target).resolve())
    return targets


def front_matter(path: Path) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None
    fields = {}
    for line in lines[1:]:
        if line == "---":
            return fields
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return None


def check_front_matter(files: list[Path]) -> None:
    today = datetime.date.today()
    for path in files:
        fields = front_matter(path)
        if fields is None:
            errors.append(f"{rel(path)}: missing front-matter block")
            continue
        for key in FRONT_MATTER_KEYS:
            if not fields.get(key):
                errors.append(f"{rel(path)}: front-matter missing '{key}'")
        if reviewed := fields.get("reviewed"):
            try:
                if datetime.date.fromisoformat(reviewed) > today:
                    errors.append(f"{rel(path)}: reviewed date {reviewed} is in the future")
            except ValueError:
                errors.append(f"{rel(path)}: reviewed '{reviewed}' is not a YYYY-MM-DD date")


def check_chapters(chapters: dict[int, Path], appendices: list[Path]) -> None:
    for number, path in sorted(chapters.items()):
        sections = h2_sections(path)
        ending = [heading for heading, _ in sections[-3:]]
        if ending != CHAPTER_ENDING:
            errors.append(f"{rel(path)}: last H2s are {ending}, expected {CHAPTER_ENDING}")
            continue
        refs = link_targets(path, sections[-1][1])
        for neighbour, label in ((number - 1, "previous"), (number + 1, "next")):
            if neighbour in chapters and chapters[neighbour].resolve() not in refs:
                errors.append(f"{rel(path)}: References has no link to the {label} chapter {chapters[neighbour].name}")
    for path in appendices:
        sections = h2_sections(path)
        if not sections or sections[-1][0] != "References":
            errors.append(f"{rel(path)}: last H2 must be References")


def check_readme(files: list[Path]) -> None:
    readme = ROOT / "README.md"
    linked = link_targets(readme, body_lines(readme))
    for path in files:
        if path.resolve() not in linked:
            errors.append(f"README.md: no link to {rel(path)}")


def check_glossary(chapter_01: Path | None) -> None:
    glossary = ROOT / "GLOSSARY.md"
    sections = h2_sections(glossary)
    entries = {heading.lower() for heading, _ in sections}
    for heading, body in sections:
        targets = link_targets(glossary, body)
        if not any(t.is_relative_to(ROOT / "playbook") or t.is_relative_to(ROOT / "standards") for t in targets):
            errors.append(f"GLOSSARY.md: entry '{heading}' links to no chapter or standard")
    if chapter_01 is None:
        return
    vocabulary = dict(h2_sections(chapter_01)).get("The vocabulary")
    if vocabulary is None:
        errors.append(f"{rel(chapter_01)}: no 'The vocabulary' section")
        return
    for line in vocabulary:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and (m := re.fullmatch(r"\*\*(.+?)\*\*", cells[1])):
            if m.group(1).lower() not in entries:
                errors.append(f"GLOSSARY.md: no entry for Chapter 01 term '{m.group(1)}'")


def check_adrs() -> None:
    numbers: dict[int, list[Path]] = {}
    for path in sorted((ROOT / "docs" / "adr").glob("*.md")):
        if m := ADR.match(path.name):
            numbers.setdefault(int(m.group(1)), []).append(path)
            text = path.read_text(encoding="utf-8")
            for field in ADR_FIELDS:
                if not re.search(rf"^- \*\*{field}:\*\* \S", text, re.MULTILINE):
                    errors.append(f"{rel(path)}: missing '- **{field}:**' line")
    for number, paths in numbers.items():
        if len(paths) > 1:
            errors.append(f"docs/adr: number {number:04d} used by {', '.join(p.name for p in paths)}")
    for missing in sorted(set(range(1, max(numbers, default=0) + 1)) - set(numbers)):
        errors.append(f"docs/adr: gap in numbering, no {missing:04d}")


def main() -> int:
    playbook = sorted((ROOT / "playbook").glob("*.md"))
    standards = sorted((ROOT / "standards").glob("*.md"))
    chapters = {int(m.group(1)): p for p in playbook if (m := CHAPTER.match(p.name))}
    appendices = [p for p in playbook if p.name.startswith("appendix-")]

    check_front_matter(playbook + standards)
    check_chapters(chapters, appendices)
    check_readme(playbook + standards)
    check_glossary(chapters.get(1))
    check_adrs()

    for e in errors:
        print(e)
    print(f"Checked {len(playbook)} playbook and {len(standards)} standards file(s), {len(errors)} violation(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
