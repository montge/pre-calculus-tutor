# Spec Delta

## Purpose

Defines the reviewed correspondence between textbook sections and Duolingo units (optionally narrowed to specific lessons), including how well each unit covers a section, and the integrity rules that keep the mapping consistent with both catalogs.

## ADDED Requirements

### Requirement: Every section has a mapping entry
The mapping SHALL contain exactly one entry for every numbered section in the textbook catalog, including sections that have no matching Duolingo unit.

#### Scenario: Section with no coverage
- **WHEN** a section such as "Partial Fractions" has no Duolingo unit
- **THEN** its entry lists zero units and a note explaining that Duolingo does not cover it

#### Scenario: Missing entry
- **WHEN** a section in the catalog has no mapping entry
- **THEN** validation fails and names the section

### Requirement: Mapped units carry a coverage rating
Each unit listed under a section SHALL have a coverage rating of `full`, `partial`, or `prerequisite`, and a note stating what the unit covers relative to the section.

#### Scenario: Partial coverage
- **WHEN** a unit practices right-triangle ratios only in degrees for section "Right Triangle Trigonometry"
- **THEN** it is rated `partial` with a note that radians and applications are not covered

#### Scenario: Invalid rating
- **WHEN** an entry uses a rating other than the three allowed values
- **THEN** validation fails and names the entry

### Requirement: A mapped unit may be narrowed to specific lessons
A unit listed under a section MAY carry a list of lesson identifiers from that unit. When the list is present, only those lessons are recommended for the section; when it is absent, every lesson of the unit is recommended. Lessons SHALL always be presented in their catalog (path) order regardless of the order written in the mapping.

#### Scenario: Unit narrowed to two lessons
- **WHEN** section 1.3 lists a unit with lessons `[l-g9-012, l-g9-010]`
- **THEN** outputs recommend only those two lessons for 1.3, shown in path order (`l-g9-010` first)

#### Scenario: Lesson not in the unit
- **WHEN** a lesson identifier under a unit belongs to a different unit or does not exist
- **THEN** validation fails and names the section, the unit, and the lesson

### Requirement: Mapping references resolve
Every section identifier in the mapping MUST exist in the textbook catalog, and every unit identifier MUST exist in the Duolingo catalog.

#### Scenario: Dangling unit reference
- **WHEN** a mapping references a unit identifier that is not in the Duolingo catalog
- **THEN** validation fails and names the section and the unknown unit

### Requirement: Mapping records review status
Each section entry SHALL record whether its mapping has been reviewed by a person, so that generated output can distinguish reviewed mappings from drafts.

#### Scenario: Draft mapping shown as such
- **WHEN** a section's entry is marked unreviewed
- **THEN** the generated outputs mark that section's recommendations as draft
