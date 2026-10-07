# pre-calculus-tutor

A study guide that maps Duolingo Math units to the sections of a specific
precalculus textbook, so a student following the book knows which Duolingo
units to practice before or alongside each section, and which sections the
app does not cover at all.

Textbook followed: Larson, *Precalculus with Limits*, 2nd edition.

## License

Code is licensed under the [Apache License 2.0](LICENSE). Content (the data
files, mappings, planning documents, and generated tutorial) is licensed under
[CC BY 4.0](LICENSE-CC-BY-4.0). Textbook titles and Duolingo unit names are
third-party material cited under fair use and are not covered by either
license; see [NOTICE](NOTICE).

## Content policy (fair use)

This repository stores only the textbook's chapter and section titles, page
numbers, and bibliographic data, for the purpose of reference and citation.
It does not and must not contain textbook prose, exercises, answers, figures,
or scanned pages, nor Duolingo screenshots or lesson content. Duolingo unit
names are recorded as observed in the app.

## Layout

- `data/textbook/` — textbook structure (chapters, sections, pages, citation)
- `data/duolingo/` — Duolingo Math inventory as the app's tree: grade, unit, lesson, in path order (transcribed from the app; being collected)
- `data/mappings/` — reviewed section-to-unit mappings with coverage ratings
- `docs/` — the generated tutorial (not yet built)
- `openspec/` — planning artifacts; this project uses
  [OpenSpec](https://github.com/Fission-AI/OpenSpec) for spec-driven changes

## Planned deliverables

1. **Mapping data and index** (`map-duolingo-to-textbook`): validated
   catalogs of textbook sections and Duolingo grades, units, and lessons, a
   reviewed mapping with coverage ratings, and a Markdown index with grade
   lanes showing which lessons to follow for each chapter and section.
2. **Progress tracker** (`progress-tracker-spreadsheet`): a workbook students
   fill in at the Duolingo unit level, grouped by chapter, with live
   per-chapter completion.
3. **Chapter study guides** (`chapter-study-guides`): one LaTeX-built PDF per
   chapter with a plain-language tutorial, original worked examples and
   practice problems with answers, TI-84 Plus CE procedures, common errors,
   and tricks, plus a combined book.

## Workflow

Changes are planned and tracked with OpenSpec, in the order listed above:

```bash
npx @fission-ai/openspec list
npx @fission-ai/openspec status --change map-duolingo-to-textbook
```

In Claude Code, `/opsx:apply` implements the tasks of a change and
`/opsx:archive` finalizes it.
