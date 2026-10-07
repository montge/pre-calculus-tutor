# Spec Delta

## Purpose

Holds the structural outline of the textbook the tutorial follows (chapters, sections, page numbers, and a citation) so other capabilities can reference sections by a stable identifier.

## ADDED Requirements

### Requirement: Textbook catalog lists every chapter and section
The textbook catalog SHALL contain one entry per chapter and one entry per numbered section, each with its title and starting page number, in the order they appear in the book.

#### Scenario: Catalog matches the printed table of contents
- **WHEN** the catalog for *Precalculus with Limits*, 2nd edition, is loaded
- **THEN** it contains 12 chapters, 76 numbered sections, Appendix A with 7 sections, and Appendix B with 3 sections, each with the title shown in the book's contents pages

#### Scenario: Chapter end matter is recorded
- **WHEN** a chapter entry is read
- **THEN** it lists the chapter's summary, review exercises, chapter test, proofs, problem-solving pages, and any cumulative test with their page numbers

### Requirement: Sections have stable identifiers
Each section SHALL have an identifier equal to its number as printed in the book (for example `4.2` or `A.3`), and identifiers SHALL be unique within a catalog.

#### Scenario: Identifier lookup
- **WHEN** another data file references section `4.2`
- **THEN** exactly one section in the catalog has that identifier, titled "Trigonometric Functions: The Unit Circle"

### Requirement: Catalog carries a citation
The catalog SHALL record the book's title, edition, author, publisher, and year so that generated documents can cite it, and SHALL flag any citation field that has not been verified against the book's copyright page.

#### Scenario: Unverified field is flagged
- **WHEN** the year was transcribed from memory rather than from the copyright page
- **THEN** the catalog marks the year as unverified and the generated tutorial notes it

### Requirement: Catalog stores no copyrighted content
The textbook catalog MUST contain only chapter and section titles, page numbers, and bibliographic data. It MUST NOT contain textbook prose, exercises, answers, figures, or scanned images.

#### Scenario: Scan is rejected
- **WHEN** a contributor attempts to add a photo of a textbook page to the repository
- **THEN** validation fails and the file is not accepted
