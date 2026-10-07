# Design

## Context

See proposal.md. Builds on the `precalc_tutor` loader and validator; this change adds only a renderer. Spreadsheet consumers are students on whatever they have: Excel, Google Sheets, LibreOffice, sometimes a phone.

## Goals / Non-Goals

**Goals:**
- A workbook that is useful on day one with zero setup, and still correct after the student fills it in.
- Formulas that survive a round trip through Google Sheets import.

**Non-Goals:**
- Syncing with the Duolingo account. The student marks units by hand.
- Per-lesson (sub-unit) tracking. The app does not name the nodes inside a unit, so the unit is the finest grain that can be tracked by name.
- Charts in the workbook. A percent column is enough; charts can be added later if wanted.

## Decisions

- **openpyxl to write `.xlsx`.** Alternatives: xlsxwriter (write-only, cannot be used by tests to read back), CSV (no dropdowns or formulas). openpyxl writes data validation, conditional formatting, and formulas, and the tests can reopen the file with the same library.
- **Three sheets: Tracker, Chapters, About.** One flat Tracker sheet rather than a sheet per chapter so autofilter and sorting work across the whole book and the summary formulas reference one range.
- **Summary formulas use `COUNTIFS` only.** `COUNTIFS` is supported identically by Excel, Google Sheets, and LibreOffice. No structured table references, no `LET`, no array formulas, since Google Sheets import and older Excel handle those inconsistently.
- **Status dropdown via a list data validation with the three literal values.** Simpler and more portable than a named range on a hidden sheet.
- **Item type column distinguishes "Read section" from "Duolingo unit".** This keeps chapter completion meaningful for chapters with no Duolingo coverage and lets a student filter to Duolingo rows only.
- **Reproducibility: fixed workbook properties (no creation timestamp), sorted iteration, and tests compare cell-level content rather than bytes.** openpyxl writes a timestamp into document properties by default; it is set to a constant so builds are stable.
- **Verification in LibreOffice headless when available, skipped otherwise.** Formula results cannot be computed by openpyxl; the portable check is to convert with `soffice --headless --convert-to xlsx` and read back cached values. CI installs LibreOffice; local tests skip when it is absent.

## Risks / Trade-offs

- [Google Sheets import drops some conditional formatting] → formatting is cosmetic; the dropdown and formulas are what matter and both survive import.
- [Students edit the generated file, then the mapping changes] → the About sheet records the mapping version (git commit) so a student can tell their copy is older; migration of a filled-in tracker is manual and out of scope.
- [Row count grows if the Duolingo inventory grows] → formulas use whole-column ranges on the Tracker sheet, so added rows are counted.

