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
"""Load the section-to-unit mapping."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from . import MAPPING_PATH

RATINGS = ("full", "partial", "prerequisite")
RATING_ORDER = {"prerequisite": 0, "full": 1, "partial": 2}


@dataclass(frozen=True)
class UnitRef:
  unit: str
  rating: str
  note: str


@dataclass(frozen=True)
class SectionEntry:
  section: str
  reviewed: bool
  note: str
  units: tuple[UnitRef, ...]
  gaps: tuple[str, ...] = ()  # parts of the section Duolingo does not cover (book only)


@dataclass(frozen=True)
class Mapping:
  textbook: str
  duolingo: str
  chapter_summaries: dict[str, str]
  entries: tuple[SectionEntry, ...]

  def entry(self, section_id: str) -> SectionEntry | None:
    for e in self.entries:
      if e.section == section_id:
        return e
    return None


def load_mapping(path: Path = MAPPING_PATH) -> Mapping:
  raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
  summaries = {str(c["number"]): str(c.get("summary") or "") for c in (raw.get("chapters") or [])}
  entries = tuple(
    SectionEntry(
      section=str(e["section"]), reviewed=bool(e.get("reviewed", False)), note=str(e.get("note") or ""),
      units=tuple(UnitRef(unit=str(u["unit"]), rating=str(u.get("rating", "")), note=str(u.get("note") or ""))
                  for u in (e.get("units") or [])),
      gaps=tuple(str(g) if g is not None else "" for g in (e.get("gaps") or [])),
    )
    for e in (raw.get("sections") or [])
  )
  return Mapping(textbook=str(raw["textbook"]), duolingo=str(raw["duolingo"]), chapter_summaries=summaries, entries=entries)
