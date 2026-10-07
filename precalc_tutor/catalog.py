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
"""Load the textbook and Duolingo catalogs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import DUOLINGO_PATH, TEXTBOOK_PATH


@dataclass(frozen=True)
class Section:
  id: str
  title: str
  page: str
  chapter: str  # chapter number as a string, or appendix letter


@dataclass(frozen=True)
class Chapter:
  id: str  # "1".."12" or "A", "B"
  title: str
  page: str
  sections: tuple[Section, ...]
  is_appendix: bool = False


@dataclass(frozen=True)
class Textbook:
  id: str
  title: str
  edition: int
  author: str
  publisher: str
  year: int | None
  isbn: str | None
  verified: dict[str, bool]
  chapters: tuple[Chapter, ...]  # numbered chapters then appendices, book order

  def sections(self) -> list[Section]:
    return [s for c in self.chapters for s in c.sections]

  def section(self, section_id: str) -> Section | None:
    for s in self.sections():
      if s.id == section_id:
        return s
    return None

  def citation(self) -> str:
    year = str(self.year) if self.year is not None else "n.d."
    return f"{self.author}. *{self.title}*, {_ordinal(self.edition)} ed. {self.publisher}, {year}."


def _ordinal(n: int) -> str:
  suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
  return f"{n}{suffix}"


def load_textbook(path: Path = TEXTBOOK_PATH) -> Textbook:
  raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
  chapters: list[Chapter] = []
  for ch in raw.get("chapters", []):
    cid = str(ch["number"])
    chapters.append(Chapter(
      id=cid, title=ch["title"], page=str(ch["page"]),
      sections=tuple(Section(id=str(s["id"]), title=s["title"], page=str(s["page"]), chapter=cid) for s in ch["sections"]),
    ))
  for ap in raw.get("appendices", []):
    cid = str(ap["id"])
    chapters.append(Chapter(
      id=cid, title=ap["title"], page=str(ap["page"]), is_appendix=True,
      sections=tuple(Section(id=str(s["id"]), title=s["title"], page=str(s["page"]), chapter=cid) for s in ap["sections"]),
    ))
  return Textbook(
    id=raw["id"], title=raw["title"], edition=int(raw["edition"]), author=raw["author"],
    publisher=raw["publisher"], year=raw.get("year"), isbn=raw.get("isbn"),
    verified=dict(raw.get("verified", {})), chapters=tuple(chapters),
  )


@dataclass(frozen=True)
class Unit:
  id: str
  name: str
  order: int
  lane: str  # lane id: "g9" for grade 9, or the topic id
  description: str = ""


@dataclass(frozen=True)
class Lane:
  """A grade or a topic: one ordered path of units in the app."""
  id: str
  name: str  # "Grade 9" or the topic name
  kind: str  # "grade" or "topic"
  rank: int  # sort key: grades by number, then topics in app order
  unit_count: int
  units: tuple[Unit, ...]


@dataclass(frozen=True)
class Duolingo:
  id: str
  title: str
  last_verified: str
  platform: str
  complete: bool
  lanes: tuple[Lane, ...]
  _units: dict[str, Unit] = field(default_factory=dict, compare=False, repr=False)

  def units(self) -> list[Unit]:
    return [u for lane in self.lanes for u in lane.units]

  def unit(self, unit_id: str) -> Unit | None:
    return self._units.get(unit_id)

  def lane(self, lane_id: str) -> Lane | None:
    for lane in self.lanes:
      if lane.id == lane_id:
        return lane
    return None


def load_duolingo(path: Path = DUOLINGO_PATH) -> Duolingo:
  raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
  lanes: list[Lane] = []
  for g in raw.get("grades", []):
    lid = f"g{g['grade']}"
    units = tuple(Unit(id=str(u["id"]), name=str(u["name"]), order=int(u["order"]), lane=lid,
                       description=str(u.get("description") or "")) for u in (g.get("units") or []))
    lanes.append(Lane(id=lid, name=f"Grade {g['grade']}", kind="grade", rank=int(g["grade"]),
                      unit_count=int(g["unit_count"]), units=units))
  for i, t in enumerate(raw.get("topics", [])):
    lid = str(t["id"])
    units = tuple(Unit(id=str(u["id"]), name=str(u["name"]), order=int(u["order"]), lane=lid,
                       description=str(u.get("description") or "")) for u in (t.get("units") or []))
    lanes.append(Lane(id=lid, name=str(t["name"]), kind="topic", rank=1000 + i,
                      unit_count=int(t["unit_count"]), units=units))
  index = {u.id: u for lane in lanes for u in lane.units}
  return Duolingo(
    id=raw["id"], title=raw["title"], last_verified=str(raw["last_verified"]), platform=str(raw["platform"]),
    complete=bool(raw.get("complete", False)), lanes=tuple(lanes), _units=index,
  )
