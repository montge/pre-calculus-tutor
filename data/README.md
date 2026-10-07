# Data files

This directory holds the three hand-curated data files the project is built
from. All of them are plain YAML so they can be edited by hand and reviewed
in a diff.

| File | Contents |
| --- | --- |
| `textbook/larson-precalculus-with-limits-2e.yaml` | Chapter and section titles, starting page numbers, and bibliographic data for the textbook. |
| `duolingo/math-course.yaml` | Every Duolingo Math grade and topic with its units in the order the app shows them, plus the date and platform the inventory was verified on. |
| `mappings/larson-2e-to-duolingo.yaml` | One entry per textbook section listing the Duolingo units to practise for it, each with a coverage rating (`full`, `partial`, `prerequisite`) and a note. |

## Fair-use policy

These files store **titles, identifiers, page numbers, order, and our own
commentary only**. They must never contain:

- textbook prose, examples, exercises, answers, figures, or scanned pages;
- Duolingo screenshots, exercise content, or anything beyond unit names and
  their grouping and order.

The validator rejects image files anywhere under `data/`. Textbook titles and
Duolingo unit names are third-party material cited under fair use; see the
repository `NOTICE`.
