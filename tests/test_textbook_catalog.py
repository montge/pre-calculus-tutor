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

from precalc_tutor.catalog import load_textbook
from precalc_tutor.validate import validate_textbook


class TextbookCatalogTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.book = load_textbook()

  def test_counts(self):
    numbered = [c for c in self.book.chapters if not c.is_appendix]
    appendices = {c.id: c for c in self.book.chapters if c.is_appendix}
    self.assertEqual(len(numbered), 12)
    self.assertEqual(sum(len(c.sections) for c in numbered), 76)
    self.assertEqual(len(appendices["A"].sections), 7)
    self.assertEqual(len(appendices["B"].sections), 3)

  def test_section_ids_unique_and_resolvable(self):
    ids = [s.id for s in self.book.sections()]
    self.assertEqual(len(ids), len(set(ids)))
    self.assertEqual(self.book.section("4.2").title, "Trigonometric Functions: The Unit Circle")

  def test_every_section_has_title_and_page(self):
    for s in self.book.sections():
      self.assertTrue(s.title, s.id)
      self.assertTrue(s.page, s.id)

  def test_validator_passes_on_real_data(self):
    self.assertEqual(validate_textbook(self.book), [])

  def test_citation(self):
    self.assertIn("Precalculus with Limits", self.book.citation())
    self.assertIn("2nd ed.", self.book.citation())


if __name__ == "__main__":
  unittest.main()
