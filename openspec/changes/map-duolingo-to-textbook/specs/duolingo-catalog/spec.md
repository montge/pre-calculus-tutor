# Spec Delta

## Purpose

Holds the inventory of Duolingo Math content as a hierarchy of grades, units, and lessons in the order the app presents them, so mappings can reference a unit or lesson by a stable identifier, outputs can lay lessons out in per-grade lanes, and readers can tell how current the inventory is.

## ADDED Requirements

### Requirement: Inventory is a grade, unit, lesson hierarchy in app order
The Duolingo catalog SHALL be organized as grades, each containing its units in the order the app's path presents them, each unit containing its lessons in path order. Where the app groups units under a heading (its own section or topic grouping), that heading SHALL be recorded on each unit so the grouping can be reproduced.

#### Scenario: Order is preserved
- **WHEN** grade 10's path shows unit "Polynomial arithmetic" before "Polynomial function equations and graphs"
- **THEN** the catalog lists them in that order under grade 10 and each carries its position in the path

#### Scenario: Lessons belong to one unit
- **WHEN** a lesson entry is loaded
- **THEN** it sits under exactly one unit and has a position within that unit

### Requirement: Unit entries record name and grouping
Each unit SHALL have a unique identifier, the unit name as shown in the app, the grade it appears under, the app grouping heading it appears under if any, its position in the grade's path, and a one-sentence description of what the unit practices.

#### Scenario: Unit entry is complete
- **WHEN** a unit entry is loaded
- **THEN** it has a non-empty identifier, name, grade, position, and description, and validation reports any unit missing one of these

### Requirement: Lesson entries record name and position
Each lesson SHALL have an identifier unique within the catalog, the lesson name as shown in the app, and its position within its unit. A unit MAY have an empty lesson list while its lessons are still being collected.

#### Scenario: Lesson identifier lookup
- **WHEN** a mapping references a lesson identifier
- **THEN** exactly one lesson in the catalog has that identifier and the catalog can report its grade, unit, and position

#### Scenario: Duplicate lesson identifier
- **WHEN** two lessons share an identifier
- **THEN** validation fails and names both units

### Requirement: Inventory is transcribed, never scraped or stored as images
Unit and lesson names SHALL be transcribed as text from the app as a person observes it (including from screenshots the person shares while working), and the repository MUST NOT contain Duolingo screenshots, lesson exercises, or other app content beyond the names, grouping, and order.

#### Scenario: Screenshot is rejected
- **WHEN** a contributor attempts to add an app screenshot under `data/`
- **THEN** validation fails and the file is not accepted

### Requirement: Inventory records its provenance
The Duolingo catalog SHALL record the date it was last checked against the app and the platform it was observed on, because unit and lesson names and groupings change between app releases.

#### Scenario: Provenance appears in output
- **WHEN** any output (mapping index, spreadsheet, study guide) is generated
- **THEN** it states the date the inventory was last verified

### Requirement: Inventory may be partial
The catalog SHALL allow a `complete: false` flag so that a partial inventory can be used while grades, units, or lessons are still being collected, and every generated output SHALL warn readers when the inventory is incomplete.

#### Scenario: Partial inventory
- **WHEN** the catalog is marked incomplete
- **THEN** validation passes and the mapping index shows an incomplete-inventory notice at the top
