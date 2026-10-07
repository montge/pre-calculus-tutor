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
import unittest

from precalc_tutor import MAPPING_PATH
from precalc_tutor.catalog import load_duolingo, load_textbook
from precalc_tutor.lanes import chapter_lanes, section_lanes
from precalc_tutor.mapping import load_mapping
from precalc_tutor.validate import validate_mapping
from tests.helpers import modified, write_temp_data


class LessonMappingTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.book = load_textbook()
    cls.course = load_duolingo()
    cls.mapping = load_mapping()

  def _errors_for(self, mutate):
    data = write_temp_data(mapping=modified(MAPPING_PATH, mutate))
    return validate_mapping(load_mapping(data / "mappings" / MAPPING_PATH.name), self.book, self.course)

  def test_every_section_has_exactly_one_entry(self):
    self.assertEqual([e.section for e in self.mapping.entries], [s.id for s in self.book.sections()])

  def test_all_units_resolve_and_ratings_valid(self):
    self.assertEqual(validate_mapping(self.mapping, self.book, self.course), [])

  def test_chapters_1_to_3_are_mapped(self):
    for s in self.book.sections():
      if s.chapter in ("1", "2", "3"):
        entry = self.mapping.entry(s.id)
        self.assertIsNotNone(entry)
        self.assertTrue(entry.note, s.id)
        if s.id not in ("2.3", "2.7"):
          self.assertTrue(entry.units, s.id)

  def test_missing_entry_is_reported(self):
    errors = self._errors_for(lambda d: d["sections"].pop(0))
    self.assertIn("mapping: section 1.1 has no entry", errors)

  def test_extra_entry_is_reported(self):
    errors = self._errors_for(lambda d: d["sections"].append({"section": "99.1", "units": []}))
    self.assertIn("mapping: entry 99.1 is not a section in the textbook catalog", errors)

  def test_invalid_rating_is_reported(self):
    def mutate(d):
      d["sections"][0]["units"][0]["rating"] = "great"
    errors = self._errors_for(mutate)
    self.assertTrue(any("section 1.1" in e and "invalid rating 'great'" in e for e in errors), errors)

  def test_dangling_unit_names_section_and_unit(self):
    def mutate(d):
      d["sections"][0]["units"][0]["unit"] = "u-g99-01"
    errors = self._errors_for(mutate)
    self.assertIn("mapping: section 1.1 references unknown unit 'u-g99-01'", errors)

  def test_gaps_present_for_chapters_1_to_3(self):
    self.assertEqual(self.mapping.entry("2.3").gaps[:2], ("Polynomial long division", "Synthetic division"))
    self.assertEqual(self.mapping.entry("1.7").gaps, ())
    self.assertEqual(self.mapping.entry("4.1").gaps, ())

  def test_empty_gap_is_reported(self):
    def mutate(d):
      d["sections"][0]["gaps"] = ["", "ok"]
    errors = self._errors_for(mutate)
    self.assertIn("mapping: section 1.1 gap 1 is empty", errors)

  def test_reviewed_no_coverage_section_needs_gaps(self):
    def mutate(d):
      e = next(e for e in d["sections"] if e["section"] == "2.3")
      e["reviewed"] = True
      e["gaps"] = []
    errors = self._errors_for(mutate)
    self.assertIn("mapping: section 2.3 is reviewed with no units but lists no gaps", errors)

  def test_section_lanes_are_in_path_order(self):
    rows = section_lanes(self.mapping.entry("1.7"), self.course)
    names = [r.lane.name for r in rows]
    self.assertEqual(names, ["Grade 9", "Grade 11", "Algebraic Graphing"])
    for r in rows:
      orders = [lu.unit.order for lu in r.units]
      self.assertEqual(orders, sorted(orders), r.lane.name)

  def test_chapter_lanes_list_a_shared_unit_once(self):
    ch = next(c for c in self.book.chapters if c.id == "3")
    rows = chapter_lanes(ch, self.mapping, self.course)
    g11 = next(r for r in rows if r.lane.id == "g11")
    growth = [lu for lu in g11.units if lu.unit.name == "Exponential growth"]
    self.assertEqual(len(growth), 1)
    self.assertEqual(growth[0].sections, ("3.1", "3.5"))


if __name__ == "__main__":
  unittest.main()
