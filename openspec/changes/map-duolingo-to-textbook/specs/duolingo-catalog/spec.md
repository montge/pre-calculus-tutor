# Spec Delta

## Purpose

Holds the inventory of Duolingo Math units, with their grade and topic groupings, so mappings can reference a unit by a stable identifier and readers can tell how current the inventory is.

## ADDED Requirements

### Requirement: Unit inventory records name and grouping
Each unit in the Duolingo catalog SHALL have a unique identifier, the unit name as shown in the app, the grade it appears under, the topic it appears under if any, and a one-sentence description of what the unit practices.

#### Scenario: Unit entry is complete
- **WHEN** a unit entry is loaded
- **THEN** it has a non-empty identifier, name, grade, and description, and validation reports any unit missing one of these

### Requirement: Inventory records its provenance
The Duolingo catalog SHALL record the date it was last checked against the app and the platform it was observed on, because unit names and groupings change between app releases.

#### Scenario: Provenance appears in output
- **WHEN** any output (mapping index, spreadsheet, study guide) is generated
- **THEN** it states the date the unit inventory was last verified

### Requirement: Inventory may be partial
The catalog SHALL allow a `complete: false` flag so that a partial inventory can be used while units are still being collected, and every generated output SHALL warn readers when the inventory is incomplete.

#### Scenario: Partial inventory
- **WHEN** the catalog is marked incomplete
- **THEN** validation passes and the mapping index shows an incomplete-inventory notice at the top
