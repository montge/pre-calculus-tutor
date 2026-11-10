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
"""Validate the data files and render docs/mapping-index.md.

Exits non-zero and leaves the previous index untouched if validation fails.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from precalc_tutor import DUOLINGO_PATH, MAPPING_PATH, TEXTBOOK_PATH  # noqa: E402
from precalc_tutor.catalog import load_duolingo, load_textbook  # noqa: E402
from precalc_tutor.index import render_index  # noqa: E402
from precalc_tutor.mapping import load_mapping  # noqa: E402
from precalc_tutor.validate import validate  # noqa: E402


def main(argv: list[str] | None = None) -> int:
  ap = argparse.ArgumentParser(description=__doc__)
  ap.add_argument("--textbook", type=Path, default=TEXTBOOK_PATH)
  ap.add_argument("--duolingo", type=Path, default=DUOLINGO_PATH)
  ap.add_argument("--mapping", type=Path, default=MAPPING_PATH)
  ap.add_argument("--out", type=Path, default=ROOT / "docs" / "mapping-index.md")
  ap.add_argument("--check", action="store_true", help="validate only; write nothing")
  args = ap.parse_args(argv)

  book = load_textbook(args.textbook)
  course = load_duolingo(args.duolingo)
  mapping = load_mapping(args.mapping)
  errors = validate(book, course, mapping, data_dir=args.textbook.parent.parent)
  if errors:
    for e in errors:
      print(f"error: {e}", file=sys.stderr)
    print(f"{len(errors)} validation error(s); index not written", file=sys.stderr)
    return 1
  if args.check:
    print("data valid")
    return 0

  text = render_index(book, course, mapping)
  args.out.parent.mkdir(parents=True, exist_ok=True)
  tmp = args.out.with_suffix(args.out.suffix + ".tmp")
  tmp.write_text(text, encoding="utf-8")
  os.replace(tmp, args.out)
  print(f"wrote {args.out}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
