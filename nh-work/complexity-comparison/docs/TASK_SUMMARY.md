# STARK vs SyntComplex Verification Summary

Date: 2026-06-02

This workspace verifies the current STARK implementation of syntactic complexity measures against the reference SyntComplex script on the same input data.

> This summary covers the **dev** split (the task as originally scoped). The comparison was later extended to **train** and **test** with the same conclusion; see [`SSJ_TRAIN_TEST_RESULTS.md`](SSJ_TRAIN_TEST_RESULTS.md). Saved outputs are now suffixed per split (`_dev`/`_train`/`_test`).

## Data and Versions

- STARK checkout: [`b4c59799ab5fa4daa49d7a3a248bc2d75dec84e2`](https://github.com/hulln/STARK/commit/b4c59799ab5fa4daa49d7a3a248bc2d75dec84e2), version `3.2.0`
- SyntComplex reference: Luka Terčon's [`lukatercon/SyntComplex`](https://github.com/lukatercon/SyntComplex) at commit [`bb0ba82ee5f9061ddd516de76b48c56fc7bfa682`](https://github.com/lukatercon/SyntComplex/commit/bb0ba82ee5f9061ddd516de76b48c56fc7bfa682)
- SyntComplex script: [`scripts/calculate_metrics.py`](https://github.com/lukatercon/SyntComplex/blob/bb0ba82ee5f9061ddd516de76b48c56fc7bfa682/scripts/calculate_metrics.py)
- Corpus: official [`UD_Slovenian-SSJ/sl_ssj-ud-dev.conllu`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/blob/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu) at commit [`212197db9aebc89dbdf8c1631f3fcc29b88840d4`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/commit/212197db9aebc89dbdf8c1631f3fcc29b88840d4)
- Input SHA-256: `2999a1ac8261df77e71c4e824c8e036e4845f84748f36d04bc7b730d7daf9d9a`
- The same input file was used for both tools.

The checked-in local STARK sample `sample/sl_ssj-ud-dev.conllu` was not used because it is not identical to the current official UD file. The syntax columns are the same, but the files differ in metadata, MISC/NER content, and some `sent_id` values.

## STARK Run

STARK was run with the dedicated config:

`nh-work/complexity-comparison/configs/stark_complexity_sl_ssj_dev.ini`

Key settings:

```ini
size = 1-10000
head = deprel=root
complexity_measures = yes
example = yes
complete = yes
greedy_counter = yes
```

STARK produced `1250` rows, one for each sentence/root tree.

## SyntComplex Run

The reference `calculate_metrics.py` script was kept unmodified. Because SyntComplex uses hardcoded input paths, the wrapper `scripts/run_syntcomplex_reference.py` creates a temporary work directory, places the same SSJ dev file at the path expected by SyntComplex, creates empty placeholder files for unused inputs, runs the original script, and copies the SSJ dev result into this workspace.

SyntComplex also produced `1250` rows.

## Comparison Result

All sentences aligned correctly by `sent_id`.

| Measure | Match count |
|---|---:|
| MDD | 1245/1250 |
| NDD | 1245/1250 |
| Max depth | 1250/1250 |
| N clauses | 1250/1250 |
| N T-units | 1250/1250 |
| Clauses/T-unit | 1250/1250 |
| Number of nodes / tokens | 1250/1250 |

The only differences are five short punctuation-wrapped fragments:

- `ssj499.2651.9487` `(mu)`
- `ssj514.2725.9728` `(fl)`
- `ssj533.2814.10023` `(jo)`
- `ssj546.2865.10180` `(sta)`
- `ssj554.2895.10259` `(pj)`

In these sentences, the parentheses are `punct` and the middle token is `root`. Both scripts ignore `punct` and `root` for MDD/NDD, so there are no valid dependency-distance arcs.

SyntComplex reports the undefined value as:

```text
MDD = n/a
NDD = n/a
```

STARK currently reports the same edge case as:

```text
MDD = 0.00
NDD = 0.00
```

## Conclusion

STARK matches SyntComplex for all normally measurable sentences and for all other complexity measures. The only discrepancy is the representation of undefined MDD/NDD when a sentence has no non-punctuation, non-root dependency arcs.

If exact output compatibility with SyntComplex is required, STARK should report `n/a` for MDD and NDD in this edge case instead of `0.00`.

Manual Excel check (git-ignored — regenerate with `python3 scripts/make_manual_check_files.py --split dev`):

`nh-work/complexity-comparison/outputs/manual-check/stark_vs_syntcomplex_manual_check_dev.xlsx`

Detailed QA report:

`nh-work/complexity-comparison/docs/QA_REPORT.md`
