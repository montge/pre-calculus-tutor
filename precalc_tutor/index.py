# Copyright 2026 Evan Montgomery-Recht
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Render the Markdown mapping index from the catalogs and mapping."""

from __future__ import annotations

from .catalog import Chapter, Duolingo, Textbook
from .lanes import LaneRow, chapter_lanes, section_lanes
from .mapping import RATING_ORDER, Mapping

RATING_LABEL = {"full": "full", "partial": "partial", "prerequisite": "prereq"}


def _md(text: str) -> str:
  return text.replace("|", "\\|").replace("\n", " ").strip()


def _lane_table(rows: list[LaneRow], with_sections: bool) -> list[str]:
  out = ["| Lane | Units to follow, in app order |", "| --- | --- |"]
  for row in rows:
    cells = []
    for lu in row.units:
      tag = f" ({', '.join(lu.sections)})" if with_sections else ""
      cells.append(f"{_md(lu.unit.name)} [{RATING_LABEL[lu.rating]}]{tag}")
    out.append(f"| {_md(row.lane.name)} | {' · '.join(cells)} |")
  return out


def _chapter_heading(ch: Chapter) -> str:
  label = f"Appendix {ch.id}" if ch.is_appendix else f"Chapter {ch.id}"
  return f"## {label}: {_md(ch.title)} (p. {ch.page})"


def render_index(book: Textbook, course: Duolingo, mapping: Mapping) -> str:
  lines: list[str] = []
  lines.append(f"# Duolingo Math units for *{_md(book.title)}*, {book.edition}e")
  lines.append("")
  lines.append("Generated from the data files in `data/`; do not edit by hand. For each textbook section, the Duolingo "
               "units to practise are listed with a coverage rating: **full** (the unit covers the section's main "
               "skill), **partial** (covers part of it), or **prereq** (a warm-up from an earlier grade). Each chapter "
               "and section also shows one lane per Duolingo grade or topic, with that lane's units in the order the "
               "app presents them. Sections marked *draft* have not yet been reviewed.")
  lines.append("")
  if not course.complete:
    lines.append("> **Notice:** the Duolingo inventory is incomplete. Recommendations may be missing units.")
    lines.append("")

  no_coverage: list[str] = []
  for ch in book.chapters:
    lines.append(_chapter_heading(ch))
    lines.append("")
    summary = mapping.chapter_summaries.get(ch.id, "")
    if summary:
      lines.append(_md(summary))
      lines.append("")
    rows = chapter_lanes(ch, mapping, course)
    if rows:
      lines.append("**Chapter lanes** (each unit once, tagged with the sections it serves):")
      lines.append("")
      lines.extend(_lane_table(rows, with_sections=True))
      lines.append("")
    else:
      lines.append("*No Duolingo units are mapped for this chapter yet.*")
      lines.append("")
    for s in ch.sections:
      entry = mapping.entry(s.id)
      draft = "" if entry and entry.reviewed else " *(draft)*"
      lines.append(f"### {s.id} {_md(s.title)} (p. {s.page}){draft}")
      lines.append("")
      if entry and entry.note:
        lines.append(_md(entry.note))
        lines.append("")
      if entry and entry.gaps:
        lines.append("**Book only** (Duolingo does not cover): " + "; ".join(_md(g) for g in entry.gaps) + ".")
        lines.append("")
      if not entry or not entry.units:
        lines.append("No Duolingo coverage for this section.")
        lines.append("")
        no_coverage.append(f"{s.id} {s.title}")
        continue
      srows = section_lanes(entry, course)
      lines.extend(_lane_table(srows, with_sections=False))
      lines.append("")
      ordered = sorted(entry.units, key=lambda u: (RATING_ORDER[u.rating], course.unit(u.unit).lane, course.unit(u.unit).order))
      for ref in ordered:
        u = course.unit(ref.unit)
        lane = course.lane(u.lane)
        lines.append(f"- **{_md(u.name)}** ({_md(lane.name)}, unit {u.order}) · {RATING_LABEL[ref.rating]} · {_md(ref.note)}")
      lines.append("")

  lines.append("## Book-only topics by chapter")
  lines.append("")
  lines.append("Everything a section needs that Duolingo does not practise. The chapter study guides teach exactly these.")
  lines.append("")
  for ch in book.chapters:
    items = [(s.id, mapping.entry(s.id).gaps) for s in ch.sections if mapping.entry(s.id) and mapping.entry(s.id).gaps]
    if not items:
      continue
    lines.append(f"**{'Appendix' if ch.is_appendix else 'Chapter'} {ch.id}**")
    lines.append("")
    for sid, gaps in items:
      lines.append(f"- {sid}: " + "; ".join(_md(g) for g in gaps))
    lines.append("")
  lines.append("## Sections with no Duolingo coverage")
  lines.append("")
  lines.append(f"{len(no_coverage)} of {len(book.sections())} sections have no mapped unit:")
  lines.append("")
  for item in no_coverage:
    lines.append(f"- {_md(item)}")
  lines.append("")
  lines.append("## Sources")
  lines.append("")
  lines.append(f"Textbook: {_md(book.citation()).replace(_md(book.title), f'*{_md(book.title)}*', 1)}")
  unverified = [k for k, v in book.verified.items() if not v]
  if unverified:
    lines.append(f"Citation fields not yet verified against the book's copyright page: {', '.join(unverified)}.")
  lines.append("")
  lines.append(f"Duolingo inventory: *{_md(course.title)}*, {len(course.units())} units across "
               f"{sum(1 for l in course.lanes if l.kind == 'grade')} grades and "
               f"{sum(1 for l in course.lanes if l.kind == 'topic')} topics, last verified {course.last_verified} on {course.platform}.")
  lines.append("")
  lines.append("Only chapter and section titles, page numbers, and Duolingo unit names are reproduced here, for the "
               "purpose of reference. No textbook or Duolingo content is included. Data and this index are licensed "
               "CC BY 4.0; see the repository NOTICE for third-party material.")
  lines.append("")
  return "\n".join(lines)
