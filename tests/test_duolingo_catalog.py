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

from precalc_tutor import DUOLINGO_PATH
from precalc_tutor.catalog import load_duolingo
from precalc_tutor.validate import validate_duolingo
from tests.helpers import modified, write_temp_data


class DuolingoCatalogTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.course = load_duolingo()

  def test_required_fields(self):
    self.assertTrue(self.course.last_verified)
    self.assertTrue(self.course.platform)
    for u in self.course.units():
      self.assertTrue(u.id and u.name and u.order >= 1 and u.lane, u)

  def test_ids_unique_across_grades_and_topics(self):
    ids = [u.id for u in self.course.units()]
    self.assertEqual(len(ids), len(set(ids)))

  def test_counts_match_app_totals(self):
    for lane in self.course.lanes:
      self.assertEqual(len(lane.units), lane.unit_count, lane.name)
    grades = [l for l in self.course.lanes if l.kind == "grade"]
    topics = [l for l in self.course.lanes if l.kind == "topic"]
    self.assertEqual([l.rank for l in grades], list(range(2, 13)))
    self.assertEqual(len(topics), 8)
    self.assertEqual(len(self.course.units()), 820)

  def test_same_name_in_several_grades_is_distinct(self):
    hits = [u for u in self.course.units() if u.name == "Equivalent fractions"]
    self.assertGreaterEqual(len(hits), 3)
    self.assertEqual(len({u.id for u in hits}), len(hits))

  def test_validator_passes_on_real_data(self):
    self.assertEqual(validate_duolingo(self.course), [])

  def test_missing_name_reaches_validator(self):
    def mutate(doc):
      del doc["grades"][0]["units"][0]["name"]
    data = write_temp_data(duolingo=modified(DUOLINGO_PATH, mutate))
    errors = validate_duolingo(load_duolingo(data / "duolingo" / DUOLINGO_PATH.name))
    self.assertTrue(any("unit u-g2-01 in Grade 2 has no name" in e for e in errors), errors)

  def test_validator_reports_count_mismatch_and_bad_date(self):
    def mutate(doc):
      doc["last_verified"] = "yesterday"
      doc["grades"][0]["units"].pop()
    data = write_temp_data(duolingo=modified(DUOLINGO_PATH, mutate))
    errors = validate_duolingo(load_duolingo(data / "duolingo" / DUOLINGO_PATH.name))
    self.assertTrue(any("not an ISO date" in e for e in errors), errors)
    self.assertTrue(any("Grade 2 lists 6 units but unit_count is 7" in e for e in errors), errors)


if __name__ == "__main__":
  unittest.main()
