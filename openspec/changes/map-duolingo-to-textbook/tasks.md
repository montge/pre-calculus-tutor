# Tasks

## 1. Project scaffolding

- [ ] 1.1 Add `requirements.txt` (PyYAML) and a `.gitignore` for Python artifacts; verify `pip install -r requirements.txt` succeeds and `git status` shows no `__pycache__`.
- [ ] 1.2 Add `data/README.md` stating the fair-use policy (titles and page numbers only, no textbook text, exercises, figures, or scans; no Duolingo screenshots) and the layout of the three data files; verify the policy text appears in the file.

## 2. Textbook catalog

- [ ] 2.1 Re-check `data/textbook/larson-precalculus-with-limits-2e.yaml` against the printed contents pages (iii-vi) for title and page-number typos; verify 12 chapters, 76 sections, Appendix A with 7 sections, Appendix B with 3 sections.
- [ ] 2.2 Confirm publisher, year, and ISBN from the book's copyright page and flip the `verified` flags; verify the YAML loads and the flags are true.
- [ ] 2.3 Write `tests/test_textbook_catalog.py` covering: expected counts, unique section ids, every section has a title and page; verify `python -m unittest` passes.

## 3. Duolingo catalog

- [ ] 3.1 Create `data/duolingo/math-course.yaml` with header fields (`last_verified`, `platform`, `complete: false`) and the nested layout `grades -> units -> lessons`, each unit with `id`, `order`, `name`, `group`, `description`, and `lessons` (each with `id`, `order`, `name`); seed it with the grade 9 through 12 units already known (polynomial arithmetic, polynomial function equations and graphs, sine, cosine, tangent ratios, connecting trigonometric ratios, sine, cosine, tangent functions) with empty lesson lists; verify the file loads and each unit has id, name, grade, order, description.
- [x] 3.2 Transcribe the Grades and Topics views from the user's screenshots, entering every unit name in displayed order; verify the unit count per grade and per topic matches the app's total (done 2026-10-07: grades 2 through 12, 663 units; eight topics, 157 units; `units_complete: true`). Screenshots are never committed.
- [ ] 3.2b Transcribe lessons within units, starting with grades 11 and 12 and the Algebraic Graphing and Geometry topics (the units the chapter 1 through 6 mapping draws on); verify each unit's lesson count matches the app and set `complete: true` once every mapped unit has its lessons.
- [ ] 3.3 Write `tests/test_duolingo_catalog.py` covering: required fields present, unit and lesson ids unique across the catalog, `order` values contiguous within each grade and unit, `last_verified` is a date; verify `python -m unittest` passes.

## 4. Lesson mapping

- [ ] 4.1 Create `data/mappings/larson-2e-to-duolingo.yaml` with one entry per textbook section (76 entries), each with `units: []`, `reviewed: false`, and an empty note; verify a count script reports 76 entries matching the catalog ids.
- [ ] 4.2 Fill in and review mappings for chapters 1 through 3 (functions, polynomials, exponentials and logarithms) with coverage ratings and notes, setting `reviewed: true` on each; verify every listed unit id exists in the Duolingo catalog.
- [ ] 4.3 Fill in and review mappings for chapters 4 through 6 (trigonometry) the same way; verify as in 4.2.
- [ ] 4.4 Mark chapters 7 through 12 and the appendices as no-coverage or unreviewed with a note per section; verify every section still has exactly one entry.
- [ ] 4.5 Write `tests/test_lesson_mapping.py` covering: every catalog section has an entry, no extra entries, ratings are one of the three values, all unit ids resolve, a dangling unit id fails with the section named, a `lessons:` list that names a lesson from another unit fails with section, unit, and lesson named; verify `python -m unittest` passes.

## 5. Shared loader and mapping index

- [ ] 5.1 Implement the `precalc_tutor/` package: `catalog.py`, `mapping.py`, and `validate.py` running all checks from groups 2 through 4 and returning every error found; verify a deliberately broken copy of the mapping yields the expected error list from `validate()`.
- [ ] 5.2 Implement `scripts/build_index.py` rendering the chapter-by-chapter index (section, page, ordered units with rating and note, draft marker for unreviewed sections, explicit "no Duolingo coverage" line) to `docs/mapping-index.md`, exiting non-zero without writing when validation fails; verify the output for chapter 4 lists its 8 sections in order and a broken mapping leaves `docs/` untouched.
- [ ] 5.3 Implement grade lanes in `precalc_tutor/lanes.py`: a function that, given a section entry, returns the contributing grades in ascending order and for each grade the recommended lessons in path order (all lessons of the unit unless narrowed), and a chapter-level merge that lists each lesson once tagged with its section ids; verify with a fixture where one lesson serves two sections that it appears once in the chapter lane with both ids.
- [ ] 5.4 Render the lanes in `build_index.py`: a per-section table (grade, unit, lessons) and a chapter-opening table, with a "lessons not yet collected" marker for units whose lesson list is empty; verify chapter 1's opening table has one row per contributing grade and the section tables omit non-contributing grades.
- [ ] 5.5 Implement the no-coverage summary, the incomplete-inventory notice, and the citation and verification-date footer; verify the summary count equals the number of zero-unit sections and the footer contains the book citation.
- [ ] 5.6 Make the build reproducible (sorted iteration, no timestamps in the body other than the data's own `last_verified`); verify two consecutive builds produce identical files via `diff`.
- [ ] 5.7 Write `tests/test_build_index.py` covering: valid data renders, lane tables match the lanes function, invalid data exits non-zero without writing, reproducibility; verify `python -m unittest` passes.
- [ ] 5.8 Update the top-level `README.md` with the project purpose, the build command, the data layout, the fair-use policy, and the dual-license summary, and add an Apache 2.0 header comment to each file under `precalc_tutor/`, `scripts/`, and `tests/`; verify the documented command runs as written and regenerates `docs/mapping-index.md`.

## 6. Integration check

- [ ] 6.1 Run the full build from a clean checkout and read `docs/mapping-index.md` end to end; verify every chapter appears with its grade-lane table, every section has either units with lanes or a no-coverage line, and the citation is present.

## Workflow follow-up

- Archive the change after the mapping index has been reviewed by the user.
- After archive, schedule a periodic re-verification of the Duolingo inventory (unit names change between releases).
