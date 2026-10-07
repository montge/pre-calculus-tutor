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

## The mapping index

[`docs/mapping-index.md`](docs/mapping-index.md) is the reference view: for
every chapter and section of the book, the Duolingo units to practise, with
a coverage rating and a note, laid out as one lane per Duolingo grade or
topic in the order the app presents them. Chapters 1 through 3 are mapped;
later chapters are placeholders until they are reviewed.

## Track your progress

Download either file from `dist/` (no build needed):

- [`progress-tracker.xlsx`](dist/progress-tracker.xlsx): a workbook with a
  **By section** sheet (book order) and a **By lane** sheet (the same units
  grouped by chapter and Duolingo grade or topic, in the order the app shows
  them). Set each row's Status to *Not started*, *In progress*, or *Done*;
  the **Chapters** sheet totals up as you go. Opens in Excel, Google Sheets,
  and LibreOffice.
- [`progress-checklist.pdf`](dist/progress-checklist.pdf): the same checklist
  on paper, one chapter per page, with a checkbox per textbook section and
  per Duolingo unit in app order.

Both cover chapters 1 through 3 so far.

## Building

```bash
pip install -r requirements.txt
python scripts/build_index.py          # validates data/ and writes docs/mapping-index.md
python scripts/build_index.py --check  # validate only
python scripts/build_tracker.py        # writes dist/progress-tracker.xlsx and dist/progress-checklist.pdf
python -m unittest                     # run the tests
```

The build validates all three data files first (every section has one
mapping entry, every unit id resolves, unit counts match the app, no images
under `data/`) and refuses to overwrite the index if anything fails.

## Layout

- `data/textbook/` — textbook structure (chapters, sections, pages, citation)
- `data/duolingo/` — Duolingo Math inventory: every grade and topic with its units in path order (transcribed from the app)
- `data/mappings/` — reviewed section-to-unit mappings with coverage ratings
- `docs/` — the generated mapping index
- `dist/` — the generated tracker workbook and printable checklist
- `precalc_tutor/` — loader, validator, lane derivation, and index renderer
- `scripts/` — build entry points
- `tests/` — unit tests (`python -m unittest`)
- `openspec/` — planning artifacts; this project uses
  [OpenSpec](https://github.com/Fission-AI/OpenSpec) for spec-driven changes

## Planned deliverables

1. **Mapping data and index** (`map-duolingo-to-textbook`): validated
   catalogs of textbook sections and Duolingo grades, topics, and units, a
   reviewed mapping with coverage ratings, and a Markdown index with lanes
   showing which units to follow for each chapter and section.
2. **Progress tracker** (`progress-tracker-spreadsheet`): a workbook students
   fill in at the Duolingo unit level, in book order and in Duolingo order,
   with live per-chapter completion, plus a printable checklist PDF.
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
