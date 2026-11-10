#!/usr/bin/env python3
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
"""Validate the data and write one LaTeX checklist per mapped chapter to dist/checklists/, compiled to PDF.

Writes chapter-N.tex and, when pdflatex is installed, chapter-N.pdf. Exits non-zero and writes nothing if
validation fails or a chapter does not compile.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from precalc_tutor import DUOLINGO_PATH, MAPPING_PATH, TEXTBOOK_PATH  # noqa: E402
from precalc_tutor.catalog import load_duolingo, load_textbook  # noqa: E402
from precalc_tutor.checklist_tex import render_chapter  # noqa: E402
from precalc_tutor.lanes import mapped_chapters  # noqa: E402
from precalc_tutor.mapping import load_mapping  # noqa: E402
from precalc_tutor.validate import validate  # noqa: E402


def compile_tex(source: str, name: str) -> bytes:
  """Run pdflatex twice in a scratch directory and return the PDF bytes. Raises RuntimeError with the log on failure."""
  with tempfile.TemporaryDirectory() as tmp:
    tex_path = Path(tmp) / f"{name}.tex"
    tex_path.write_text(source, encoding="utf-8")
    env = dict(os.environ, SOURCE_DATE_EPOCH="0", FORCE_SOURCE_DATE="1")
    for _ in range(2):
      proc = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
                            cwd=tmp, env=env, capture_output=True, text=True)
      if proc.returncode != 0:
        log = (Path(tmp) / f"{name}.log")
        raise RuntimeError(log.read_text(errors="replace")[-2000:] if log.exists() else proc.stdout[-2000:])
    return (Path(tmp) / f"{name}.pdf").read_bytes()


def main(argv: list[str] | None = None) -> int:
  ap = argparse.ArgumentParser(description=__doc__)
  ap.add_argument("--textbook", type=Path, default=TEXTBOOK_PATH)
  ap.add_argument("--duolingo", type=Path, default=DUOLINGO_PATH)
  ap.add_argument("--mapping", type=Path, default=MAPPING_PATH)
  ap.add_argument("--out", type=Path, default=ROOT / "dist" / "checklists")
  ap.add_argument("--tex-only", action="store_true", help="write the .tex files without compiling")
  args = ap.parse_args(argv)

  book = load_textbook(args.textbook)
  course = load_duolingo(args.duolingo)
  mapping = load_mapping(args.mapping)
  errors = validate(book, course, mapping, data_dir=args.textbook.parent.parent)
  if errors:
    for e in errors:
      print(f"error: {e}", file=sys.stderr)
    print(f"{len(errors)} validation error(s); nothing written", file=sys.stderr)
    return 1

  compile_pdf = not args.tex_only
  if compile_pdf and shutil.which("pdflatex") is None:
    print("error: pdflatex not found; install TeX Live or pass --tex-only", file=sys.stderr)
    return 1

  outputs: dict[str, tuple[str, bytes | None]] = {}
  for ch in mapped_chapters(book, mapping):
    name = f"chapter-{ch.id}"
    source = render_chapter(book, course, mapping, ch.id)
    try:
      pdf = compile_tex(source, name) if compile_pdf else None
    except RuntimeError as exc:
      print(f"error: {name}.tex did not compile:\n{exc}", file=sys.stderr)
      return 1
    outputs[name] = (source, pdf)

  args.out.mkdir(parents=True, exist_ok=True)
  for name, (source, pdf) in outputs.items():
    (args.out / f"{name}.tex").write_text(source, encoding="utf-8")
    print(f"wrote {args.out / f'{name}.tex'}")
    if pdf is not None:
      tmp = args.out / f"{name}.pdf.tmp"
      tmp.write_bytes(pdf)
      os.replace(tmp, args.out / f"{name}.pdf")
      print(f"wrote {args.out / f'{name}.pdf'}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
