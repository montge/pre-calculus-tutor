# Spec Delta

## Purpose

Produces a Markdown index of the section-to-unit mapping, readable directly on GitHub, so the reviewed data has a human-readable view that other deliverables (spreadsheet, study guides) can be checked against. The index shows each section's recommendations both as a list and as lanes, one per grade or topic, so a student can see, lane by lane, which units to follow for that section.

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

### Requirement: Index shows lanes per section
For each section with at least one mapped unit, the index SHALL render a lane table: one row (lane) per grade or topic that contributes a unit, grades first in ascending order and then topics in app order, listing in that lane the recommended units in the app's path order with their ratings. Grades and topics that contribute nothing to the section SHALL be omitted from that section's table.

#### Scenario: Section drawing on two grades and a topic
- **WHEN** section 1.7 maps to grade 9 units, grade 11 units, and Algebraic Graphing units
- **THEN** its table has a Grade 9 lane, a Grade 11 lane, and an Algebraic Graphing lane, each listing that lane's units in path order

#### Scenario: Path order wins over mapping order
- **WHEN** a mapping lists a grade 11 unit before another grade 11 unit that comes earlier in the app's path
- **THEN** the lane shows them in path order

### Requirement: Index shows a chapter-level lane summary
Each chapter SHALL open with its summary note, if any, followed by a lane table that merges its sections' lanes: one lane per contributing grade or topic, listing that lane's recommended units in path order and tagging each unit with the section(s) it serves, so a student working a whole chapter can follow one lane from top to bottom.

#### Scenario: Unit serving two sections
- **WHEN** one unit is recommended for sections 1.5 and 1.6
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
