# Design

## Context

See proposal.md. Depends on the `precalc_tutor` loader from `map-duolingo-to-textbook`. In this cloud environment TeX Live is not preinstalled but installs with apt after `apt-get update` (verified), and pandoc and LibreOffice are present. GitHub Actions is available for publishing.

## Goals / Non-Goals

**Goals:**
- Hand-written LaTeX stays hand-written; anything derived from data is generated and never edited.
- A contributor with pdflatex can build one chapter in seconds without building the whole book.
- Mathematics and graphs render as vector output.

**Non-Goals:**
- HTML or EPUB output. PDF is the deliverable; the Markdown index covers the on-screen case.
- Interactive or auto-graded problems.
- Covering Appendix B (web-only statistics) or chapters beyond what the textbook contains.

## Decisions

- **pdflatex via latexmk, with pgfplots and TikZ for graphs.** Alternatives: XeLaTeX or LuaLaTeX (needed only for system fonts, which the guides do not use), tectonic (not installable here), pandoc Markdown to PDF (still needs a LaTeX engine and loses control over layout). latexmk handles the multiple passes and the combined book cleanly.
- **Layout: `guides/common/` (preamble, macros, shared TI-84 reference), `guides/chNN/` (one `main.tex` per chapter including part files `ideas.tex`, `examples.tex`, `problems.tex`, `answers.tex`, `ti84.tex`, `errors.tex`, `tricks.tex`), `guides/generated/` (pairing includes, git-ignored), `guides/book.tex` (combines all chapters).** Part files keep diffs small and let the answer key be reviewed separately from the problems.
- **A `\key{...}` macro and a `procedure` environment for calculator steps**, defined in `guides/common/macros.tex`, rather than the `menukeys` package, so rendering does not depend on a package outside texlive-latex-recommended and the notation can be tuned in one place.
- **`scripts/build_guides.py` orchestrates:** validate data, write `guides/generated/chNN-pairing.tex` from the mapping, then run latexmk for each chapter and the book, collecting PDFs into `dist/guides/`. One Python entry point mirrors the index and tracker builders.
- **Problems carry a verification record in a LaTeX comment on the line after each answer** (for example `% verified: by hand, 2026-10-07` or `% verified: sympy`). A test greps that every `\answer` has a verification comment. Cheap, reviewable, and it satisfies the spec's verification rule without extra tooling.
- **Reproducibility by comparing page counts and extracted text (pdftotext or pypdf), not bytes.** pdflatex embeds creation dates; `SOURCE_DATE_EPOCH` is set in the build to stabilize them, but text comparison is the robust check.
- **CI uses the official `texlive/texlive` container image** so pgfplots and fonts are present without per-run apt installs; the release job attaches `dist/guides/*.pdf` on tags matching `v*`.
- **SessionStart hook runs `apt-get update` and installs `texlive-latex-base`, `texlive-latex-recommended`, `texlive-pictures`, `texlive-latex-extra`, `latexmk` only when `pdflatex` is missing.**
- **TI-84 Plus CE is the reference model**, OS 5.x menus. The monochrome TI-84 Plus differs mainly in color and screen size, and procedures note the few cases where keys differ.
- **Authoring order: chapters 1 through 6 first (Duolingo overlap), then 7 through 12 and Appendix A.** Each chapter is its own task so review can happen per chapter.

## Risks / Trade-offs

- [Authoring 13 guides is the bulk of the work and quality varies] → fixed structure and minimum counts in the spec, per-chapter tasks with independent answer verification, and the answer key reviewed separately.
- [Accidental reproduction of textbook problems from memory] → the spec requires original problems with different numbers and contexts; reviewers compare against the book before marking a chapter reviewed.
- [TI-84 procedures drift across OS versions] → each procedure states the OS assumption; the shared reference has a "check your OS version" step.
- [TeX Live install in cloud sessions is slow (minutes)] → the hook installs only when pdflatex is missing and only the listed packages; CI uses a prebuilt image.
- [pgfplots not in texlive-latex-recommended] → the hook and docs install texlive-pictures; a build-time check prints a clear message if pgfplots is absent.

## Open Questions

- Whether to include a short "How to study with this guide" page for parents and tutors. It does not change the structure or tasks and can be added to the combined book's front matter later.
