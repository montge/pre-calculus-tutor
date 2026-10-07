# Spec Delta

## Purpose

Produces a Markdown index of the section-to-unit mapping, readable directly on GitHub, so the reviewed data has a human-readable view that other deliverables (spreadsheet, study guides) can be checked against.

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

### Requirement: Index includes a no-coverage summary
The index SHALL include one consolidated list of every textbook section that has no Duolingo unit.

#### Scenario: Summary matches mapping
- **WHEN** the mapping has N sections with zero units
- **THEN** the no-coverage list has exactly N entries

### Requirement: Index cites its sources
The index SHALL end with the textbook citation and the date the Duolingo inventory was last verified, and SHALL state that no textbook content is reproduced.

#### Scenario: Citation present
- **WHEN** the index is generated
- **THEN** its final section contains the citation and the verification date
