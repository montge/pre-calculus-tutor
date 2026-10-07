# Proposal

## Why

Students working through Larson's *Precalculus with Limits* (2nd ed.) often also practice on Duolingo Math, but the app's units are organized by grade and topic rather than by any textbook, so there is no easy way to know which Duolingo units to do before (or alongside) a given textbook section. This change builds the data foundation: validated catalogs of the textbook sections and the Duolingo units, and a reviewed mapping between them. Two later changes consume it: `progress-tracker-spreadsheet` (a student tracking workbook) and `chapter-study-guides` (per-chapter LaTeX/PDF guides with sample problems, TI-84 steps, and common errors).

## What Changes

- Store the textbook's structure (chapter and section titles with page numbers, plus a citation) as a machine-readable catalog. Titles and page numbers only; no textbook text, exercises, figures, or scans are ever stored.
- Store an inventory of Duolingo Math content as a machine-readable catalog that mirrors the app's tree: each grade, its units in path order (with the app's grouping heading and a one-line description of what the unit practices), and each unit's lessons in order. Names are transcribed from the app; no screenshots are stored.
- Store a reviewed mapping from each textbook section to zero or more Duolingo units, each with a coverage rating (full, partial, prerequisite-only) and a short note on what the unit does and does not cover relative to the section. A unit may be narrowed to a subset of its lessons.
- Generate a Markdown mapping index from the three data files, readable on GitHub: sections in book order with their units, grade lanes for each chapter and section (one lane per grade listing the lessons to follow in path order), a list of textbook sections with no Duolingo coverage, and a citation block. It is the reference view the spreadsheet and study guides are checked against.
- Validate the data files so that every mapping references a real section and a real unit, and every section has an explicit entry (even if that entry is "no coverage").

## Capabilities

### New Capabilities
- `textbook-catalog`: The textbook structure data (chapters, sections, page numbers, citation) and the rules for what may be stored.
- `duolingo-catalog`: The Duolingo Math inventory (grade, unit, lesson hierarchy in app order) and its provenance (which platform and date it was observed from).
- `lesson-mapping`: The section-to-unit mapping data, its coverage ratings, and the referential integrity rules that validation enforces.
- `mapping-index`: Generation of the Markdown mapping index, including the grade-lane views, from the catalogs and mapping.

### Modified Capabilities
<!-- none: this is the project's first change -->

## Impact

- New files under `data/` (YAML catalogs and the mapping) and `docs/` (generated mapping index).
- A small Python package (`precalc_tutor/`) that loads and validates the data, shared by the later spreadsheet and study-guide builders, plus a `scripts/build_index.py` entry point.
- README gains usage and a fair-use / no-copyrighted-materials policy. The repository is dual licensed: Apache 2.0 for code, CC BY 4.0 for data and docs, with a NOTICE that textbook titles and Duolingo names are third-party material cited under fair use.
- No external services. Duolingo unit and lesson names are collected by observing the app; this environment cannot reach duolingo.com or community unit lists, so the inventory is transcribed from screenshots the user shares and is tracked as a task.
