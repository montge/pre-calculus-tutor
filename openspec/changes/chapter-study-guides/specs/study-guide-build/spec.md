# Spec Delta

## Purpose

Turns the LaTeX sources and the mapping data into PDF study guides reliably, locally and in continuous integration, so students can always download a current build.

## ADDED Requirements

### Requirement: One command builds all guides
A single command SHALL validate the data, generate the Duolingo pairing includes, and build one PDF per chapter guide plus one combined PDF, exiting non-zero on any validation error or LaTeX error.

#### Scenario: Successful build
- **WHEN** the build command runs on valid sources
- **THEN** `dist/guides/` contains one PDF per chapter guide and one combined PDF

#### Scenario: LaTeX error fails the build
- **WHEN** a chapter source has a LaTeX error
- **THEN** the build exits non-zero and the log names the chapter and the error

### Requirement: Generated includes are never hand edited
Generated LaTeX includes SHALL live in a dedicated generated directory, SHALL carry a do-not-edit header, and SHALL be ignored by version control.

#### Scenario: Generated directory
- **WHEN** the build runs
- **THEN** every file in the generated directory begins with a do-not-edit comment and none is tracked by git

### Requirement: Builds are reproducible
Two builds of unchanged sources SHALL produce PDFs with identical page counts and identical extracted text.

#### Scenario: Reproducibility check
- **WHEN** the build runs twice with no changes
- **THEN** page counts and extracted text of each PDF match

### Requirement: Continuous integration builds and publishes
Every push SHALL build all guides in continuous integration, fail the check on error, and upload the PDFs as workflow artifacts; a tagged release SHALL attach the PDFs as release assets.

#### Scenario: Push with a LaTeX error
- **WHEN** a push introduces a LaTeX error
- **THEN** the continuous-integration check fails and names the chapter

#### Scenario: Release
- **WHEN** a version tag is pushed
- **THEN** the release carries every chapter PDF and the combined PDF

### Requirement: Cloud sessions can build locally
A session-start hook SHALL install the TeX Live packages the build needs when they are absent, so a cloud session can run the build and tests.

#### Scenario: Fresh cloud session
- **WHEN** a cloud session starts without pdflatex installed
- **THEN** after the hook runs, the build command succeeds
