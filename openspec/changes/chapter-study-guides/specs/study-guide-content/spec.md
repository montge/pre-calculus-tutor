# Spec Delta

## Purpose

Defines the content every chapter study guide must deliver to a student, and the originality and attribution rules that keep the guides within fair use.

## ADDED Requirements

### Requirement: One guide per chapter with a fixed structure
There SHALL be one study guide for each of the 12 textbook chapters and for Appendix A, and each guide SHALL contain, in order: Overview, Duolingo pairing, Key ideas by section, Worked examples, Practice problems, Answer key, TI-84 how-to, Common errors, Tricks and shortcuts, and Chapter checklist.

#### Scenario: Guide has every part
- **WHEN** a chapter guide is built
- **THEN** its table of contents lists all ten parts in that order

#### Scenario: Chapter with no Duolingo coverage
- **WHEN** the mapping has no units for any section of the chapter
- **THEN** the Duolingo pairing part states that and points the student to the practice problems instead

### Requirement: Key ideas cover every section
The Key ideas part SHALL have one subsection per numbered textbook section of the chapter, titled with the section id and title and citing its page, explaining the section's main ideas in the guide author's own words.

#### Scenario: Section coverage
- **WHEN** chapter 4 is built
- **THEN** Key ideas has eight subsections, 4.1 through 4.8, each citing its page number

### Requirement: Problems are original with checked answers
Worked examples and practice problems MUST be written for this project (not taken from the textbook, Duolingo, or any other copyrighted source), each practice problem MUST have an answer in the answer key, and every answer MUST have been verified independently of the person who wrote the problem.

#### Scenario: Minimum problem count
- **WHEN** a chapter guide is reviewed
- **THEN** it has at least two worked examples and at least four practice problems per textbook section

#### Scenario: Answer verification recorded
- **WHEN** a practice problem is added
- **THEN** the source file records who or what verified the answer and how (by hand, by CAS, by calculator)

### Requirement: Common errors and tricks are concrete
Each Common errors entry SHALL show the mistake, why it is wrong, and the correction; each Tricks entry SHALL state when the trick applies and give one example.

#### Scenario: Error entry
- **WHEN** a common error such as dropping the negative when squaring is listed
- **THEN** the entry shows the wrong step, the reason, and the corrected step

### Requirement: Duolingo pairing is generated from the mapping
The Duolingo pairing part SHALL be generated from the mapping data at build time, listing each section's units in recommended order with coverage ratings, and MUST NOT be edited by hand.

#### Scenario: Mapping change propagates
- **WHEN** a unit is added to section 3.2 in the mapping and the guides are rebuilt
- **THEN** the chapter 3 guide's pairing part lists the new unit without any edit to the guide source

### Requirement: Guides carry attribution
Each guide SHALL state on its first page that it accompanies the cited textbook, that it reproduces none of the textbook's content, that the author is not affiliated with the publisher or Duolingo, and the content license.

#### Scenario: Attribution present
- **WHEN** any chapter PDF is opened
- **THEN** the first page shows the textbook citation and the non-affiliation and license statement
