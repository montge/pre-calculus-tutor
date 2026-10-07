# Spec Delta

## Purpose

Gives students a downloadable workbook to record progress through Duolingo units and textbook sections, chapter by chapter, with summaries that update as they work.

## ADDED Requirements

### Requirement: Tracker lists one row per trackable item
The Tracker sheet SHALL contain one row per textbook section (item type "Read section") and one row per mapped Duolingo unit under that section (item type "Duolingo unit"), in book order, with chapter, section id, section title, page, item type, Duolingo grade and topic, unit name, coverage rating, status, date done, and notes columns.

#### Scenario: Section with two units
- **WHEN** section 4.3 maps to two Duolingo units
- **THEN** the Tracker has three consecutive rows for 4.3: the section row followed by the two unit rows in recommended order

#### Scenario: Section with no units
- **WHEN** a section maps to no units
- **THEN** the Tracker has exactly one row for it, of type "Read section", with the unit columns empty

### Requirement: Status is a constrained dropdown
The status column SHALL offer exactly the values "Not started", "In progress", and "Done" through data validation, defaulting to "Not started", and SHALL be color coded by conditional formatting.

#### Scenario: Invalid status rejected
- **WHEN** a user types a value other than the three allowed in a status cell in Excel or Google Sheets
- **THEN** the spreadsheet rejects the entry

### Requirement: Chapter summary uses live formulas
The Chapters sheet SHALL show, for each chapter, the number of items, the number marked Done, and the percent complete, computed by spreadsheet formulas from the Tracker sheet rather than by values written at build time.

#### Scenario: Marking an item done updates the summary
- **WHEN** a student changes one chapter 2 item from "Not started" to "Done"
- **THEN** the chapter 2 Done count and percent on the Chapters sheet increase without any rebuild

### Requirement: Workbook is portable
The workbook MUST open without repair prompts in Microsoft Excel, Google Sheets, and LibreOffice Calc, using only formulas supported by all three.

#### Scenario: Opens in LibreOffice headless
- **WHEN** the workbook is converted by LibreOffice in headless mode
- **THEN** conversion succeeds and the recalculated Chapters sheet shows zero Done for a fresh workbook

### Requirement: About sheet carries provenance
The About sheet SHALL contain the status legend, the textbook citation, the Duolingo inventory verification date, the incomplete-inventory notice when applicable, and the content license.

#### Scenario: Provenance present
- **WHEN** the workbook is generated
- **THEN** the About sheet names the textbook, edition, and author and shows the last-verified date

### Requirement: Build is reproducible and validated
The workbook SHALL be built by a single command that validates the data first, exits non-zero without writing on any validation error, and produces an identical file on repeated runs over unchanged data.

#### Scenario: Reproducible build
- **WHEN** the build runs twice with no data changes
- **THEN** the two workbooks have identical cell contents, formulas, and validations
