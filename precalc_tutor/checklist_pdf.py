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
"""Render the printable checklist PDF: one part per mapped chapter, lanes in app order, a checkbox per line."""

from __future__ import annotations

import io
from xml.sax.saxutils import escape

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .catalog import Duolingo, Textbook
from .lanes import chapter_lanes, section_lanes
from .mapping import Mapping

RATING_LABEL = {"full": "full", "partial": "partial", "prerequisite": "prereq"}
BOX = 0.16 * inch


def _styles():
  ss = getSampleStyleSheet()
  return {
    "title": ParagraphStyle("t", parent=ss["Title"], fontSize=16, leading=20, alignment=TA_LEFT, spaceAfter=4),
    "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontSize=14, leading=17, spaceBefore=0, spaceAfter=4),
    "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontSize=11, leading=14, spaceBefore=8, spaceAfter=3, textColor=colors.HexColor("#1F3A5F")),
    "body": ParagraphStyle("b", parent=ss["BodyText"], fontSize=9, leading=11.5),
    "cell": ParagraphStyle("c", parent=ss["BodyText"], fontSize=9, leading=11),
    "small": ParagraphStyle("s", parent=ss["BodyText"], fontSize=7.5, leading=9.5, textColor=colors.HexColor("#555555")),
  }


def _check_table(rows: list[tuple[str, str, str]], st, widths) -> Table:
  """rows: (main text, right text, tag). First column is an empty bordered checkbox cell."""
  data = [["", Paragraph(escape(a), st["cell"]), Paragraph(escape(b), st["cell"]), Paragraph(escape(c), st["cell"])] for a, b, c in rows]
  t = Table(data, colWidths=widths, hAlign="LEFT")
  style = [
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ("LINEBELOW", (1, 0), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
  ]
  for i in range(len(rows)):
    style.append(("BOX", (0, i), (0, i), 0.8, colors.black))
  t.setStyle(TableStyle(style))
  for i in range(len(rows)):
    t._argH[i] = max(t._argH[i] or 0, BOX + 4)
  return t


def mapped_chapters(book: Textbook, mapping: Mapping) -> list:
  """Chapters with at least one section that maps to a Duolingo unit."""
  return [c for c in book.chapters if any(mapping.entry(s.id) and mapping.entry(s.id).units for s in c.sections)]


def _section_guide(ch, course: Duolingo, mapping: Mapping, st, widths) -> list:
  """Per-section quick reference: what to practise on Duolingo and what to read in the book, with checkboxes for book-only items."""
  out = [Paragraph("Section guide", st["h1"]),
         Paragraph("For each section: the Duolingo units that practise it (already listed above with checkboxes), then the "
                   "parts only the textbook teaches. Tick each book-only item once you have worked it in the book.", st["body"])]
  for s in ch.sections:
    e = mapping.entry(s.id)
    block = [Paragraph(f"{escape(s.id)} {escape(s.title)} (p. {escape(s.page)})", st["h2"])]
    if e and e.note:
      block.append(Paragraph(escape(e.note), st["body"]))
    if e and e.units:
      lines = []
      for row in section_lanes(e, course):
        items = " · ".join(f"{lu.unit.order}. {escape(lu.unit.name)} ({RATING_LABEL[lu.rating]})" for lu in row.units)
        lines.append(f"<b>{escape(row.lane.name)}:</b> {items}")
      block.append(Paragraph("<b>Duolingo</b>, in app order:<br/>" + "<br/>".join(lines), st["body"]))
    else:
      block.append(Paragraph("<b>Duolingo:</b> no unit covers this section.", st["body"]))
    if e and e.gaps:
      block.append(Paragraph("<b>Book only:</b>", st["body"]))
      block.append(_check_table([(g, "", "") for g in e.gaps], st, widths))
    out.append(KeepTogether(block))
  return out


def build_pdf(book: Textbook, course: Duolingo, mapping: Mapping, chapters: list[str] | None = None) -> bytes:
  """Render the checklist. With `chapters`, render only those chapters and add a section guide (a standalone handout)."""
  rl_config.invariant = 1
  st = _styles()
  buf = io.BytesIO()
  doc = SimpleDocTemplate(buf, pagesize=letter, leftMargin=0.7 * inch, rightMargin=0.7 * inch,
                          topMargin=0.7 * inch, bottomMargin=0.7 * inch,
                          title="Precalculus with Duolingo Math: checklist", author="precalc-tutor build", invariant=1)
  width = letter[0] - 1.4 * inch
  widths = [BOX + 6, width - (BOX + 6) - 0.9 * inch - 1.1 * inch, 0.9 * inch, 1.1 * inch]

  selected = [c for c in book.chapters if chapters is None or c.id in chapters]
  if chapters is not None and len(selected) == 1:
    ch0 = selected[0]
    heading = f"{'Appendix' if ch0.is_appendix else 'Chapter'} {escape(ch0.id)} Duolingo Math checklist"
  else:
    heading = f"{escape(book.title)}, {book.edition}e: Duolingo Math checklist"
  story = [Paragraph(heading, st["title"]),
           Paragraph("Tick each textbook section as you read it and each Duolingo unit as you finish it. Units are listed per "
                     "lane (a Duolingo grade or topic) in the order the app presents them, so you can follow one lane top to "
                     "bottom. Ratings: full = covers the section's main skill, partial = covers part of it, prereq = a warm-up "
                     "from an earlier grade. The right column names the textbook sections the unit serves.", st["body"]),
           Spacer(1, 6)]
  mapped = [c for c in selected if chapter_lanes(c, mapping, course)]
  if not mapped:
    story.append(Paragraph("No chapters are mapped yet.", st["body"]))
  for idx, ch in enumerate(mapped):
    if idx > 0:
      story.append(PageBreak())
    label = f"Appendix {ch.id}" if ch.is_appendix else f"Chapter {ch.id}"
    story.append(Paragraph(f"{label}: {escape(ch.title)} (p. {escape(ch.page)})", st["h1"]))
    summary = mapping.chapter_summaries.get(ch.id)
    if summary:
      story.append(Paragraph(escape(summary), st["body"]))
    sec_rows = [(f"{s.id} {s.title}", f"p. {s.page}", "") for s in ch.sections]
    block = [Paragraph("Textbook sections", st["h2"]), _check_table(sec_rows, st, widths)]
    gaps = [(s.id, mapping.entry(s.id).gaps) for s in ch.sections if mapping.entry(s.id) and mapping.entry(s.id).gaps]
    if gaps:
      block.append(Paragraph("Book only, not on Duolingo: " + " ".join(f"<b>{escape(sid)}</b> {escape('; '.join(g))}." for sid, g in gaps), st["small"]))
    story.append(KeepTogether(block))
    for lr in chapter_lanes(ch, mapping, course):
      rows = [(f"{lu.unit.order}. {lu.unit.name}", RATING_LABEL[lu.rating], ", ".join(lu.sections)) for lu in lr.units]
      story.append(KeepTogether([Paragraph(escape(lr.lane.name), st["h2"]), _check_table(rows, st, widths)]))
    if chapters is not None:
      story.append(PageBreak())
      story.extend(_section_guide(ch, course, mapping, st, widths))
  story.append(Spacer(1, 10))
  story.append(Paragraph(f"Textbook: {escape(book.citation())} Duolingo inventory: {len(course.units())} units, last verified "
                         f"{escape(course.last_verified)} on {escape(course.platform)}. Only titles and unit names are reproduced, for "
                         "reference; no textbook or Duolingo content is included. This checklist is licensed CC BY 4.0; see the "
                         "repository NOTICE for third-party material.", st["small"]))

  def footer(canvas, d):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawRightString(letter[0] - 0.7 * inch, 0.45 * inch, f"Page {d.page}")
    canvas.drawString(0.7 * inch, 0.45 * inch, "Precalculus with Duolingo Math checklist")
    canvas.restoreState()

  doc.build(story, onFirstPage=footer, onLaterPages=footer)
  return buf.getvalue()
