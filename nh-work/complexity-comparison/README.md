# STARK vs SyntComplex Complexity Comparison

This workspace verifies STARK complexity measures against SyntComplex on the same official UD Slovenian SSJ dev file.

SyntComplex is an external reference from Luka Terčon's [`lukatercon/SyntComplex`](https://github.com/lukatercon/SyntComplex), not STARK code. The copied reference script under `external/SyntComplex/scripts/calculate_metrics.py` is kept unmodified. Precomputed SyntComplex result files from Luka's repo are intentionally omitted because they are not used in this verification.

## Folder Layout

- `configs/`: dedicated STARK config for this verification.
- `data/`: local corpus location. The `.conllu` file is ignored by git; see `data/README.md` for the exact source, hash, and download command.
- `docs/`: human-readable task summary and QA report.
- `external/`: pinned SyntComplex reference script.
- `outputs/`: saved STARK, SyntComplex, comparison, and manual-check outputs.
- `qa/`: independent QA rerun outputs.
- `scripts/`: wrappers and comparison/manual-check helpers.
- `MANIFEST.tsv`: source, command, hash, and output traceability log.

## Sources

- STARK checkout: [`b4c59799ab5fa4daa49d7a3a248bc2d75dec84e2`](https://github.com/hulln/STARK/commit/b4c59799ab5fa4daa49d7a3a248bc2d75dec84e2), version `3.2.0`.
- SyntComplex snapshot: [`lukatercon/SyntComplex`](https://github.com/lukatercon/SyntComplex) at commit [`bb0ba82ee5f9061ddd516de76b48c56fc7bfa682`](https://github.com/lukatercon/SyntComplex/commit/bb0ba82ee5f9061ddd516de76b48c56fc7bfa682).
- SyntComplex script: [`scripts/calculate_metrics.py`](https://github.com/lukatercon/SyntComplex/blob/bb0ba82ee5f9061ddd516de76b48c56fc7bfa682/scripts/calculate_metrics.py).
- Corpus: official [`UD_Slovenian-SSJ/sl_ssj-ud-dev.conllu`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/blob/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu) at commit [`212197db9aebc89dbdf8c1631f3fcc29b88840d4`](https://github.com/UniversalDependencies/UD_Slovenian-SSJ/commit/212197db9aebc89dbdf8c1631f3fcc29b88840d4).
- Corpus raw download: [`sl_ssj-ud-dev.conllu`](https://raw.githubusercontent.com/UniversalDependencies/UD_Slovenian-SSJ/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu).
- Corpus SHA-256: `2999a1ac8261df77e71c4e824c8e036e4845f84748f36d04bc7b730d7daf9d9a`.

The checked-in STARK sample `sample/sl_ssj-ud-dev.conllu` was not used because it differs from current official UD master (`22ac006f...`, 30,633 lines vs official `2999a1ac...`, 31,883 lines).

Before rerunning the tools, make sure the ignored local corpus file exists:

```bash
curl -L -o nh-work/complexity-comparison/data/sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu \
  https://raw.githubusercontent.com/UniversalDependencies/UD_Slovenian-SSJ/212197db9aebc89dbdf8c1631f3fcc29b88840d4/sl_ssj-ud-dev.conllu
```

## Commands

Run STARK:

```bash
python3 stark.py --config_file nh-work/complexity-comparison/configs/stark_complexity_sl_ssj_dev.ini
```

Run SyntComplex through the wrapper that creates its temporary hardcoded-path work directory:

```bash
python3 nh-work/complexity-comparison/scripts/run_syntcomplex_reference.py
```

Run comparison:

```bash
python3 nh-work/complexity-comparison/scripts/compare_stark_syntcomplex.py
```

Create Excel/manual-check files:

```bash
python3 nh-work/complexity-comparison/scripts/make_manual_check_files.py
```

## Outputs

- `outputs/stark/stark_sl_ssj_dev.tsv`
- `outputs/stark/stark_sl_ssj_dev_details.tsv`
- `outputs/syntcomplex/syntcomplex_sl_ssj_dev.tsv`
- `outputs/comparison/comparison_summary.tsv`
- `outputs/comparison/mismatches.tsv`
- `outputs/comparison/mismatches_first20.md`
- `outputs/manual-check/stark_vs_syntcomplex_manual_check.xlsx`
- `outputs/manual-check/manual_side_by_side.tsv`
- `outputs/manual-check/manual_side_by_side.csv`
- `outputs/manual-check/manual_mismatches_only.tsv`
- `scripts/run_syntcomplex_reference.py`
- `scripts/compare_stark_syntcomplex.py`
- `scripts/make_manual_check_files.py`
- `docs/TASK_SUMMARY.md`
- `docs/QA_REPORT.md`
- `MANIFEST.tsv`

## Manual Excel Check

For manual side-by-side checking, open:

`outputs/manual-check/stark_vs_syntcomplex_manual_check.xlsx`

The most useful sheet is `Manual side-by-side`. It has one row per sentence, in original corpus order, with STARK and SyntComplex values next to each other:

- `STARK MDD`
- `SyntComplex MDD raw`
- `SyntComplex MDD rounded like STARK`
- `MDD match?`
- equivalent columns for NDD, max depth, clauses, T-units, clauses/T-unit, and token count

Rows with `NO` in a match column are highlighted. The `Mismatches` sheet contains only the 10 mismatching metric rows.

If Excel import is preferred over the workbook, use:

- `outputs/manual-check/manual_side_by_side.tsv`
- `outputs/manual-check/manual_side_by_side.csv`

## Verdict

`FAIL`

Both tools produced and aligned 1250 sentence rows. All non-MDD/NDD measures match:

- `Max depth`: 1250/1250 match
- `N clauses`: 1250/1250 match
- `N T-units`: 1250/1250 match
- `Clauses/T-unit`: 1250/1250 match after STARK-style formatting
- `Number of nodes` sanity check: 1250/1250 match

The only differences are 5 sentences where SyntComplex returns `n/a` for MDD and NDD while STARK prints `0.00`, giving 10 metric mismatches total.

Affected sentence IDs:

- `ssj499.2651.9487`
- `ssj514.2725.9728`
- `ssj533.2814.10023`
- `ssj546.2865.10180`
- `ssj554.2895.10259`

These are punctuation-wrapped one-token fragments such as `( mu )`, where there are no non-punctuation, non-root dependency arcs. SyntComplex treats MDD/NDD as undefined (`n/a`); current STARK returns numeric zero for that case.

No STARK implementation changes were made in this workspace.
