# STARK vs SyntComplex — extended to SSJ train and test

Date: 2026-06-02

The original verification compared STARK and SyntComplex on the SSJ **dev** split
(1250 sentences). This document extends the same comparison to the **train** and
**test** splits of the same treebank, and adds an independent third
reimplementation of the measures as a referee.

## Data

All three splits were obtained online from UD, the same way as the dev file. The
files are byte-identical between the dev pin `212197db…` and current UD master
`17011b12…`, so they are simultaneously the latest version and consistent with
the dev comparison. See `data/README.md` for hashes and download commands.

| Split | Sentences | SHA-256 (corpus) |
|---|---:|---|
| dev | 1250 | `2999a1ac…d9d9a` |
| train | 10903 | `c6991732…57243` |
| test | 1282 | `c14d5d2f…c8b0` |

## Commands (reproducible)

STARK (same dedicated dev config; only `--input`/`--output` change per split):

```bash
python3 stark.py --config_file nh-work/complexity-comparison/configs/stark_complexity_sl_ssj_dev.ini \
  --input  nh-work/complexity-comparison/data/sl_ssj-ud-train.UD-Slovenian-SSJ-212197d.conllu \
  --output nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_train.tsv \
  --detailed_results_file nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_train_details.tsv
# ...and the same with test in place of train.
```

SyntComplex (reference script unmodified; the workspace wrapper now accepts
`--corpus`, default = dev, so the dev run is unchanged):

```bash
python3 nh-work/complexity-comparison/scripts/run_syntcomplex_reference.py \
  --corpus nh-work/complexity-comparison/data/sl_ssj-ud-train.UD-Slovenian-SSJ-212197d.conllu \
  --output nh-work/complexity-comparison/outputs/syntcomplex/syntcomplex_sl_ssj_train.tsv
```

Independent referee + per-split comparison files:

```bash
python3 nh-work/complexity-comparison/scripts/independent_referee.py --split train \
  --corpus       nh-work/complexity-comparison/data/sl_ssj-ud-train.UD-Slovenian-SSJ-212197d.conllu \
  --stark        nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_train.tsv \
  --stark-details nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_train_details.tsv \
  --syntcomplex  nh-work/complexity-comparison/outputs/syntcomplex/syntcomplex_sl_ssj_train.tsv \
  --summary      nh-work/complexity-comparison/outputs/comparison/referee_summary_train.tsv \
  --mismatches   nh-work/complexity-comparison/outputs/comparison/referee_mismatches_train.tsv
```

## Saved files (committed vs regenerate-on-demand)

To keep the repo light, the small comparison/referee tables are committed
(`outputs/comparison/`), while the bulky, fully-regenerable artifacts are
git-ignored: the raw STARK `train`/`test` outputs and everything under
`outputs/manual-check/`. Recreate them with the commands above (or, for the
side-by-side/Excel, `make_manual_check_files.py --split <split>`). The MANIFEST
lists every file with its hash, including the git-ignored ones.

## Row counts

| Split | STARK main rows | STARK detail lines | SyntComplex rows | Sentences |
|---|---:|---:|---:|---:|
| dev | 1250 | 1250 | 1250 | 1250 |
| train | 10861 | 10903 | 10903 | 10903 |
| test | 1281 | 1282 | 1282 | 1282 |

STARK aggregates identical trees, so on train/test the **main** output has fewer
rows than sentences (10861 vs 10903; 1281 vs 1282). No sentence is dropped: the
**details** file still has one line per sentence, and the comparison maps every
sentence to its STARK values through that details file.

## Results — three-way comparison, all sentences

Independent referee (a from-scratch reimplementation, no STARK/SyntComplex code)
compared against both tools, per sentence:

| Split | Measure | referee == STARK | referee == SyntComplex |
|---|---|---:|---:|
| dev | MDD, NDD | 1245 / 1250 | **1250 / 1250** |
| dev | max depth, clauses, T-units, clauses/T-unit, tokens | **1250 / 1250** | **1250 / 1250** |
| train | MDD, NDD | 10813 / 10903 | **10903 / 10903** |
| train | max depth, clauses, T-units, clauses/T-unit, tokens | **10903 / 10903** | **10903 / 10903** |
| test | MDD, NDD | 1279 / 1282 | **1282 / 1282** |
| test | max depth, clauses, T-units, clauses/T-unit, tokens | **1282 / 1282** | **1282 / 1282** |

The referee matches **SyntComplex on every measure for every sentence in all
three splits**, and matches **STARK on everything except MDD/NDD in a small set
of degenerate sentences**. Disagreements that are anything **other than** the one
known edge case: **0** in every split.

## The only discrepancy (same edge case as dev, at larger scale)

The sole difference is the representation of an **undefined** MDD/NDD: when a
sentence has no non-punctuation, non-root dependency arcs, MDD is mathematically
undefined. SyntComplex and the independent referee report `n/a`; STARK reports
`0.00`.

| Split | Edge-case sentences | MDD+NDD cells |
|---|---:|---:|
| dev | 5 | 10 |
| train | 90 | 180 |
| test | 3 | 6 |
| **total** | **98** | **196** |

These are short fragments such as `(mu)`, `(fl)` (parentheses are `punct`, the
middle token is `root`) and lone-punctuation sentences such as a single `"`
(which is both `punct` and `root`). Per-sentence detail is in
`outputs/comparison/referee_mismatches_{dev,train,test}.tsv`; all rows are
classified `stark_na_reported_as_zero`.

## Notes for whoever evaluates STARK

1. **STARK's calculations are correct.** Across the entire SSJ treebank
   (13,435 sentences), STARK agrees with both SyntComplex and an independent
   reimplementation on all six complexity measures — MDD, NDD, maximum tree
   depth, number of clauses, number of T-units, and clauses per T-unit — plus
   the word-count cross-check, for every sentence, with the single exception of
   how it prints an undefined MDD/NDD.

2. **The one fix to consider in STARK:** print `n/a` (or empty) for MDD and NDD
   when there are no non-punctuation, non-root arcs, instead of `0.00`. This is a
   reporting choice, not a calculation error.

3. **Comparison-tooling fix (not a STARK issue):** STARK writes the *details*
   file as raw tab-separated text, and a tree can start with a literal `"`;
   parsing it with a CSV reader mis-handles those lines, and the original helper
   also assumed one tree maps to exactly one sentence (untrue on train/test,
   where STARK aggregates identical trees). Both `compare_stark_syntcomplex.py`
   and `independent_referee.py` now parse the details file with raw tab splitting
   and expand every sentence through it, so all sentences are compared correctly
   on every split. This was found and fixed during this extension.

## Verdict

STARK matches the SyntComplex reference (and an independent third
implementation) on all six complexity measures (MDD, NDD, maximum tree depth,
number of clauses, number of T-units, clauses per T-unit) across SSJ train, dev,
and test, for every sentence. The only deviation is the cosmetic `0.00`-vs-`n/a`
representation of undefined MDD/NDD in 98 degenerate sentences.
