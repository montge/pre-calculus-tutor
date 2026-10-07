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
"""Derive per-section and per-chapter lanes (one per grade or topic) from the mapping."""

from __future__ import annotations

from dataclasses import dataclass

from .catalog import Chapter, Duolingo, Lane, Unit
from .mapping import Mapping, SectionEntry, UnitRef


@dataclass(frozen=True)
class LaneUnit:
  unit: Unit
  rating: str
  note: str
  sections: tuple[str, ...]  # section ids this unit serves (one for a section lane)


@dataclass(frozen=True)
class LaneRow:
  lane: Lane
  units: tuple[LaneUnit, ...]  # in app path order


def section_lanes(entry: SectionEntry, course: Duolingo) -> list[LaneRow]:
  """One row per contributing grade or topic, grades ascending then topics in app order; units in path order."""
  by_lane: dict[str, list[tuple[Unit, UnitRef]]] = {}
  for ref in entry.units:
    unit = course.unit(ref.unit)
    if unit is None:
      continue
    by_lane.setdefault(unit.lane, []).append((unit, ref))
  rows: list[LaneRow] = []
  for lane_id, pairs in by_lane.items():
    lane = course.lane(lane_id)
    assert lane is not None
    pairs.sort(key=lambda p: p[0].order)
    rows.append(LaneRow(lane=lane, units=tuple(
      LaneUnit(unit=u, rating=r.rating, note=r.note, sections=(entry.section,)) for u, r in pairs)))
  rows.sort(key=lambda r: r.lane.rank)
  return rows


def chapter_lanes(chapter: Chapter, mapping: Mapping, course: Duolingo) -> list[LaneRow]:
  """Merge the chapter's section lanes: each unit once, tagged with every section it serves, in path order."""
  merged: dict[str, dict[str, tuple[Unit, str, str, list[str]]]] = {}
  for section in chapter.sections:
    entry = mapping.entry(section.id)
    if entry is None:
      continue
    for row in section_lanes(entry, course):
      lane_units = merged.setdefault(row.lane.id, {})
      for lu in row.units:
        if lu.unit.id in lane_units:
          lane_units[lu.unit.id][3].append(section.id)
        else:
          lane_units[lu.unit.id] = (lu.unit, lu.rating, lu.note, [section.id])
  rows: list[LaneRow] = []
  for lane_id, lane_units in merged.items():
    lane = course.lane(lane_id)
    assert lane is not None
    items = sorted(lane_units.values(), key=lambda t: t[0].order)
    rows.append(LaneRow(lane=lane, units=tuple(
      LaneUnit(unit=u, rating=r, note=n, sections=tuple(secs)) for u, r, n, secs in items)))
  rows.sort(key=lambda r: r.lane.rank)
  return rows
