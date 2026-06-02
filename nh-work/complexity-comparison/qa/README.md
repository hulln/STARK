# QA rerun (dev reproducibility snapshot)

`20260602-qa-rerun/` is a one-time, point-in-time rerun of the **dev** pipeline,
kept to prove the saved dev outputs are reproducible. Its files are byte-for-byte
identical to the corresponding committed dev outputs (see `docs/QA_REPORT.md`).

It is intentionally **dev-only** and uses the original (pre-unification) file
names. It is not regenerated for train/test: the independent referee
(`scripts/independent_referee.py`, with `referee_summary_*` / `referee_mismatches_*`
outputs) provides the equivalent independent cross-check for all three splits.
