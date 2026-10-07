# Spec Delta

## Purpose

Produces the student-facing tutorial document from the catalogs and the mapping, so the recommendation a student reads is always derived from the reviewed data rather than maintained by hand.

## ADDED Requirements

### Requirement: Tutorial is generated from data
The tutorial document SHALL be produced by a single command from the textbook catalog, the Duolingo catalog, and the mapping, and running the command twice on unchanged data SHALL produce identical output.

#### Scenario: Reproducible build
- **WHEN** the build command runs twice with no data changes
- **THEN** the generated file is byte-for-byte identical

#### Scenario: Build refuses invalid data
- **WHEN** any data file fails validation
- **THEN** the build exits non-zero, prints each validation error, and does not overwrite the previous tutorial

### Requirement: Tutorial has a chapter-by-chapter study guide
The tutorial SHALL present, for each chapter in book order, each section with its page number and the recommended Duolingo units in the order a student should do them, with each unit's coverage rating and note.

#### Scenario: Section with units
- **WHEN** a section maps to two units
- **THEN** the tutorial lists both under that section with their ratings, prerequisites first

#### Scenario: Section without units
- **WHEN** a section maps to no units
- **THEN** the tutorial says so explicitly under that section and the section also appears in the no-coverage list

### Requirement: Tutorial includes a no-coverage summary
The tutorial SHALL include one consolidated list of every textbook section that has no Duolingo unit, so a student knows what must be studied from the book alone.

#### Scenario: Summary matches mapping
- **WHEN** the mapping has N sections with zero units
- **THEN** the no-coverage list has exactly N entries

### Requirement: Tutorial cites its sources
The tutorial SHALL end with a citation of the textbook (title, edition, author, publisher, year) and the date the Duolingo inventory was last verified, and SHALL state that no textbook content is reproduced.

#### Scenario: Citation present
- **WHEN** the tutorial is generated
- **THEN** its final section contains the citation and the verification date
