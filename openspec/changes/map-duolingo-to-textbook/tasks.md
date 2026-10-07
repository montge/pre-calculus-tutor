# Tasks

## 1. Project scaffolding

- [ ] 1.1 Add `requirements.txt` (PyYAML) and a `.gitignore` for Python artifacts; verify `pip install -r requirements.txt` succeeds and `git status` shows no `__pycache__`.
- [ ] 1.2 Add `data/README.md` stating the fair-use policy (titles and page numbers only, no textbook text, exercises, figures, or scans; no Duolingo screenshots) and the layout of the three data files; verify the policy text appears in the file.

## 2. Textbook catalog

- [ ] 2.1 Re-check `data/textbook/larson-precalculus-with-limits-2e.yaml` against the printed contents pages (iii-vi) for title and page-number typos; verify 12 chapters, 76 sections, Appendix A with 7 sections, Appendix B with 3 sections.
- [ ] 2.2 Confirm publisher, year, and ISBN from the book's copyright page and flip the `verified` flags; verify the YAML loads and the flags are true.
- [ ] 2.3 Write `tests/test_textbook_catalog.py` covering: expected counts, unique section ids, every section has a title and page; verify `python -m unittest` passes.

## 3. Duolingo catalog

- [ ] 3.1 Create `data/duolingo/math-course.yaml` with header fields (`last_verified`, `platform`, `complete: false`) and the grade 9 through 12 units that are already known (polynomial arithmetic, polynomial function equations and graphs, sine, cosine, tangent ratios, connecting trigonometric ratios, sine, cosine, tangent functions); verify the file loads and each unit has id, name, grade, description.
- [ ] 3.2 Walk the Duolingo Math app (Grades view, grades 9 through 12, and the Graphing and Algebraic Graphing topics) and enter every unit name with its grade and topic; verify the count matches the app's displayed unit counts for those grades and set `complete: true`.
- [ ] 3.3 Write `tests/test_duolingo_catalog.py` covering: required fields present, unique ids, `last_verified` is a date; verify `python -m unittest` passes.

## 4. Lesson mapping

- [ ] 4.1 Create `data/mappings/larson-2e-to-duolingo.yaml` with one entry per textbook section (76 entries), each with `units: []`, `reviewed: false`, and an empty note; verify a count script reports 76 entries matching the catalog ids.
- [ ] 4.2 Fill in and review mappings for chapters 1 through 3 (functions, polynomials, exponentials and logarithms) with coverage ratings and notes, setting `reviewed: true` on each; verify every listed unit id exists in the Duolingo catalog.
- [ ] 4.3 Fill in and review mappings for chapters 4 through 6 (trigonometry) the same way; verify as in 4.2.
- [ ] 4.4 Mark chapters 7 through 12 and the appendices as no-coverage or unreviewed with a note per section; verify every section still has exactly one entry.
- [ ] 4.5 Write `tests/test_lesson_mapping.py` covering: every catalog section has an entry, no extra entries, ratings are one of the three values, all unit ids resolve, a dangling unit id fails with the section named; verify `python -m unittest` passes.

## 5. Tutorial rendering

- [ ] 5.1 Implement `scripts/build_tutorial.py` loading the three files and running all validations from groups 2 through 4, exiting non-zero with every error listed on failure; verify a deliberately broken copy of the mapping produces the expected error and leaves `docs/` untouched.
- [ ] 5.2 Implement rendering of the chapter-by-chapter guide (section, page, ordered units with rating and note, draft marker for unreviewed sections, explicit "no Duolingo coverage" line) to `docs/tutorial.md`; verify the output for chapter 4 lists its 8 sections in order.
- [ ] 5.3 Implement the no-coverage summary, the incomplete-inventory notice, and the citation and verification-date footer; verify the summary count equals the number of zero-unit sections and the footer contains the book citation.
- [ ] 5.4 Make the build reproducible (sorted iteration, no timestamps in the body other than the data's own `last_verified`); verify two consecutive builds produce identical files via `diff`.
- [ ] 5.5 Write `tests/test_build_tutorial.py` covering: valid data renders, invalid data exits non-zero without writing, reproducibility; verify `python -m unittest` passes.
- [ ] 5.6 Update the top-level `README.md` with the project purpose, the build command, the data layout, the fair-use policy, and the dual-license summary, and add an Apache 2.0 header comment to each file under `scripts/` and `tests/`; verify the documented command runs as written and regenerates `docs/tutorial.md`.

## 6. Integration check

- [ ] 6.1 Run the full build from a clean checkout and read `docs/tutorial.md` end to end; verify every chapter appears, every section has either units or a no-coverage line, and the citation is present.

## Workflow follow-up

- Archive the change after the tutorial has been reviewed by the user.
- After archive, schedule a periodic re-verification of the Duolingo inventory (unit names change between releases).
