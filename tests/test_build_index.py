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
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from precalc_tutor import MAPPING_PATH
from precalc_tutor.catalog import load_duolingo, load_textbook
from precalc_tutor.index import render_index
from precalc_tutor.mapping import load_mapping
from tests.helpers import modified, write_temp_data

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "build_index.py"


def run_build(*args: str) -> subprocess.CompletedProcess:
  return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, cwd=ROOT)


class BuildIndexTest(unittest.TestCase):
  def test_render_contents(self):
    text = render_index(load_textbook(), load_duolingo(), load_mapping())
    self.assertIn("## Chapter 4: Trigonometry", text)
    ch4 = text.split("## Chapter 4: Trigonometry")[1].split("## Chapter 5")[0]
    for sid in ("4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.8"):
      self.assertIn(f"### {sid} ", ch4)
    self.assertIn("No Duolingo coverage for this section.", text)
    self.assertIn("| Grade 11 |", text)
    self.assertIn("## Sections with no Duolingo coverage", text)
    self.assertIn("Larson", text)
    self.assertIn("last verified", text)

  def test_no_coverage_count_matches_mapping(self):
    book, course, mapping = load_textbook(), load_duolingo(), load_mapping()
    text = render_index(book, course, mapping)
    zero = sum(1 for e in mapping.entries if not e.units)
    self.assertIn(f"{zero} of {len(book.sections())} sections have no mapped unit", text)

  def test_build_is_reproducible(self):
    out = Path(tempfile.mkdtemp()) / "index.md"
    self.assertEqual(run_build("--out", str(out)).returncode, 0)
    first = out.read_bytes()
    self.assertEqual(run_build("--out", str(out)).returncode, 0)
    self.assertEqual(first, out.read_bytes())

  def test_invalid_data_exits_nonzero_without_writing(self):
    def mutate(d):
      d["sections"][0]["units"][0]["unit"] = "u-g99-01"
    data = write_temp_data(mapping=modified(MAPPING_PATH, mutate))
    out = Path(tempfile.mkdtemp()) / "index.md"
    out.write_text("previous")
    proc = run_build("--textbook", str(data / "textbook" / "larson-precalculus-with-limits-2e.yaml"),
                     "--duolingo", str(data / "duolingo" / "math-course.yaml"),
                     "--mapping", str(data / "mappings" / MAPPING_PATH.name), "--out", str(out))
    self.assertEqual(proc.returncode, 1)
    self.assertIn("unknown unit 'u-g99-01'", proc.stderr)
    self.assertEqual(out.read_text(), "previous")

  def test_image_under_data_is_rejected(self):
    data = write_temp_data()
    (data / "textbook" / "page.png").write_bytes(b"\x89PNG")
    proc = run_build("--check", "--textbook", str(data / "textbook" / "larson-precalculus-with-limits-2e.yaml"),
                     "--duolingo", str(data / "duolingo" / "math-course.yaml"),
                     "--mapping", str(data / "mappings" / MAPPING_PATH.name))
    self.assertEqual(proc.returncode, 1)
    self.assertIn("image or scan file not allowed", proc.stderr)

  def test_committed_index_is_current(self):
    text = render_index(load_textbook(), load_duolingo(), load_mapping())
    self.assertEqual((ROOT / "docs" / "mapping-index.md").read_text(encoding="utf-8"), text)


if __name__ == "__main__":
  unittest.main()
