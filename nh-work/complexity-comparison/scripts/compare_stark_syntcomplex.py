#!/usr/bin/env python3
import argparse
import csv
import math
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

METRICS = [
    {
        "name": "MDD",
        "stark": "MDD",
        "syntcomplex": "MDD",
        "kind": "float2",
        "complexity": True,
    },
    {
        "name": "NDD",
        "stark": "NDD",
        "syntcomplex": "NDD",
        "kind": "float2",
        "complexity": True,
    },
    {
        "name": "Max depth",
        "stark": "Max depth",
        "syntcomplex": "MAXIMUM_TREE_DEPTH",
        "kind": "int",
        "complexity": True,
    },
    {
        "name": "N clauses",
        "stark": "N clauses",
        "syntcomplex": "#_OF_CLAUSES",
        "kind": "float2",
        "complexity": True,
    },
    {
        "name": "N T-units",
        "stark": "N T-units",
        "syntcomplex": "#_OF_T-UNITS",
        "kind": "float2",
        "complexity": True,
    },
    {
        "name": "Clauses/T-unit",
        "stark": "Clauses/T-unit",
        "syntcomplex": "CLAUSES_PER_T-UNIT",
        "kind": "float2",
        "complexity": True,
    },
    {
        "name": "Number of nodes",
        "stark": "Number of nodes",
        "syntcomplex": "#_OF_TOKENS",
        "kind": "int",
        "complexity": False,
    },
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stark",
        default=BASE_DIR / "outputs/stark/stark_sl_ssj_dev.tsv",
        type=Path,
    )
    parser.add_argument(
        "--stark-details",
        default=BASE_DIR / "outputs/stark/stark_sl_ssj_dev_details.tsv",
        type=Path,
    )
    parser.add_argument(
        "--syntcomplex",
        default=BASE_DIR / "outputs/syntcomplex/syntcomplex_sl_ssj_dev.tsv",
        type=Path,
    )
    parser.add_argument(
        "--summary",
        default=BASE_DIR / "outputs/comparison/comparison_summary.tsv",
        type=Path,
    )
    parser.add_argument(
        "--mismatches",
        default=BASE_DIR / "outputs/comparison/mismatches.tsv",
        type=Path,
    )
    parser.add_argument(
        "--first20",
        default=BASE_DIR / "outputs/comparison/mismatches_first20.md",
        type=Path,
    )
    return parser.parse_args()


def read_stark_details(path):
    """Map each STARK tree key to the sentence ids that produced it.

    STARK aggregates identical trees, so one tree key can correspond to several
    sentences (legitimate, common on train/test). The details file is written as
    RAW tab-separated text and a tree string can start with a literal '"' (e.g. a
    one-token sentence that is just a quote), which csv.reader would mis-parse, so
    we split on tabs manually.
    """
    key_to_sids = {}
    with path.open(encoding="utf-8") as rf:
        for line in rf:
            row = line.rstrip("\n").split("\t")
            if len(row) < 2:
                continue
            key, sent_id = row[0], row[1]
            key_to_sids.setdefault(key, []).append(sent_id)
    duplicates = {k: v for k, v in key_to_sids.items() if len(v) > 1}
    return key_to_sids, duplicates


def read_stark_rows(path, key_to_sids):
    """Return sent_id -> STARK main row, covering every sentence.

    Each main row is keyed by both forms STARK may have written to the details
    file (`tree+order` and `(tree)order`); every sentence that shares an
    aggregated tree is mapped to that tree's row.
    """
    main_by_key = {}
    with path.open(newline="", encoding="utf-8") as rf:
        reader = csv.DictReader(rf, delimiter="\t")
        for row in reader:
            tree = row["Tree"]
            order = row.get("Order", "")
            main_by_key[tree + order] = row
            main_by_key[f"({tree}){order}"] = row
    rows_by_sent_id = {}
    unmatched = []
    for key, sids in key_to_sids.items():
        row = main_by_key.get(key)
        if row is None:
            unmatched.append(key)
            continue
        for sid in sids:
            rows_by_sent_id[sid] = row
    return rows_by_sent_id, unmatched


def read_syntcomplex_rows(path):
    rows = {}
    with path.open(newline="", encoding="utf-8") as rf:
        reader = csv.DictReader(rf, delimiter="\t")
        for row in reader:
            sent_id = row["SENT_ID"]
            if sent_id in rows:
                raise ValueError(f"Duplicate SyntComplex sentence id: {sent_id}")
            rows[sent_id] = row
    return rows


def is_na(value):
    return value is None or value.strip().lower() in {"", "n/a", "nan"}


def format_syntcomplex(value, kind):
    if is_na(value):
        return "n/a"
    numeric = float(value)
    if kind == "int":
        return str(int(round(numeric)))
    if kind == "float2":
        return f"{numeric:.2f}"
    raise ValueError(f"Unknown metric kind: {kind}")


def numeric_delta(stark_value, syntcomplex_value):
    if is_na(stark_value) or is_na(syntcomplex_value):
        return ""
    try:
        return f"{float(stark_value) - float(syntcomplex_value):.12g}"
    except ValueError:
        return ""


def mismatch_type(stark_value, syntcomplex_value, syntcomplex_formatted):
    if is_na(stark_value) != is_na(syntcomplex_value):
        return "na_vs_numeric"
    if stark_value != syntcomplex_formatted:
        return "formatted_mismatch"
    return ""


def compare_rows(stark_rows, syntcomplex_rows):
    all_sent_ids = sorted(set(stark_rows) | set(syntcomplex_rows))
    mismatches = []
    stats = {
        metric["name"]: {
            "total": 0,
            "matches": 0,
            "mismatches": 0,
            "na_mismatches": 0,
            "max_abs_delta_display_minus_raw": 0.0,
        }
        for metric in METRICS
    }

    for sent_id in all_sent_ids:
        stark_row = stark_rows.get(sent_id)
        syntcomplex_row = syntcomplex_rows.get(sent_id)
        if stark_row is None:
            mismatches.append(
                {
                    "sent_id": sent_id,
                    "metric": "<row>",
                    "stark_value": "<missing>",
                    "syntcomplex_value": "<present>",
                    "syntcomplex_formatted": "",
                    "delta_stark_display_minus_syntcomplex_raw": "",
                    "mismatch_type": "missing_in_stark",
                    "stark_tree": "",
                    "stark_example": "",
                }
            )
            continue
        if syntcomplex_row is None:
            mismatches.append(
                {
                    "sent_id": sent_id,
                    "metric": "<row>",
                    "stark_value": "<present>",
                    "syntcomplex_value": "<missing>",
                    "syntcomplex_formatted": "",
                    "delta_stark_display_minus_syntcomplex_raw": "",
                    "mismatch_type": "missing_in_syntcomplex",
                    "stark_tree": stark_row.get("Tree", ""),
                    "stark_example": stark_row.get("Example", ""),
                }
            )
            continue

        for metric in METRICS:
            stat = stats[metric["name"]]
            stat["total"] += 1
            stark_value = stark_row[metric["stark"]]
            syntcomplex_value = syntcomplex_row[metric["syntcomplex"]]
            syntcomplex_formatted = format_syntcomplex(
                syntcomplex_value, metric["kind"]
            )
            delta = numeric_delta(stark_value, syntcomplex_value)
            if delta:
                stat["max_abs_delta_display_minus_raw"] = max(
                    stat["max_abs_delta_display_minus_raw"],
                    abs(float(delta)),
                )
            current_mismatch_type = mismatch_type(
                stark_value, syntcomplex_value, syntcomplex_formatted
            )
            if not current_mismatch_type:
                stat["matches"] += 1
                continue
            stat["mismatches"] += 1
            if current_mismatch_type == "na_vs_numeric":
                stat["na_mismatches"] += 1
            mismatches.append(
                {
                    "sent_id": sent_id,
                    "metric": metric["name"],
                    "stark_value": stark_value,
                    "syntcomplex_value": syntcomplex_value,
                    "syntcomplex_formatted": syntcomplex_formatted,
                    "delta_stark_display_minus_syntcomplex_raw": delta,
                    "mismatch_type": current_mismatch_type,
                    "stark_tree": stark_row.get("Tree", ""),
                    "stark_example": stark_row.get("Example", ""),
                }
            )
    return stats, mismatches


def write_summary(path, stats, stark_rows, syntcomplex_rows, unmatched_stark, detail_duplicates):
    path.parent.mkdir(parents=True, exist_ok=True)
    complexity_metrics = [metric["name"] for metric in METRICS if metric["complexity"]]
    complexity_mismatches = sum(stats[name]["mismatches"] for name in complexity_metrics)
    common_count = len(set(stark_rows) & set(syntcomplex_rows))
    # Duplicate detail keys are legitimate: STARK aggregates identical trees, so
    # several sentences can share one tree (common on train/test). They are
    # reported for information but do not by themselves constitute a failure.
    verdict = (
        "PASS"
        if complexity_mismatches == 0
        and len(stark_rows) == len(syntcomplex_rows) == common_count
        and not unmatched_stark
        else "FAIL"
    )
    with path.open("w", newline="", encoding="utf-8") as wf:
        writer = csv.writer(wf, delimiter="\t")
        writer.writerow(["section", "metric", "value"])
        writer.writerow(["verdict", "status", verdict])
        writer.writerow(["rows", "stark_sentences", len(stark_rows)])
        writer.writerow(["rows", "syntcomplex_sentences", len(syntcomplex_rows)])
        writer.writerow(["rows", "common_sentences", common_count])
        writer.writerow(["rows", "unmatched_stark_rows", len(unmatched_stark)])
        writer.writerow(["rows", "duplicate_detail_keys", len(detail_duplicates)])
        for metric in METRICS:
            stat = stats[metric["name"]]
            writer.writerow(["metric", metric["name"], f"total={stat['total']}"])
            writer.writerow(["metric", metric["name"], f"matches={stat['matches']}"])
            writer.writerow(
                ["metric", metric["name"], f"mismatches={stat['mismatches']}"]
            )
            writer.writerow(
                ["metric", metric["name"], f"na_mismatches={stat['na_mismatches']}"]
            )
            writer.writerow(
                [
                    "metric",
                    metric["name"],
                    "max_abs_delta_display_minus_raw="
                    f"{stat['max_abs_delta_display_minus_raw']:.12g}",
                ]
            )
    return verdict


def write_mismatches(path, mismatches):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "sent_id",
        "metric",
        "stark_value",
        "syntcomplex_value",
        "syntcomplex_formatted",
        "delta_stark_display_minus_syntcomplex_raw",
        "mismatch_type",
        "stark_tree",
        "stark_example",
    ]
    with path.open("w", newline="", encoding="utf-8") as wf:
        writer = csv.DictWriter(wf, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for mismatch in mismatches:
            writer.writerow(mismatch)


def write_first20(path, mismatches, verdict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as wf:
        wf.write(f"# First 20 Mismatches\n\nVerdict: {verdict}\n\n")
        if not mismatches:
            wf.write("No mismatches found.\n")
            return
        for i, mismatch in enumerate(mismatches[:20], 1):
            wf.write(
                f"{i}. `{mismatch['sent_id']}` `{mismatch['metric']}` "
                f"STARK=`{mismatch['stark_value']}` "
                f"SyntComplex=`{mismatch['syntcomplex_value']}` "
                f"formatted=`{mismatch['syntcomplex_formatted']}` "
                f"type=`{mismatch['mismatch_type']}`\n"
            )


def main():
    args = parse_args()
    details, detail_duplicates = read_stark_details(args.stark_details)
    stark_rows, unmatched_stark = read_stark_rows(args.stark, details)
    syntcomplex_rows = read_syntcomplex_rows(args.syntcomplex)
    stats, mismatches = compare_rows(stark_rows, syntcomplex_rows)
    verdict = write_summary(
        args.summary,
        stats,
        stark_rows,
        syntcomplex_rows,
        unmatched_stark,
        detail_duplicates,
    )
    write_mismatches(args.mismatches, mismatches)
    write_first20(args.first20, mismatches, verdict)
    print(f"Verdict: {verdict}")
    print(f"STARK sentences: {len(stark_rows)}")
    print(f"SyntComplex sentences: {len(syntcomplex_rows)}")
    print(f"Mismatches: {len(mismatches)}")


if __name__ == "__main__":
    main()
