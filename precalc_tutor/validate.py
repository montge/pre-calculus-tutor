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
"""Integrity checks across the three data files. Every check returns all errors it finds."""

from __future__ import annotations

import datetime as _dt
from collections import Counter
from pathlib import Path

from . import DATA_DIR
from .catalog import Duolingo, Textbook
from .mapping import RATINGS, Mapping

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".bmp", ".tif", ".tiff", ".pdf"}


def validate_textbook(book: Textbook) -> list[str]:
  errors: list[str] = []
  ids = [s.id for s in book.sections()]
  for sid, n in Counter(ids).items():
    if n > 1:
      errors.append(f"textbook: section id {sid!r} appears {n} times")
  for s in book.sections():
    if not s.title:
      errors.append(f"textbook: section {s.id} has no title")
    if not s.page:
      errors.append(f"textbook: section {s.id} has no page")
  return errors


def validate_duolingo(course: Duolingo) -> list[str]:
  errors: list[str] = []
  try:
    _dt.date.fromisoformat(course.last_verified)
  except ValueError:
    errors.append(f"duolingo: last_verified {course.last_verified!r} is not an ISO date")
  if not course.platform:
    errors.append("duolingo: platform is missing")
  ids = [u.id for u in course.units()]
  for uid, n in Counter(ids).items():
    if n > 1:
      errors.append(f"duolingo: unit id {uid!r} appears {n} times")
  for lane in course.lanes:
    if len(lane.units) != lane.unit_count:
      errors.append(f"duolingo: {lane.name} lists {len(lane.units)} units but unit_count is {lane.unit_count}")
    orders = [u.order for u in lane.units]
    if orders != list(range(1, len(orders) + 1)):
      errors.append(f"duolingo: {lane.name} unit order values are not 1..{len(orders)} in sequence")
    for u in lane.units:
      if not u.name:
        errors.append(f"duolingo: unit {u.id} in {lane.name} has no name")
  return errors


def validate_mapping(mapping: Mapping, book: Textbook, course: Duolingo) -> list[str]:
  errors: list[str] = []
  if mapping.textbook != book.id:
    errors.append(f"mapping: textbook {mapping.textbook!r} does not match catalog {book.id!r}")
  if mapping.duolingo != course.id:
    errors.append(f"mapping: duolingo {mapping.duolingo!r} does not match catalog {course.id!r}")
  book_ids = [s.id for s in book.sections()]
  entry_ids = [e.section for e in mapping.entries]
  for sid, n in Counter(entry_ids).items():
    if n > 1:
      errors.append(f"mapping: section {sid} has {n} entries")
  for sid in book_ids:
    if sid not in entry_ids:
      errors.append(f"mapping: section {sid} has no entry")
  for sid in entry_ids:
    if sid not in book_ids:
      errors.append(f"mapping: entry {sid} is not a section in the textbook catalog")
  for e in mapping.entries:
    seen: set[str] = set()
    for u in e.units:
      if course.unit(u.unit) is None:
        errors.append(f"mapping: section {e.section} references unknown unit {u.unit!r}")
      if u.rating not in RATINGS:
        errors.append(f"mapping: section {e.section} unit {u.unit} has invalid rating {u.rating!r}")
      if u.unit in seen:
        errors.append(f"mapping: section {e.section} lists unit {u.unit} twice")
      seen.add(u.unit)
  chapter_ids = {c.id for c in book.chapters}
  for cid in mapping.chapter_summaries:
    if cid not in chapter_ids:
      errors.append(f"mapping: chapter summary for unknown chapter {cid!r}")
  return errors


def validate_data_dir(data_dir: Path = DATA_DIR) -> list[str]:
  """No images or scans anywhere under data/."""
  errors: list[str] = []
  for p in sorted(Path(data_dir).rglob("*")):
    if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES:
      errors.append(f"data: image or scan file not allowed: {p.relative_to(data_dir)}")
  return errors


def validate(book: Textbook, course: Duolingo, mapping: Mapping, data_dir: Path = DATA_DIR) -> list[str]:
  return (validate_textbook(book) + validate_duolingo(course)
          + validate_mapping(mapping, book, course) + validate_data_dir(data_dir))
