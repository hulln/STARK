# QA Report: STARK vs SyntComplex Complexity Comparison

QA rerun time: `2026-06-02T12:08:31+02:00`

This report double-checks that the STARK/SyntComplex comparison was run precisely, on the same data, and reproducibly.

## Source Links

- STARK checkout: [`b4c59799ab5fa4daa49d7a3a248bc2d75dec84e2`](https://github.com/hulln/STARK/commit/b4c59799ab5fa4daa49d7a3a248bc2d75dec84e2), version `3.2.0`
- SyntComplex reference: Luka Terčon's [`lukatercon/SyntComplex`](https://github.com/lukatercon/SyntComplex) at commit [`bb0ba82ee5f9061ddd516de76b48c56fc7bfa682`](https://github.com/lukatercon/SyntComplex/commit/bb0ba82ee5f9061ddd516de76b48c56fc7bfa682)
- SyntComplex script: [`scripts/calculate_metrics.py`](https://github.com/lukatercon/SyntComplex/blob/bb0ba82ee5f9061ddd516de76b48c56fc7bfa682/scripts/calculate_metrics.py)
- Corpus source file: [`UD_Slovenian-SSJ/sl_ssj-ud-dev.conllu`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/blob/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu)
- Corpus commit: [`212197db9aebc89dbdf8c1631f3fcc29b88840d4`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/commit/212197db9aebc89dbdf8c1631f3fcc29b88840d4)

## What Was Rerun

I reran both tools in a separate QA folder, without deleting or overwriting the original saved outputs:

`qa/20260602-qa-rerun/`

The QA rerun used the same pinned official UD SSJ dev file:

`data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu`

Corpus SHA-256:

`2999a1ac8261df77e71c4e824c8e036e4845f84748f36d04bc7b730d7daf9d9a`

Sentence count:

`1250`

## STARK Rerun

STARK was rerun with the same dedicated config:

`configs/stark_complexity_sl_ssj_dev.ini`

Important settings:

```ini
input = nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu
size = 1-10000
head = deprel=root
complexity_measures = yes
example = yes
greedy_counter = yes
complete = yes
```

QA command:

```bash
python3 stark.py \
  --config_file nh-work/complexity-comparison/configs/stark_complexity_sl_ssj_dev.ini \
  --output nh-work/complexity-comparison/qa/20260602-qa-rerun/stark/stark_sl_ssj_dev.tsv \
  --detailed_results_file nh-work/complexity-comparison/qa/20260602-qa-rerun/stark/stark_sl_ssj_dev_details.tsv
```

QA result:

- `1250` unique root trees
- `1251` lines in STARK main TSV: header + 1250 rows
- `1250` lines in STARK details TSV

## SyntComplex Rerun

SyntComplex was rerun from a generated temporary QA work copy:

`qa/20260602-qa-rerun/work/syntcomplex-run/`

That temporary hardcoded-path work copy was removed during cleanup. The preserved QA outputs are under:

`qa/20260602-qa-rerun/syntcomplex/`

The same official corpus file was copied to SyntComplex's hardcoded expected path:

`UD_Slovenian-SSJ-master/sl_ssj-ud-dev.conllu`

The copied file has the same SHA-256 as the STARK input:

`2999a1ac8261df77e71c4e824c8e036e4845f84748f36d04bc7b730d7daf9d9a`

The other hardcoded SyntComplex input files were empty placeholders, so only SSJ dev contributed rows.

QA command:

```bash
cd nh-work/complexity-comparison/qa/20260602-qa-rerun/work/syntcomplex-run
python3 scripts/calculate_metrics.py
```

The committed wrapper for recreating this setup is:

```bash
python3 nh-work/complexity-comparison/scripts/run_syntcomplex_reference.py
```

QA result:

- `1251` lines in SyntComplex output: header + 1250 rows

## Reproducibility Checks

The QA rerun outputs are byte-for-byte identical to the original saved outputs.

| File | Original SHA-256 | QA rerun SHA-256 | Result |
|---|---|---|---|
| STARK main output | `af0f2fda63d84dc00959e15cab5295630781385eca7b06d0d48f7fd7610b1bb8` | `af0f2fda63d84dc00959e15cab5295630781385eca7b06d0d48f7fd7610b1bb8` | identical |
| SyntComplex output | `b0384dc022958f91890b25fede77f88049d84a0c0f061a1ab52f55edb84fc90d` | `b0384dc022958f91890b25fede77f88049d84a0c0f061a1ab52f55edb84fc90d` | identical |
| mismatch table | `5109e74c6bfb8d838d8a99842d6befffc9e7cd720c1578b51a9daef558f3110e` | `5109e74c6bfb8d838d8a99842d6befffc9e7cd720c1578b51a9daef558f3110e` | identical |

## Comparison Result

Verdict remains:

`FAIL`

But the failure is narrow and fully explained.

Aligned rows:

- STARK sentences: `1250`
- SyntComplex sentences: `1250`
- Common sentence IDs: `1250`
- Unmatched STARK rows: `0`
- Duplicate STARK detail keys: `0`

Metric results:

| Metric | Matches | Mismatches |
|---|---:|---:|
| MDD | 1245/1250 | 5 |
| NDD | 1245/1250 | 5 |
| Max depth | 1250/1250 | 0 |
| N clauses | 1250/1250 | 0 |
| N T-units | 1250/1250 | 0 |
| Clauses/T-unit | 1250/1250 | 0 |
| Number of nodes sanity check | 1250/1250 | 0 |

## Mismatching Sentences

The five affected sentences are:

| sent_id | text | STARK | SyntComplex |
|---|---|---|---|
| `ssj499.2651.9487` | `(mu)` | MDD/NDD `0.00` | MDD/NDD `n/a` |
| `ssj514.2725.9728` | `(fl)` | MDD/NDD `0.00` | MDD/NDD `n/a` |
| `ssj533.2814.10023` | `(jo)` | MDD/NDD `0.00` | MDD/NDD `n/a` |
| `ssj546.2865.10180` | `(sta)` | MDD/NDD `0.00` | MDD/NDD `n/a` |
| `ssj554.2895.10259` | `(pj)` | MDD/NDD `0.00` | MDD/NDD `n/a` |

Each has the same structure:

```conllu
1   (      PUNCT   head=2   deprel=punct
2   token  X       head=0   deprel=root
3   )      PUNCT   head=2   deprel=punct
```

Both scripts exclude `punct` and `root` when calculating MDD/NDD. Therefore these sentences have zero valid dependency-distance arcs.

SyntComplex treats this as undefined:

```text
MDD = n/a
NDD = n/a
```

STARK currently treats this as zero:

```text
MDD = 0.00
NDD = 0.00
```

## QA Conclusion

The task was carried out correctly and reproducibly:

- Both tools were run on the same official corpus file.
- The QA rerun reproduced the original outputs byte-for-byte.
- All sentence IDs align.
- All non-MDD/NDD metrics match completely.
- MDD/NDD match for all normal sentences.
- The only discrepancy is an edge-case representation difference: undefined MDD/NDD are `n/a` in SyntComplex but `0.00` in STARK.

Recommended interpretation:

STARK's implementation agrees with SyntComplex for normal measurable sentences, but STARK likely needs a small fix if it should exactly reproduce SyntComplex output semantics: return/report `n/a` for MDD and NDD when there are no non-punctuation, non-root dependency arcs.
