# Design

## Context

See proposal.md for motivation. The repository is empty apart from a README, so there is no existing code to fit. The data (chapter titles, unit names, mappings) is small, hand-curated, and reviewed by a person; the only automation needed is validation and rendering. This environment cannot reach duolingo.com or community-maintained unit lists, so the Duolingo inventory cannot be fetched programmatically. It is transcribed from the app as the user observes it: the user shares screenshots of the Grades view in chat, and only the names, grouping, and order are written down. Duolingo Math presents content as a tree per grade (grade, then the app's own grouping heading, then unit, then lesson), and the number of lessons is large, so the outputs need a view that shows, per textbook section, which lessons to follow in each grade.

## Goals / Non-Goals

**Goals:**
- Keep the three data files easy to edit by hand and easy to review in a diff.
- Record the Duolingo hierarchy (grade, unit, lesson) in the order the app shows it, so outputs can lay out per-grade lanes without any extra data.
- Expose loading and validation as an importable Python module so the spreadsheet and study-guide builders in later changes reuse it instead of re-parsing YAML.
- Fail loudly when a mapping references something that does not exist.

**Non-Goals:**
- Scraping or automating Duolingo. The inventory is observed by a person.
- Storing any textbook content beyond titles, page numbers, and bibliographic data.
- Supporting more than one textbook or one Duolingo course in this change. The file layout leaves room for it (catalogs are keyed by id) but nothing is built for it.
- A web UI. The Markdown index is a reference view; the student-facing deliverables (spreadsheet, PDF study guides) are separate changes.

## Decisions

- **YAML for all data files.** Alternatives: JSON, CSV. YAML allows comments (needed for provenance notes and the fair-use header), nests cleanly for chapter/section and section/unit lists, and diffs well. CSV cannot express per-section unit lists without multiple files.
- **Duolingo catalog nests grade, unit, lesson, in path order.** Alternatives: a flat unit list with a grade field (the original plan), or a separate lessons file. Nesting mirrors how the app and the user's screenshots are organized, so transcription is a straight copy, and the position of each unit and lesson is implicit in list order (an explicit `order` field is written anyway so that reordering is visible in a diff). Identifiers are short and stable: units `u-g<grade>-<nn>`, lessons `l-g<grade>-<nnn>`, assigned once and never renumbered when the app reorders content; the `order` fields change instead.
- **Mapping targets units, optionally narrowed to lessons.** A section lists units (the unit stays the thing that carries a coverage rating and note). When only some of a unit's lessons apply, the entry adds a `lessons:` list of lesson ids. Alternative: map directly to lessons; rejected because most sections will want whole units and lesson-level ratings would multiply review work by the lesson count.
- **Grade lanes are a rendered view, not stored data.** The index derives, for each section and for each chapter, one lane per contributing grade with that grade's recommended lessons in path order. In Markdown this is a table with grade as the first column; the study guides reuse the same derivation for their pairing block. Storing lanes would duplicate the catalog order and drift from it.
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
- [Partial inventory makes early outputs misleading] → the catalog's `complete: false` flag produces a prominent notice until the inventory is finished, and a unit with no lessons collected yet renders with a "lessons not yet collected" marker rather than an empty lane.
- [Lesson names are long and numerous, so lane tables get wide] → lanes list lesson names only, grouped under their unit name, and the chapter-level lane tags each lesson with its section ids instead of repeating lessons per section.

## Open Questions

- Which Duolingo platform (iOS, Android, web) should be the reference for unit names? Names are believed to be the same across platforms; the catalog records whichever was used.
- The Grades view (iOS, 2026-10-07) lists units directly under each grade with no intermediate heading, and shows a unit count per grade (recorded as `unit_count`). The optional `group` field on a unit is kept only in case the Topics tab reveals a grouping worth recording.
- Whether the progress tracker should track at lesson rather than unit level now that lessons are in the catalog. Decided in `progress-tracker-spreadsheet` once lesson counts are known.
