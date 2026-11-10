# Proposal

## Why

Students need a single place to record which Duolingo Math units they have finished for each textbook chapter and which textbook sections they have read. The mapping index is a reference view organised by textbook section; what a student needs while working is a checklist in the order the units appear in Duolingo, so they can walk one grade's path and tick units off, and a printable version of the same checklist for people who prefer paper. A spreadsheet works offline, opens in Excel, Google Sheets, and LibreOffice, and is something a parent or tutor can glance at. Building it from the reviewed mapping (see the `map-duolingo-to-textbook` change) keeps it consistent with the study guides.

## What Changes

- Generate a progress-tracking workbook from the catalogs and mapping with two tracking sheets: **By section** (one row per trackable item, a textbook section to read or a Duolingo unit to complete, in book order) and **By lane** (the same units grouped by chapter and then by Duolingo grade or topic, in the order the app presents them, each tagged with the sections it serves). Both have a status dropdown, a completion date, and a notes column.
- Generate a printable checklist PDF from the same data: one part per chapter, opening with the chapter's textbook sections and then one block per lane listing units in app order with a checkbox each.
- Add a per-chapter summary sheet whose completion counts and percentages are live spreadsheet formulas, so the summary updates as the student marks items done.
- Add an About sheet with the legend, the textbook citation, the Duolingo inventory verification date, and the license.
- Commit the generated workbook and PDF under `dist/` so students can download them without running anything.

## Capabilities

### New Capabilities
- `progress-tracker`: The generated tracking workbook (its sheets, columns, formulas, and portability guarantees) and the printable checklist PDF.

### Modified Capabilities
<!-- none -->

## Impact

- Depends on the `precalc_tutor` loader and validator from `map-duolingo-to-textbook`; that change must be implemented first.
- New script `scripts/build_tracker.py`, new dependencies `openpyxl` and `reportlab`, new outputs `dist/progress-tracker.xlsx` and `dist/progress-checklist.pdf`.
- README gains the download link and a short "how to use the tracker" section.
