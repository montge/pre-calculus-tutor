# Spec Delta

## Purpose

Holds the inventory of Duolingo Math units as two hierarchies, grades and topics, each in the order the app presents them, so mappings can reference a unit by a stable identifier, outputs can lay units out in per-grade lanes, and readers can tell how current the inventory is.

## ADDED Requirements

### Requirement: Inventory mirrors the app's two views in app order
The Duolingo catalog SHALL record every grade from the app's Grades view and every topic from its Topics view, each containing its units in the order the app's path presents them, with the unit total the app displays for that grade or topic. Units are the finest named grain the app exposes: the nodes inside a unit are unnamed practice steps and are not recorded.

#### Scenario: Order is preserved
- **WHEN** grade 10's path shows "Intro to the sine ratio" before "Sine of 30"
- **THEN** the catalog lists them in that order under grade 10 and each carries its position in the path

#### Scenario: Count matches the app
- **WHEN** the app shows a grade or topic with N units
- **THEN** the catalog records N as that grade's or topic's unit total, and validation fails if the number of unit entries differs from it

### Requirement: Unit entries record name and grouping
Each unit SHALL have a unique identifier, the unit name exactly as shown in the app (including the app's own spellings), the grade or topic it appears under, its position in that path, and MAY have a one-sentence description of what the unit practices.

#### Scenario: Unit entry is complete
- **WHEN** a unit entry is loaded
- **THEN** it has a non-empty identifier, name, parent grade or topic, and position, and validation reports any unit missing one of these

#### Scenario: Same name in two grades
- **WHEN** "Equivalent fractions" appears in grades 3, 4, and 5
- **THEN** each is a distinct unit with its own identifier and a mapping can reference any one of them unambiguously

### Requirement: Inventory is transcribed, never scraped or stored as images
Unit names SHALL be transcribed as text from the app as a person observes it (including from screenshots the person shares while working), and the repository MUST NOT contain Duolingo screenshots, exercises, or other app content beyond the names, grouping, and order.

#### Scenario: Screenshot is rejected
- **WHEN** a contributor attempts to add an app screenshot under `data/`
- **THEN** validation fails and the file is not accepted

### Requirement: Inventory records its provenance
The Duolingo catalog SHALL record the date it was last checked against the app and the platform it was observed on, because unit names and groupings change between app releases.

#### Scenario: Provenance appears in output
- **WHEN** any output (mapping index, spreadsheet, study guide) is generated
- **THEN** it states the date the inventory was last verified

### Requirement: Inventory may be partial
The catalog SHALL allow a `complete: false` flag so that a partial inventory can be used while grades or topics are still being collected, and every generated output SHALL warn readers when the inventory is incomplete.

#### Scenario: Partial inventory
- **WHEN** the catalog is marked incomplete
- **THEN** validation passes and the mapping index shows an incomplete-inventory notice at the top
