# Proposal

## Why

Students working through Larson's *Precalculus with Limits* (2nd ed.) often also practice on Duolingo Math, but the app's units are organized by grade and topic rather than by any textbook, so there is no easy way to know which Duolingo units to do before (or alongside) a given textbook section. A tutorial that maps textbook sections to Duolingo units, and is honest about where Duolingo has no coverage, lets a student or parent plan practice chapter by chapter.

## What Changes

- Store the textbook's structure (chapter and section titles with page numbers, plus a citation) as a machine-readable catalog. Titles and page numbers only; no textbook text, exercises, figures, or scans are ever stored.
- Store an inventory of Duolingo Math units (unit name, grade and topic grouping, and a one-line description of what the unit practices) as a machine-readable catalog.
- Store a reviewed mapping from each textbook section to zero or more Duolingo units, each with a coverage rating (full, partial, prerequisite-only) and a short note on what the unit does and does not cover relative to the section.
- Generate a human-readable tutorial (Markdown) from the three data files: a chapter-by-chapter study guide, a per-section lookup table, a list of textbook sections with no Duolingo coverage, and a citation block.
- Validate the data files so that every mapping references a real section and a real unit, and every section has an explicit entry (even if that entry is "no coverage").

## Capabilities

### New Capabilities
- `textbook-catalog`: The textbook structure data (chapters, sections, page numbers, citation) and the rules for what may be stored.
- `duolingo-catalog`: The Duolingo Math unit inventory data and its provenance (which app version or date it was observed from).
- `lesson-mapping`: The section-to-unit mapping data, its coverage ratings, and the referential integrity rules that validation enforces.
- `tutorial-rendering`: Generation of the student-facing tutorial document from the catalogs and mapping.

### Modified Capabilities
<!-- none: this is the project's first change -->

## Impact

- New files under `data/` (YAML catalogs and the mapping) and `docs/` (generated tutorial).
- A small build script (Python, standard library plus PyYAML) that validates the data and renders the tutorial.
- README gains usage and a fair-use / no-copyrighted-materials policy.
- No external services. Duolingo unit names are collected by observing the app; this environment cannot reach duolingo.com or community unit lists, so the inventory must be completed by a person with the app and is tracked as a task.
