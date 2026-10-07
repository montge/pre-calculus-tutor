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
"""Shared helpers: load the real data once, and build broken copies for negative tests."""

from __future__ import annotations

import copy
import tempfile
from pathlib import Path

import yaml

from precalc_tutor import DUOLINGO_PATH, MAPPING_PATH, TEXTBOOK_PATH


def raw(path: Path) -> dict:
  return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_temp_data(textbook: dict | None = None, duolingo: dict | None = None, mapping: dict | None = None) -> Path:
  """Write a temp data/ tree from the given (possibly modified) raw documents; returns the data dir."""
  root = Path(tempfile.mkdtemp(prefix="precalc-data-"))
  for sub, doc, src in (("textbook", textbook, TEXTBOOK_PATH), ("duolingo", duolingo, DUOLINGO_PATH), ("mappings", mapping, MAPPING_PATH)):
    (root / sub).mkdir()
    (root / sub / src.name).write_text(yaml.safe_dump(doc if doc is not None else raw(src), sort_keys=False), encoding="utf-8")
  return root


def modified(path: Path, mutate) -> dict:
  doc = copy.deepcopy(raw(path))
  mutate(doc)
  return doc
