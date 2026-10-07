# Proposal

## Why

Students need a single place to record which Duolingo Math units they have finished for each textbook chapter and which textbook sections they have read. A spreadsheet works offline, opens in Excel, Google Sheets, and LibreOffice, and is something a parent or tutor can glance at. Building it from the reviewed mapping (see the `map-duolingo-to-textbook` change) keeps it consistent with the study guides.

## What Changes

- Generate a progress-tracking workbook from the catalogs and mapping: one row per trackable item (a textbook section to read, or a Duolingo unit to complete), grouped by chapter and section, with a status dropdown, a completion date, and a notes column.
- Add a per-chapter summary sheet whose completion counts and percentages are live spreadsheet formulas, so the summary updates as the student marks items done.
- Add an About sheet with the legend, the textbook citation, the Duolingo inventory verification date, and the license.
- Commit the generated workbook under `dist/` so students can download it without running anything.

## Capabilities

### New Capabilities
- `progress-tracker`: The generated tracking workbook: its sheets, columns, formulas, and portability guarantees.

### Modified Capabilities
<!-- none -->

## Impact

- Depends on the `precalc_tutor` loader and validator from `map-duolingo-to-textbook`; that change must be implemented first.
- New script `scripts/build_tracker.py`, new dependency `openpyxl`, new output `dist/progress-tracker.xlsx`.
- README gains the download link and a short "how to use the tracker" section.
