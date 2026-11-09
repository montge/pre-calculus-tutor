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
"""Validate the data files and write dist/progress-tracker.xlsx and dist/progress-checklist.pdf.

Exits non-zero and writes nothing if validation fails.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from precalc_tutor import DUOLINGO_PATH, MAPPING_PATH, TEXTBOOK_PATH  # noqa: E402
from precalc_tutor.catalog import load_duolingo, load_textbook  # noqa: E402
from precalc_tutor.checklist_pdf import build_pdf  # noqa: E402
from precalc_tutor.mapping import load_mapping  # noqa: E402
from precalc_tutor.tracker import build_workbook  # noqa: E402
from precalc_tutor.validate import validate  # noqa: E402


def mapping_version(path: Path) -> str:
  try:
    out = subprocess.run(["git", "log", "-1", "--format=%h", "--", str(path)], capture_output=True, text=True, cwd=ROOT, check=True).stdout.strip()
    return f"git {out}" if out else "unversioned"
  except (subprocess.CalledProcessError, FileNotFoundError):
    return "unversioned"


def _atomic_write(path: Path, data: bytes) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  tmp = path.with_suffix(path.suffix + ".tmp")
  tmp.write_bytes(data)
  os.replace(tmp, path)


def main(argv: list[str] | None = None) -> int:
  ap = argparse.ArgumentParser(description=__doc__)
  ap.add_argument("--textbook", type=Path, default=TEXTBOOK_PATH)
  ap.add_argument("--duolingo", type=Path, default=DUOLINGO_PATH)
  ap.add_argument("--mapping", type=Path, default=MAPPING_PATH)
  ap.add_argument("--xlsx", type=Path, default=ROOT / "dist" / "progress-tracker.xlsx")
  ap.add_argument("--pdf", type=Path, default=ROOT / "dist" / "progress-checklist.pdf")
  ap.add_argument("--version", default=None, help="mapping version string for the About sheet (default: git short hash)")
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

  version = args.version if args.version is not None else mapping_version(args.mapping)
  wb = build_workbook(book, course, mapping, mapping_version=version)
  import io
  xbuf = io.BytesIO()
  wb.save(xbuf)
  pdf = build_pdf(book, course, mapping)
  _atomic_write(args.xlsx, xbuf.getvalue())
  _atomic_write(args.pdf, pdf)
  print(f"wrote {args.xlsx}\nwrote {args.pdf}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
