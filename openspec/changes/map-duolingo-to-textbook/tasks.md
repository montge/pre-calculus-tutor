# Tasks

## 1. Project scaffolding

- [x] 1.1 Add `requirements.txt` (PyYAML) and a `.gitignore` for Python artifacts; verify `pip install -r requirements.txt` succeeds and `git status` shows no `__pycache__`.
- [x] 1.2 Add `data/README.md` stating the fair-use policy (titles and page numbers only, no textbook text, exercises, figures, or scans; no Duolingo screenshots) and the layout of the three data files; verify the policy text appears in the file.

## 2. Textbook catalog

- [ ] 2.1 Re-check `data/textbook/larson-precalculus-with-limits-2e.yaml` against the printed contents pages (iii-vi) for title and page-number typos; verify 12 chapters, 76 sections, Appendix A with 7 sections, Appendix B with 3 sections.
- [ ] 2.2 Confirm publisher, year, and ISBN from the book's copyright page and flip the `verified` flags; verify the YAML loads and the flags are true.
- [x] 2.3 Write `tests/test_textbook_catalog.py` covering: expected counts, unique section ids, every section has a title and page; verify `python -m unittest` passes.

## 3. Duolingo catalog

- [x] 3.1 Create `data/duolingo/math-course.yaml` with header fields (`last_verified`, `platform`, `complete`) and the nested layout `grades -> units` and `topics -> units`, each unit with `id`, `order`, `name`, and optional `description`; verify the file loads and each unit has id, name, order.
- [x] 3.2 Transcribe the Grades and Topics views from the user's screenshots, entering every unit name in displayed order; verify the unit count per grade and per topic matches the app's total (done 2026-10-07: grades 2 through 12, 663 units; eight topics, 157 units; `complete: true`). Opening a unit shows only unnamed practice nodes, so there is no lesson level to transcribe. Screenshots are never committed.
- [x] 3.3 Write `tests/test_duolingo_catalog.py` covering: required fields present, unit ids unique across grades and topics, `order` values contiguous within each grade and topic, unit entry counts equal to `unit_count`, `last_verified` is a date; verify `python -m unittest` passes.

## 4. Lesson mapping

- [x] 4.1 Create `data/mappings/larson-2e-to-duolingo.yaml` with one entry per textbook section (76 numbered plus 10 appendix sections), each with `units: []`, `reviewed: false`, and an empty note; verify a count script reports 86 entries matching the catalog ids.
- [ ] 4.2 Fill in and review mappings for chapters 1 through 3 (functions, polynomials, exponentials and logarithms) with coverage ratings and notes, setting `reviewed: true` on each; verify every listed unit id exists in the Duolingo catalog. (Draft entered 2026-10-07 for all 22 sections, 171 unit references, all ids verified; awaiting the user's review before flipping `reviewed`.)
- [ ] 4.3 Fill in and review mappings for chapters 4 through 6 (trigonometry) the same way; verify as in 4.2.
- [ ] 4.4 Mark chapters 7 through 12 and the appendices as no-coverage or unreviewed with a note per section; verify every section still has exactly one entry.
- [x] 4.5 Write `tests/test_lesson_mapping.py` covering: every catalog section has an entry, no extra entries, ratings are one of the three values, all unit ids resolve, a dangling unit id fails with the section named; verify `python -m unittest` passes.

## 5. Shared loader and mapping index

- [x] 5.1 Implement the `precalc_tutor/` package: `catalog.py`, `mapping.py`, and `validate.py` running all checks from groups 2 through 4 and returning every error found; verify a deliberately broken copy of the mapping yields the expected error list from `validate()`.
- [x] 5.2 Implement `scripts/build_index.py` rendering the chapter-by-chapter index (section, page, ordered units with rating and note, draft marker for unreviewed sections, explicit "no Duolingo coverage" line) to `docs/mapping-index.md`, exiting non-zero without writing when validation fails; verify the output for chapter 4 lists its 8 sections in order and a broken mapping leaves `docs/` untouched.
- [x] 5.3 Implement lanes in `precalc_tutor/lanes.py`: a function that, given a section entry, returns the contributing grades (ascending) then topics (app order) and for each the recommended units in path order, and a chapter-level merge that lists each unit once tagged with its section ids; verify with a fixture where one unit serves two sections that it appears once in the chapter lane with both ids.
- [x] 5.4 Render the lanes in `build_index.py`: a per-section table (lane, units with ratings) and a chapter-opening table preceded by the chapter summary; verify chapter 1's opening table has one row per contributing grade or topic and the section tables omit non-contributing lanes.
- [x] 5.5 Implement the no-coverage summary, the incomplete-inventory notice, and the citation and verification-date footer; verify the summary count equals the number of zero-unit sections and the footer contains the book citation.
- [x] 5.6 Make the build reproducible (sorted iteration, no timestamps in the body other than the data's own `last_verified`); verify two consecutive builds produce identical files via `diff`.
- [x] 5.7 Write `tests/test_build_index.py` covering: valid data renders, lane tables match the lanes function, invalid data exits non-zero without writing, reproducibility; verify `python -m unittest` passes.
- [x] 5.8 Update the top-level `README.md` with the project purpose, the build command, the data layout, the fair-use policy, and the dual-license summary, and add an Apache 2.0 header comment to each file under `precalc_tutor/`, `scripts/`, and `tests/`; verify the documented command runs as written and regenerates `docs/mapping-index.md`.

## 6. Integration check

- [x] 6.1 Run the full build from a clean checkout and read `docs/mapping-index.md` end to end; verify every chapter appears with its grade-lane table, every section has either units with lanes or a no-coverage line, and the citation is present.

## Workflow follow-up

- Archive the change after the mapping index has been reviewed by the user.
- After archive, schedule a periodic re-verification of the Duolingo inventory (unit names change between releases).
