# Proposal

## Why

The mapping tells a student which Duolingo units pair with each textbook chapter, but Duolingo covers only part of precalculus and the textbook does not teach the TI-84. Students need, for each chapter, a short tutorial that explains the ideas in plain language, original worked examples and practice problems, step-by-step TI-84 instructions, and a list of the mistakes students actually make along with the tricks that avoid them. Printable PDFs built from LaTeX render mathematics properly and can be handed out.

## What Changes

- Author one LaTeX study guide per textbook chapter (12 chapters plus Appendix A) with a fixed structure: overview and Duolingo pairing, key ideas per section, worked examples, practice problems with an answer key, TI-84 how-to, common errors, tricks and shortcuts, and a chapter checklist.
- Generate the Duolingo pairing block of each guide from the mapping data so it never drifts from the spreadsheet or index.
- Maintain a shared TI-84 Plus CE reference (keystroke conventions, mode settings, the menus used throughout) that chapter guides cross-reference.
- Build each chapter to its own PDF and all chapters to one combined PDF with a single command, locally and in continuous integration, and publish the PDFs as downloadable release assets.
- All problems, examples, explanations, and figures are original. No textbook text, exercises, or figures are reproduced.

## Capabilities

### New Capabilities
- `study-guide-content`: What every chapter guide must contain, the originality and citation rules, and how the Duolingo pairing block is sourced.
- `calculator-guidance`: The TI-84 Plus CE instructions: the shared reference, the per-chapter procedures, and the conventions for writing keystrokes.
- `study-guide-build`: The LaTeX to PDF build: inputs, outputs, reproducibility, failure behavior, and continuous-integration publishing.

### Modified Capabilities
<!-- none -->

## Impact

- Depends on the `precalc_tutor` loader from `map-duolingo-to-textbook` for the generated pairing blocks.
- New directory `guides/` (LaTeX sources, shared preamble and macros, generated includes), new script `scripts/build_guides.py`, a GitHub Actions workflow, and a SessionStart hook that installs TeX Live in cloud sessions.
- New system dependency: TeX Live (pdflatex, latexmk, pgfplots). Verified installable in this environment via apt after `apt-get update`.
- README gains download links to the PDFs.
