# Spec Delta

## Purpose

Defines the reviewed correspondence between textbook sections and Duolingo units, including how well each unit covers a section, and the integrity rules that keep the mapping consistent with both catalogs.

## ADDED Requirements

### Requirement: Every section has a mapping entry
The mapping SHALL contain exactly one entry for every numbered section in the textbook catalog, including appendix sections and sections that have no matching Duolingo unit.

#### Scenario: Section with no coverage
- **WHEN** a section such as "Polynomial and Synthetic Division" has no Duolingo unit
- **THEN** its entry lists zero units and a note explaining that Duolingo does not cover it

#### Scenario: Missing entry
- **WHEN** a section in the catalog has no mapping entry
- **THEN** validation fails and names the section

### Requirement: Mapped units carry a coverage rating
Each unit listed under a section SHALL have a coverage rating of `full`, `partial`, or `prerequisite`, and a note stating what the unit covers relative to the section. A unit may come from a grade or from a topic.

#### Scenario: Partial coverage
- **WHEN** a unit practices right-triangle ratios only in degrees for section "Right Triangle Trigonometry"
- **THEN** it is rated `partial` with a note that radians and applications are not covered

#### Scenario: Invalid rating
- **WHEN** an entry uses a rating other than the three allowed values
- **THEN** validation fails and names the entry

### Requirement: Mapping references resolve
Every section identifier in the mapping MUST exist in the textbook catalog, and every unit identifier MUST exist in the Duolingo catalog, under a grade or a topic.

#### Scenario: Dangling unit reference
- **WHEN** a mapping references a unit identifier that is not in the Duolingo catalog
- **THEN** validation fails and names the section and the unknown unit

### Requirement: Mapping records review status
Each section entry SHALL record whether its mapping has been reviewed by a person, so that generated output can distinguish reviewed mappings from drafts.

#### Scenario: Draft mapping shown as such
- **WHEN** a section's entry is marked unreviewed
- **THEN** the generated outputs mark that section's recommendations as draft

### Requirement: Mapping may carry chapter summaries
The mapping MAY carry one summary note per chapter (for example which lane to follow when time is short, or that the chapter is book only), which outputs show at the top of that chapter.

#### Scenario: Chapter summary shown
- **WHEN** chapter 2 has a summary note
- **THEN** the mapping index prints it under the chapter heading before the lane table
