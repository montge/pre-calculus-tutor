# Design

## Context

See proposal.md for motivation. The repository is empty apart from a README, so there is no existing code to fit. The data (chapter titles, unit names, mappings) is small, hand-curated, and reviewed by a person; the only automation needed is validation and rendering. This environment cannot reach duolingo.com or community-maintained unit lists, so the Duolingo inventory cannot be fetched programmatically and must be entered from the app.

## Goals / Non-Goals

**Goals:**
- Keep the three data files easy to edit by hand and easy to review in a diff.
- Expose loading and validation as an importable Python module so the spreadsheet and study-guide builders in later changes reuse it instead of re-parsing YAML.
- Fail loudly when a mapping references something that does not exist.

**Non-Goals:**
- Scraping or automating Duolingo. The inventory is observed by a person.
- Storing any textbook content beyond titles, page numbers, and bibliographic data.
- Supporting more than one textbook or one Duolingo course in this change. The file layout leaves room for it (catalogs are keyed by id) but nothing is built for it.
- A web UI. The Markdown index is a reference view; the student-facing deliverables (spreadsheet, PDF study guides) are separate changes.

## Decisions

- **YAML for all data files.** Alternatives: JSON, CSV. YAML allows comments (needed for provenance notes and the fair-use header), nests cleanly for chapter/section and section/unit lists, and diffs well. CSV cannot express per-section unit lists without multiple files.
- **One mapping file keyed by textbook section, not by Duolingo unit.** The outputs are read in textbook order, and the "every section has an entry" rule is easiest to enforce when the section is the key. A reverse index (unit to sections) is derived at render time if needed.
- **Three coverage ratings: `full`, `partial`, `prerequisite`.** Alternatives: a numeric score, or free text. Three named levels are enough for a student to decide "do this before", "do this instead of some practice", or "this is just a warm-up", and are easy to validate.
- **Python 3 with PyYAML, standard library otherwise.** A small package `precalc_tutor/` with `catalog.py` (load textbook and Duolingo catalogs), `mapping.py` (load mapping), `validate.py` (all integrity checks, returning a list of errors), and `scripts/build_index.py` as the entry point. Alternatives: Node, a static-site generator. Python is already present, openpyxl (for the later spreadsheet) is Python, and the LaTeX generator will be Python too, so one language keeps the toolchain small. No templating library: f-strings are sufficient for this size.
- **Validate then render, writing to a temp path and renaming on success.** This gives the "build never overwrites with invalid data" behavior without a separate validate command. Later builders call the same `validate` function first.
- **Tests as plain `unittest` cases in `tests/` run via `python -m unittest`.** Keeps the dependency surface at PyYAML only.
- **Mapping entries are keyed by section but may also carry a `chapter_summary` note.** The spreadsheet and study guides group by chapter; a chapter-level note (for example "Duolingo has nothing for this chapter; use the book") avoids repeating it on every section.
- **Draft mapping is shipped in this change for chapters 1 through 6 only.** Those are the chapters where Duolingo Math is known to have related units (functions, polynomials, exponentials, trigonometry). Chapters 7 through 12 get explicit no-coverage or unreviewed entries so validation passes, and are filled in once the unit inventory is complete.

## Risks / Trade-offs

- [Duolingo unit names and groupings change between app releases] → the catalog records a last-verified date and platform, and the generated outputs print it; re-verification is a periodic task, not a code change.
- [Mapping quality depends on one person's judgment] → every entry carries a `reviewed` flag and a note; generated outputs label unreviewed entries as draft.
- [Transcription errors in the textbook catalog] → the catalog header names the source pages (contents pp. iii-vi); a task re-checks the file against the book.
- [Fair-use scope creep: someone adds textbook exercises "for convenience"] → the spec forbids it, the README states the policy, and the validator rejects image files under `data/`.
- [Partial inventory makes early outputs misleading] → the catalog's `complete: false` flag produces a prominent notice until the inventory is finished.

## Open Questions

- Which Duolingo platform (iOS, Android, web) should be the reference for unit names? Names are believed to be the same across platforms; the catalog records whichever was used.
