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
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from precalc_tutor import MAPPING_PATH
from precalc_tutor.catalog import load_duolingo, load_textbook
from precalc_tutor.checklist_tex import render_chapter, tex
from precalc_tutor.lanes import mapped_chapters
from precalc_tutor.mapping import load_mapping
from tests.helpers import modified, write_temp_data

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "build_checklists.py"
OUT = ROOT / "dist" / "checklists"
HAS_PDFLATEX = shutil.which("pdflatex") is not None


def pdf_text(data: bytes) -> str:
  from pypdf import PdfReader
  return " ".join(" ".join(p.extract_text() for p in PdfReader(io.BytesIO(data)).pages).split())


class ChecklistTexTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.book, cls.course, cls.mapping = load_textbook(), load_duolingo(), load_mapping()

  def test_escape(self):
    self.assertEqual(tex("A e^{kt} & 5% #1_x ~ \\"), r"A e\textasciicircum{}\{kt\} \& 5\% \#1\_x \textasciitilde{} \textbackslash{}")

  def test_render_is_deterministic_and_complete(self):
    one = render_chapter(self.book, self.course, self.mapping, "3")
    self.assertEqual(one, render_chapter(self.book, self.course, self.mapping, "3"))
    for needle in (r"\section{1.\quad Read the textbook sections}", r"\section{2.\quad Practise on Duolingo}",
                   r"\section{3.\quad Section by section}", r"\section{4.\quad Finish the chapter}",
                   r"\subsection{Grade 11}", "Logistic growth models", "Cumulative Test for Chapters 1-3"):
      self.assertIn(needle, one)
    self.assertNotIn("Draft.", one)  # chapter 3 is reviewed

  def test_unreviewed_chapter_shows_draft_notice(self):
    data = write_temp_data(mapping=modified(MAPPING_PATH, lambda d: [e.update(reviewed=False) for e in d["sections"]]))
    mapping = load_mapping(data / "mappings" / MAPPING_PATH.name)
    self.assertIn(r"\textbf{Draft.}", render_chapter(self.book, self.course, mapping, "3"))

  def test_committed_checklists_are_current(self):
    ids = [c.id for c in mapped_chapters(self.book, self.mapping)]
    self.assertEqual(sorted(p.name for p in OUT.glob("chapter-*.tex")), sorted(f"chapter-{i}.tex" for i in ids))
    self.assertEqual(sorted(p.name for p in OUT.glob("chapter-*.pdf")), sorted(f"chapter-{i}.pdf" for i in ids))
    for cid in ids:
      self.assertEqual((OUT / f"chapter-{cid}.tex").read_text(encoding="utf-8"),
                       render_chapter(self.book, self.course, self.mapping, cid), cid)

  @unittest.skipUnless(HAS_PDFLATEX, "pdflatex not installed")
  def test_compiles_reproducibly_and_matches_committed_pdf(self):
    sys.path.insert(0, str(ROOT / "scripts"))
    from build_checklists import compile_tex
    source = render_chapter(self.book, self.course, self.mapping, "3")
    first = compile_tex(source, "chapter-3")
    self.assertEqual(first, compile_tex(source, "chapter-3"))
    text = pdf_text(first)
    self.assertIn("Chapter 3 Checklist", text)
    self.assertIn("Logistic growth models", text)
    self.assertEqual(text, pdf_text((OUT / "chapter-3.pdf").read_bytes()))

  def test_script_refuses_invalid_data(self):
    def mutate(d):
      d["sections"][0]["units"][0]["unit"] = "u-g99-01"
    data = write_temp_data(mapping=modified(MAPPING_PATH, mutate))
    out = Path(tempfile.mkdtemp()) / "out"
    proc = subprocess.run([sys.executable, str(SCRIPT), "--tex-only", "--out", str(out),
                           "--textbook", str(data / "textbook" / "larson-precalculus-with-limits-2e.yaml"),
                           "--duolingo", str(data / "duolingo" / "math-course.yaml"),
                           "--mapping", str(data / "mappings" / MAPPING_PATH.name)], capture_output=True, text=True, cwd=ROOT)
    self.assertEqual(proc.returncode, 1)
    self.assertIn("unknown unit", proc.stderr)
    self.assertFalse(out.exists())


if __name__ == "__main__":
  unittest.main()
