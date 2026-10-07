# Tasks

## 1. Scaffolding

- [ ] 1.1 Add `openpyxl` to `requirements.txt` and create `scripts/build_tracker.py` that imports the `precalc_tutor` loader and validator and exits non-zero on validation errors; verify a broken mapping copy makes the script exit non-zero without creating `dist/progress-tracker.xlsx`.

## 2. Tracker sheet

- [ ] 2.1 Implement row generation (section rows and unit rows in book order with all columns from the spec) and write the Tracker sheet with a frozen header row and autofilter; verify with a test that section 4.3's rows are consecutive and in recommended order and that a no-unit section yields exactly one row.
- [ ] 2.2 Add the status data validation (three values, default "Not started") and conditional formatting per status; verify by reopening the file with openpyxl that the validation formula lists exactly the three values and applies to the whole status column.

## 3. Chapters and About sheets

- [ ] 3.1 Implement the Chapters sheet with per-chapter item count, Done count (`COUNTIFS` over the Tracker chapter and status columns), and percent formulas; verify the formula strings reference the Tracker columns and that a LibreOffice headless recalculation (skipped if `soffice` is absent) shows zero Done on a fresh workbook.
- [ ] 3.2 Implement the About sheet with legend, citation, last-verified date, incomplete-inventory notice when applicable, mapping git commit, and license; verify the sheet contains the textbook title and author.

## 4. Reproducibility and docs

- [ ] 4.1 Pin workbook document properties to constants and sort all iteration; verify two consecutive builds produce workbooks whose cells, formulas, and validations compare equal in a test.
- [ ] 4.2 Write `tests/test_build_tracker.py` covering groups 2 through 4; verify `python -m unittest` passes.
- [ ] 4.3 Commit `dist/progress-tracker.xlsx` and add a "Track your progress" section to `README.md` with the download link and the status legend; verify the link resolves in the repository.

## 5. Integration check

- [ ] 5.1 Open the generated workbook in Google Sheets (import) and confirm the dropdown works and the Chapters percentages update when a row is marked Done; record the result in the task notes.
