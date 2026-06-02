# STARK vs SyntComplex Complexity Comparison

This workspace verifies STARK complexity measures against SyntComplex on the same official UD Slovenian SSJ data. The comparison covers the **dev**, **train**, and **test** splits (13,435 sentences in total), with an independent from-scratch reimplementation of the measures as a referee.

SyntComplex is an external reference from Luka Terčon's [`lukatercon/SyntComplex`](https://github.com/lukatercon/SyntComplex), not STARK code. The copied reference script under `external/SyntComplex/scripts/calculate_metrics.py` is kept unmodified. Precomputed SyntComplex result files from Luka's repo are intentionally omitted because they are not used in this verification.

All saved outputs are suffixed per split (`_dev`, `_train`, `_test`) so the three splits look identical in structure.

## Folder Layout

- `configs/`: dedicated STARK config for this verification.
- `data/`: local corpus location for the dev/train/test splits. The `.conllu` files are ignored by git; see `data/README.md` for sources, hashes, and download commands.
- `docs/`: human-readable summaries — `TASK_SUMMARY.md` and `QA_REPORT.md` (dev), `SSJ_TRAIN_TEST_RESULTS.md` (train/test extension).
- `external/`: pinned, unmodified SyntComplex reference script.
- `outputs/`: saved STARK, SyntComplex, comparison, and manual-check outputs, suffixed per split.
- `qa/`: a one-time dev reproducibility rerun (byte-for-byte identical to the saved dev outputs). The independent referee provides the equivalent cross-check for all splits.
- `scripts/`: tool wrappers and comparison/manual-check helpers (see below).
- `MANIFEST.tsv`: source, command, hash, and output traceability log.

## Scripts

- `run_syntcomplex_reference.py`: runs the unmodified SyntComplex reference on a chosen split (`--corpus`, default = dev) by recreating its hardcoded input paths in a temp dir.
- `compare_stark_syntcomplex.py`: the tool-vs-tool comparison — aligns STARK and SyntComplex by sentence id and reports matches/mismatches. Handles STARK tree aggregation (one tree shared by several sentences) and the raw-tab details format.
- `independent_referee.py`: an independent from-scratch reimplementation of the measures (no STARK/SyntComplex code), compared against both tools as a third opinion.
- `make_manual_check_files.py`: builds the human-readable side-by-side TSV/CSV and Excel workbook for a split.

## Sources

- STARK checkout: [`b4c59799ab5fa4daa49d7a3a248bc2d75dec84e2`](https://github.com/hulln/STARK/commit/b4c59799ab5fa4daa49d7a3a248bc2d75dec84e2), version `3.2.0`.
- SyntComplex snapshot: [`lukatercon/SyntComplex`](https://github.com/lukatercon/SyntComplex) at commit [`bb0ba82ee5f9061ddd516de76b48c56fc7bfa682`](https://github.com/lukatercon/SyntComplex/commit/bb0ba82ee5f9061ddd516de76b48c56fc7bfa682).
- SyntComplex script: [`scripts/calculate_metrics.py`](https://github.com/lukatercon/SyntComplex/blob/bb0ba82ee5f9061ddd516de76b48c56fc7bfa682/scripts/calculate_metrics.py).
- Corpus: official [`UD_Slovenian-SSJ/sl_ssj-ud-dev.conllu`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/blob/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu) at commit [`212197db9aebc89dbdf8c1631f3fcc29b88840d4`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/commit/212197db9aebc89dbdf8c1631f3fcc29b88840d4).
- Corpus raw download: [`sl_ssj-ud-dev.conllu`](https://raw.githubusercontent.com/UniversalDependencies/UD_Slovenian-SSJ/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu).
- Corpus SHA-256 (dev): `2999a1ac8261df77e71c4e824c8e036e4845f84748f36d04bc7b730d7daf9d9a`.
- Train and test splits of the same treebank are used as well; see `data/README.md` for their hashes and download commands. All three splits are byte-identical between the dev pin `212197db…` and current UD master `17011b12…`.

The checked-in STARK sample `sample/sl_ssj-ud-dev.conllu` was not used because it differs from current official UD master (`22ac006f...`, 30,633 lines vs official `2999a1ac...`, 31,883 lines).

Before rerunning the tools, make sure the ignored local corpus file exists:

```bash
curl -L -o nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu \
  https://raw.githubusercontent.com/UniversalDependencies/UD_Slovenian-SSJ/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu
```

## Commands

Run the full pipeline on a split (replace `dev` with `train` or `test`):

```bash
# STARK
python3 stark.py --config_file nh-work/complexity-comparison/configs/stark_complexity_sl_ssj_dev.ini \
  --input  nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu \
  --output nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_dev.tsv \
  --detailed_results_file nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_dev_details.tsv

# SyntComplex (unmodified reference)
python3 nh-work/complexity-comparison/scripts/run_syntcomplex_reference.py \
  --corpus nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu \
  --output nh-work/complexity-comparison/outputs/syntcomplex/syntcomplex_sl_ssj_dev.tsv

# Tool-vs-tool comparison
python3 nh-work/complexity-comparison/scripts/compare_stark_syntcomplex.py \
  --stark         nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_dev.tsv \
  --stark-details nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_dev_details.tsv \
  --syntcomplex   nh-work/complexity-comparison/outputs/syntcomplex/syntcomplex_sl_ssj_dev.tsv \
  --summary    nh-work/complexity-comparison/outputs/comparison/comparison_summary_dev.tsv \
  --mismatches nh-work/complexity-comparison/outputs/comparison/mismatches_dev.tsv \
  --first20    nh-work/complexity-comparison/outputs/comparison/mismatches_first20_dev.md

# Independent referee (third check)
python3 nh-work/complexity-comparison/scripts/independent_referee.py --split dev \
  --corpus nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu \
  --stark  nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_dev.tsv \
  --stark-details nh-work/complexity-comparison/outputs/stark/stark_sl_ssj_dev_details.tsv \
  --syntcomplex   nh-work/complexity-comparison/outputs/syntcomplex/syntcomplex_sl_ssj_dev.tsv \
  --summary    nh-work/complexity-comparison/outputs/comparison/referee_summary_dev.tsv \
  --mismatches nh-work/complexity-comparison/outputs/comparison/referee_mismatches_dev.tsv

# Human-readable side-by-side (TSV/CSV/Excel)
python3 nh-work/complexity-comparison/scripts/make_manual_check_files.py --split dev
```

## Outputs

Per split (`<split>` = `dev`, `train`, `test`):

- `outputs/stark/stark_sl_ssj_<split>.tsv`, `…_<split>_details.tsv`
- `outputs/syntcomplex/syntcomplex_sl_ssj_<split>.tsv`
- `outputs/comparison/comparison_summary_<split>.tsv`, `mismatches_<split>.tsv`, `mismatches_first20_<split>.md`
- `outputs/comparison/referee_summary_<split>.tsv`, `referee_mismatches_<split>.tsv`
- `outputs/manual-check/manual_side_by_side_<split>.tsv` / `.csv`, `manual_mismatches_only_<split>.tsv`, `stark_vs_syntcomplex_manual_check_<split>.xlsx`

Scripts and docs:

- `scripts/run_syntcomplex_reference.py`, `scripts/compare_stark_syntcomplex.py`, `scripts/independent_referee.py`, `scripts/make_manual_check_files.py`
- `docs/TASK_SUMMARY.md`, `docs/QA_REPORT.md`, `docs/SSJ_TRAIN_TEST_RESULTS.md`
- `MANIFEST.tsv`

## Manual Excel Check

For manual side-by-side checking, open the workbook for the split you want, e.g. for dev:

`outputs/manual-check/stark_vs_syntcomplex_manual_check_dev.xlsx`

The most useful sheet is `Manual side-by-side`. It has one row per sentence, in original corpus order, with STARK and SyntComplex values next to each other:

- `STARK MDD`
- `SyntComplex MDD raw`
- `SyntComplex MDD rounded like STARK`
- `MDD match?`
- equivalent columns for NDD, max depth, clauses, T-units, clauses/T-unit, and token count

Rows with `NO` in a match column are highlighted. The `Mismatches` sheet contains only the mismatching metric rows (all of them the `0.00`-vs-`n/a` edge case).

The `dev` and `test` side-by-side files (TSV/CSV/Excel) are committed. The `train` side-by-side and Excel are large (~20 MB, 10,903 rows) and are **git-ignored — regenerate them on demand**:

```bash
python3 nh-work/complexity-comparison/scripts/make_manual_check_files.py --split train
```

For quick scanning of dev/test, the TSV/CSV are usually easier than the workbook:

- `outputs/manual-check/manual_side_by_side_<split>.tsv`
- `outputs/manual-check/manual_side_by_side_<split>.csv`

## Verdict

**MATCH — with one documented edge-case difference, across the whole SSJ treebank.**

STARK reproduces the SyntComplex reference (and an independent referee) on every complexity measure for every sentence in dev, train, and test. The single exception is the representation of an *undefined* MDD/NDD: when a sentence has no non-punctuation, non-root dependency arcs (short fragments such as `(mu)`, or a lone `"`), MDD is mathematically undefined. SyntComplex and the referee print `n/a`; STARK prints `0.00`. This is a representation choice, not a calculation error.

| Split | Sentences | Measures matching | Edge-case sentences (STARK `0.00` vs `n/a`) |
|---|---:|---|---:|
| dev | 1250 | all 5 (+ token count) | 5 |
| train | 10903 | all 5 (+ token count) | 90 |
| test | 1282 | all 5 (+ token count) | 3 |

Strict byte-equality status (the machine verdict in each `comparison_summary_<split>.tsv`): `FAIL`, driven solely by those `0.00`-vs-`n/a` cells. If exact parity is required, STARK should print `n/a` for MDD/NDD when there are no non-punctuation, non-root arcs.

See `docs/SSJ_TRAIN_TEST_RESULTS.md` for the full train/test breakdown and `docs/TASK_SUMMARY.md` for the dev write-up.

No STARK implementation changes were made in this workspace.
