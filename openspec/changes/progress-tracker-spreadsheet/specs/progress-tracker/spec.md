# Spec Delta

## Purpose

Gives students a downloadable workbook and a printable checklist to record progress through Duolingo units and textbook sections, chapter by chapter, in the order the units appear in the app, with summaries that update as they work.

## ADDED Requirements

### Requirement: By-section sheet lists one row per trackable item
The By section sheet SHALL contain one row per textbook section (item type "Read section") and one row per mapped Duolingo unit under that section (item type "Duolingo unit"), in book order, with chapter, section id, section title, page, item type, Duolingo grade and topic, unit name, coverage rating, status, date done, and notes columns.

#### Scenario: Section with two units
- **WHEN** section 4.3 maps to two Duolingo units
- **THEN** the By section sheet has three consecutive rows for 4.3: the section row followed by the two unit rows in recommended order

#### Scenario: Section with no units
- **WHEN** a section maps to no units
- **THEN** the By section sheet has exactly one row for it, of type "Read section", with the unit columns empty

### Requirement: By-lane sheet lists units in app order
The By lane sheet SHALL list, for each chapter that has mapped units, one block per contributing Duolingo grade or topic (grades ascending, then topics in app order), each block listing that lane's recommended units once, in the order the app presents them, with the unit's position in the app, its coverage rating, the textbook sections it serves, and the same status, date done, and notes columns as the By section sheet.

#### Scenario: Unit serving two sections appears once
- **WHEN** one grade 11 unit is recommended for sections 3.1 and 3.5
- **THEN** the chapter 3 Grade 11 block lists it once with "3.1, 3.5" in the sections column

#### Scenario: Order follows the app
- **WHEN** the mapping lists a grade 9 unit before another grade 9 unit that comes earlier in the app
- **THEN** the Grade 9 block lists them in app order

### Requirement: Printable checklist PDF
A PDF SHALL be generated from the same data with one part per chapter that has mapped units, each part opening with that chapter's textbook sections to read and then one block per lane in the same order and content as the By lane sheet, every line carrying an empty checkbox, and a footer with the textbook citation, the inventory verification date, and the license. Chapters start on a new page.

#### Scenario: Chapter page
- **WHEN** chapter 1 has units from Grade 9, Grade 11, and Algebraic Graphing
- **THEN** its part of the PDF has a textbook-sections block followed by three lane blocks, each line with a checkbox, unit name, rating, and section tags

#### Scenario: Reproducible PDF
- **WHEN** the build runs twice with no data changes
- **THEN** the two PDFs are byte-for-byte identical

### Requirement: Status is a constrained dropdown
The status column on both tracking sheets SHALL offer exactly the values "Not started", "In progress", and "Done" through data validation, defaulting to "Not started", and SHALL be color coded by conditional formatting.

#### Scenario: Invalid status rejected
- **WHEN** a user types a value other than the three allowed in a status cell in Excel or Google Sheets
- **THEN** the spreadsheet rejects the entry

### Requirement: Chapter summary uses live formulas
The Chapters sheet SHALL show, for each chapter, the number of items, the number marked Done, and the percent complete, computed by spreadsheet formulas from the By section sheet rather than by values written at build time.

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
The workbook and PDF SHALL be built by a single command that validates the data first, exits non-zero without writing on any validation error, and produces identical files on repeated runs over unchanged data.

#### Scenario: Reproducible build
- **WHEN** the build runs twice with no data changes
- **THEN** the two workbooks have identical cell contents, formulas, and validations
