# pre-calculus-tutor

A study guide that maps Duolingo Math units to the sections of a specific
precalculus textbook, so a student following the book knows which Duolingo
units to practice before or alongside each section, and which sections the
app does not cover at all.

Textbook followed: Larson, *Precalculus with Limits*, 2nd edition.

## Content policy (fair use)

This repository stores only the textbook's chapter and section titles, page
numbers, and bibliographic data, for the purpose of reference and citation.
It does not and must not contain textbook prose, exercises, answers, figures,
or scanned pages, nor Duolingo screenshots or lesson content. Duolingo unit
names are recorded as observed in the app.

## Layout

- `data/textbook/` — textbook structure (chapters, sections, pages, citation)
- `data/duolingo/` — Duolingo Math unit inventory (to be collected from the app)
- `data/mappings/` — reviewed section-to-unit mappings with coverage ratings
- `docs/` — the generated tutorial (not yet built)
- `openspec/` — planning artifacts; this project uses
  [OpenSpec](https://github.com/Fission-AI/OpenSpec) for spec-driven changes

## Workflow

Changes are planned and tracked with OpenSpec. The current change is
`map-duolingo-to-textbook`:

```bash
npx @fission-ai/openspec status --change map-duolingo-to-textbook
```

In Claude Code, `/opsx:apply` implements the tasks of a change and
`/opsx:archive` finalizes it.
