# Tasks

## 1. Scaffolding

- [x] 1.1 Add `openpyxl` and `reportlab` to `requirements.txt` and create `scripts/build_tracker.py` that imports the `precalc_tutor` loader and validator and exits non-zero on validation errors; verify a broken mapping copy makes the script exit non-zero without creating `dist/progress-tracker.xlsx` or `dist/progress-checklist.pdf`.

## 2. Tracking sheets

- [x] 2.1 Implement row generation (section rows and unit rows in book order with all columns from the spec) and write the By section sheet with a frozen header row and autofilter; verify with a test that section 4.3's rows are consecutive and in recommended order and that a no-unit section yields exactly one row.
- [x] 2.2 Add the status data validation (three values, default "Not started") and conditional formatting per status to both tracking sheets; verify by reopening the file with openpyxl that the validation formula lists exactly the three values and applies to the whole status column on each sheet.
- [x] 2.3 Implement the By lane sheet from `precalc_tutor.lanes.chapter_lanes`: chapter, lane, unit position, unit, rating, sections served, status, date, notes, in chapter then lane rank then app order; verify a unit serving two sections appears once with both section ids and that each lane block is in ascending app order.

## 3. Chapters and About sheets

- [x] 3.1 Implement the Chapters sheet with per-chapter item count, Done count (`COUNTIFS` over the By section chapter and status columns), and percent formulas; verify the formula strings reference the Tracker columns and that a LibreOffice headless recalculation (skipped if `soffice` is absent) shows zero Done on a fresh workbook.
- [x] 3.2 Implement the About sheet with legend, citation, last-verified date, incomplete-inventory notice when applicable, mapping git commit, and license; verify the sheet contains the textbook title and author.

## 4. Printable checklist

- [x] 4.1 Implement `precalc_tutor/checklist_pdf.py` with reportlab in invariant mode: one part per mapped chapter starting on a new page, a textbook-sections block, then lane blocks with a bordered empty checkbox cell, unit name, rating, and section tags, and a footer with citation, verification date, and license; verify the PDF text contains each mapped chapter title and that two builds are byte-identical.

## 5. Reproducibility and docs

- [x] 5.1 Pin workbook document properties to constants and sort all iteration; verify two consecutive builds produce workbooks whose cells, formulas, and validations compare equal in a test.
- [x] 5.2 Write `tests/test_build_tracker.py` covering groups 2 through 5; verify `python -m unittest` passes.
- [x] 5.3 Commit `dist/progress-tracker.xlsx` and `dist/progress-checklist.pdf` and add a "Track your progress" section to `README.md` with the download links and the status legend; verify the links resolve in the repository.

## 6. Integration check

- [ ] 6.1 (User) Open the generated workbook in Google Sheets (import) and confirm the dropdown works and the Chapters percentages update when a row is marked Done; record the result in the task notes.
