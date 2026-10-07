# Spec Delta

## Purpose

Produces a Markdown index of the section-to-unit mapping, readable directly on GitHub, so the reviewed data has a human-readable view that other deliverables (spreadsheet, study guides) can be checked against. The index shows each section's recommendations both as a list and as grade lanes, so a student can see, grade by grade, which lessons to follow for that section.

## ADDED Requirements

### Requirement: Index is generated from data
The mapping index SHALL be produced by a single command from the textbook catalog, the Duolingo catalog, and the mapping, and running the command twice on unchanged data SHALL produce identical output.

#### Scenario: Reproducible build
- **WHEN** the build command runs twice with no data changes
- **THEN** the generated file is byte-for-byte identical

#### Scenario: Build refuses invalid data
- **WHEN** any data file fails validation
- **THEN** the build exits non-zero, prints each validation error, and does not overwrite the previous index

### Requirement: Index lists sections in book order with their units
The index SHALL present, for each chapter in book order, each section with its page number and the mapped Duolingo units in recommended order, with each unit's coverage rating and note, and SHALL mark unreviewed sections as draft.

#### Scenario: Section with units
- **WHEN** a section maps to two units
- **THEN** the index lists both under that section with their ratings, prerequisites first

#### Scenario: Section without units
- **WHEN** a section maps to no units
- **THEN** the index says so explicitly under that section

### Requirement: Index shows grade lanes per section
For each section with at least one mapped unit, the index SHALL render a grade-lane table: one row (lane) per grade that contributes a unit, in ascending grade order, listing in that lane the recommended lessons in path order, each labeled with its unit name. Grades that contribute nothing to the section SHALL be omitted from that section's table.

#### Scenario: Section drawing on two grades
- **WHEN** section 2.2 maps to one grade 10 unit and one grade 11 unit
- **THEN** its table has a grade 10 lane and a grade 11 lane, each listing that grade's recommended lessons in path order under the unit name

#### Scenario: Narrowed unit
- **WHEN** a mapped unit is narrowed to three of its lessons
- **THEN** the lane lists only those three lessons

#### Scenario: Unit with no lessons collected yet
- **WHEN** a mapped unit has an empty lesson list in the catalog
- **THEN** the lane shows the unit name with a "lessons not yet collected" marker

### Requirement: Index shows a chapter-level grade-lane summary
Each chapter SHALL open with a grade-lane table that merges its sections' lanes: one lane per contributing grade, listing that grade's recommended lessons in path order and tagging each lesson with the section(s) it serves, so a student working a whole chapter can follow one grade's path from top to bottom.

#### Scenario: Lesson serving two sections
- **WHEN** one lesson is recommended for sections 1.4 and 1.5
- **THEN** the chapter lane lists it once, tagged with both section ids

### Requirement: Index includes a no-coverage summary
The index SHALL include one consolidated list of every textbook section that has no Duolingo unit.

#### Scenario: Summary matches mapping
- **WHEN** the mapping has N sections with zero units
- **THEN** the no-coverage list has exactly N entries

### Requirement: Index cites its sources
The index SHALL end with the textbook citation and the date the Duolingo inventory was last verified, and SHALL state that no textbook or Duolingo content is reproduced.

#### Scenario: Citation present
- **WHEN** the index is generated
- **THEN** its final section contains the citation and the verification date
