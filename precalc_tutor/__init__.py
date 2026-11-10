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
"""Shared loader, validator, and lane derivation for the precalculus tutor data."""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TEXTBOOK_PATH = DATA_DIR / "textbook" / "larson-precalculus-with-limits-2e.yaml"
DUOLINGO_PATH = DATA_DIR / "duolingo" / "math-course.yaml"
MAPPING_PATH = DATA_DIR / "mappings" / "larson-2e-to-duolingo.yaml"
