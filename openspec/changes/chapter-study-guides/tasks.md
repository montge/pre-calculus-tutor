# Tasks

## 1. Build scaffolding

- [ ] 1.1 Create `guides/common/preamble.tex` and `macros.tex` (amsmath, amssymb, pgfplots, hyperref, the `\key` macro, the `procedure` environment, the `\answer` macro, attribution front-page command) and a minimal `guides/ch01/main.tex` that includes them; verify `latexmk -pdf` builds it.
- [ ] 1.2 Implement `scripts/build_guides.py`: validate data via `precalc_tutor`, write `guides/generated/chNN-pairing.tex` and `guides/generated/chNN-gaps.tex` (the section's book-only gaps, for the Key ideas opener) with a do-not-edit header, check that every gap in the mapping has a `\gapexample{<section>}{<gap>}` tag in the chapter's worked examples and fail naming the section and gap otherwise, run latexmk per chapter and for `guides/book.tex`, collect PDFs into `dist/guides/`, exit non-zero on any error; verify a deliberate LaTeX error in one chapter fails the build and names the chapter.
- [ ] 1.3 Add `guides/generated/` and LaTeX build artifacts to `.gitignore`, add `SOURCE_DATE_EPOCH` handling, and write `tests/test_build_guides.py` covering generated-header presence, reproducibility (page count and extracted text), and the verification-comment check for every `\answer`; verify `python -m unittest` passes.
- [ ] 1.4 Add a SessionStart hook that installs the TeX Live packages when `pdflatex` is missing, and `.github/workflows/guides.yml` building in the `texlive/texlive` image, uploading `dist/guides/*.pdf` as artifacts, and attaching them to releases on `v*` tags; verify the workflow passes on a push and the hook makes `pdflatex` available in a fresh cloud session.

## 2. Shared calculator reference

- [ ] 2.1 Write `guides/common/ti84-reference.tex` (key notation, modes, Y= and graph workflow, window and zoom, table, CALC menu, reset) and include it as the final appendix of every chapter and the book; verify it appears in the chapter 1 PDF's table of contents.

## 3. Chapter guides, Duolingo-overlap chapters first

- [ ] 3.1 Write the chapter 1 guide (Functions and Their Graphs): ideas for 1.1 through 1.10, examples, problems with verified answers, TI-84 procedures (graphing, table, intersect, evaluating a function), errors, tricks, checklist; verify it builds, has all ten parts, meets the minimum problem counts, and every answer has a verification comment.
- [ ] 3.2 Write the chapter 2 guide (Polynomial and Rational Functions) the same way, with TI-84 procedures for zeros, maximum and minimum, and polynomial division checks; verify as in 3.1.
- [ ] 3.3 Write the chapter 3 guide (Exponential and Logarithmic Functions) with TI-84 procedures for logs of any base, solving exponential equations by intersect, and regression; verify as in 3.1.
- [ ] 3.4 Write the chapter 4 guide (Trigonometry) with TI-84 procedures for radian and degree mode, unit-circle values, graphing sine and cosine with suitable windows, and inverse functions; verify as in 3.1.
- [ ] 3.5 Write the chapter 5 guide (Analytic Trigonometry) with TI-84 procedures for checking identities numerically and graphically and solving trig equations on an interval; verify as in 3.1.
- [ ] 3.6 Write the chapter 6 guide (Additional Topics in Trigonometry) with TI-84 procedures for Law of Sines and Cosines computations, vectors, and complex numbers in polar form; verify as in 3.1.

## 4. Chapter guides, remaining chapters

- [ ] 4.1 Write the chapter 7 guide (Systems of Equations and Inequalities) with TI-84 procedures for intersect and shading inequalities; verify as in 3.1.
- [ ] 4.2 Write the chapter 8 guide (Matrices and Determinants) with TI-84 procedures for the MATRIX menu, rref, inverse, and determinant; verify as in 3.1.
- [ ] 4.3 Write the chapter 9 guide (Sequences, Series, and Probability) with TI-84 procedures for seq, sum, nCr, nPr, and factorial; verify as in 3.1.
- [ ] 4.4 Write the chapter 10 guide (Topics in Analytic Geometry) with TI-84 procedures for parametric and polar modes; verify as in 3.1.
- [ ] 4.5 Write the chapter 11 guide (Analytic Geometry in Three Dimensions) with TI-84 procedures for vector arithmetic via lists; verify as in 3.1.
- [ ] 4.6 Write the chapter 12 guide (Limits and an Introduction to Calculus) with TI-84 procedures for tables near a point, nDeriv, and fnInt; verify as in 3.1.
- [ ] 4.7 Write the Appendix A guide (Review of Fundamental Concepts of Algebra) with TI-84 procedures for fractions, exponents, and checking factoring; verify as in 3.1.

## 5. Combined book and publishing

- [ ] 5.1 Assemble `guides/book.tex` with front matter (attribution, how the book pairs with Duolingo, table of contents) and all chapters; verify the combined PDF builds and its bookmarks list every chapter.
- [ ] 5.2 Add download links for the combined PDF and each chapter PDF to `README.md` pointing at the latest release; verify the links resolve after the first tagged release.

## 6. Integration check

- [ ] 6.1 Build from a clean checkout with the one build command, open each PDF, and confirm every chapter has all ten parts, the pairing block matches `docs/mapping-index.md`, and the attribution page is present; record the result in the task notes.

## Workflow follow-up

- Archive the change after the user has reviewed at least the chapters 1 through 6 guides.
