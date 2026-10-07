# Spec Delta

## Purpose

Gives students accurate, consistently written TI-84 Plus CE instructions for the techniques each chapter needs, so calculator use supports rather than replaces understanding.

## ADDED Requirements

### Requirement: Shared calculator reference
There SHALL be a shared TI-84 reference included in every guide's appendix covering: the key notation used in all guides, mode settings (radian versus degree, float versus fixed), the Y= and graph workflow, window and zoom, table, and the CALC menu, and how to reset to defaults.

#### Scenario: Reference present
- **WHEN** any chapter PDF is built
- **THEN** it contains the shared reference as its final appendix

### Requirement: Keystrokes are written in one notation
Every calculator procedure SHALL present keystrokes as a numbered sequence using the shared key macro, SHALL state which menu each step opens, and SHALL show what the screen displays after the final step.

#### Scenario: Procedure format
- **WHEN** a procedure for finding a zero with the CALC menu is written
- **THEN** each step names the key pressed and the menu or prompt that appears, and the last step states the expected on-screen result

### Requirement: Each chapter has procedures for its techniques
Each chapter guide SHALL include a TI-84 procedure for every technique in the chapter where the calculator is commonly used, and SHALL note what the calculator cannot do or where it misleads (for example, asymptotes drawn as lines in connected mode).

#### Scenario: Trigonometry chapter
- **WHEN** the chapter 4 guide is built
- **THEN** it includes procedures for setting radian mode, evaluating trigonometric functions, graphing sine with a suitable window, and converting degrees to radians, and a note on mode-related errors

### Requirement: Model assumption is stated
Procedures SHALL target the TI-84 Plus CE and SHALL note differences when the TI-84 Plus or TI-84 Plus Silver Edition differs in a way that affects the procedure.

#### Scenario: Model note
- **WHEN** a procedure relies on a key or menu that differs on the monochrome TI-84 Plus
- **THEN** the procedure carries a note describing the difference
