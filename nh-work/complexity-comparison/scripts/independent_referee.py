#!/usr/bin/env python3
"""Independent, third-party verification of the complexity measures.

This is a deliberately separate reimplementation: it parses the raw CoNLL-U
itself (no STARK code, no SyntComplex code) and computes all measures, then
compares its own per-sentence numbers against BOTH tools. It serves as a
referee so that "STARK == SyntComplex" is confirmed by a third calculation,
not just by the two tools agreeing with each other.

Two robustness details that matter on the full SSJ treebank (train/test, not
just dev):

  * STARK aggregates identical trees, so the main output can have fewer rows
    than sentences. We therefore map EVERY sentence to its STARK values through
    the details file, so aggregated duplicates are still fully compared.
  * STARK writes the details file as RAW tab-separated text; tree strings may
    start with a literal '"'. It is NOT csv-quoted, so the details file must be
    split on tabs manually (csv.reader would mis-parse quote-leading lines).

Usage:
    independent_referee.py --split SPLIT --corpus FILE \
        --stark FILE --stark-details FILE --syntcomplex FILE \
        [--summary FILE] [--mismatches FILE]
"""
import argparse
import csv
import math
from collections import Counter
from pathlib import Path

CLAUSE_DEPRELS = {"csubj", "ccomp", "xcomp", "advcl", "acl", "conj", "parataxis"}
TUNIT_DEPRELS = {"conj", "parataxis"}

MEASURES = ["MDD", "NDD", "maxdepth", "clauses", "tunits", "cpt", "ntokens"]
SYNT_COL = {"MDD": "MDD", "NDD": "NDD", "maxdepth": "MAXIMUM_TREE_DEPTH",
            "clauses": "#_OF_CLAUSES", "tunits": "#_OF_T-UNITS",
            "cpt": "CLAUSES_PER_T-UNIT", "ntokens": "#_OF_TOKENS"}
STARK_COL = {"MDD": "MDD", "NDD": "NDD", "maxdepth": "Max depth",
             "clauses": "N clauses", "tunits": "N T-units",
             "cpt": "Clauses/T-unit", "ntokens": "Number of nodes"}
INT_MEASURES = {"maxdepth", "ntokens"}


def parse_conllu(path):
    sents, meta, toks = [], {}, []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("#"):
            if line.startswith("# sent_id"):
                meta["sent_id"] = line.split("=", 1)[1].strip()
            continue
        if line == "":
            if toks:
                sents.append((meta.get("sent_id"), toks))
            meta, toks = {}, []
            continue
        c = line.split("\t")
        if "-" in c[0] or "." in c[0]:
            continue  # skip multiword-token ranges and empty nodes
        toks.append({"id": int(c[0]), "upos": c[3], "head": int(c[6]),
                     "deprel": c[7].split(":")[0]})
    if toks:
        sents.append((meta.get("sent_id"), toks))
    return sents


def has_cop(toks, tid):
    return any(t["deprel"] == "cop" and t["head"] == tid for t in toks)


def metrics(toks):
    dd = [abs(t["id"] - t["head"]) for t in toks
          if t["deprel"] not in ("punct", "root")]
    mdd = sum(dd) / len(dd) if dd else None
    if mdd is None:
        ndd = None
    else:
        root_id = next(t["id"] for t in toks if t["deprel"] == "root")
        ndd = abs(math.log(mdd / math.sqrt(root_id * len(dd))))
    byid = {t["id"]: t for t in toks}
    depths = []
    for t in toks:
        depth, cur, guard = 1, t["head"], 0
        while cur != 0:
            depth += 1
            cur = byid[cur]["head"]
            guard += 1
            if guard > len(toks) + 5:
                raise RuntimeError("dependency cycle")
        depths.append(depth)
    clauses = 1 + sum(1 for t in toks if t["deprel"] in CLAUSE_DEPRELS
                      and (t["upos"] == "VERB" or has_cop(toks, t["id"])))
    tunits = 1 + sum(1 for t in toks if t["deprel"] in TUNIT_DEPRELS
                     and (t["upos"] == "VERB" or has_cop(toks, t["id"])))
    return {"MDD": mdd, "NDD": ndd, "maxdepth": max(depths),
            "clauses": clauses, "tunits": tunits, "cpt": clauses / tunits,
            "ntokens": len(toks)}


def load_syntcomplex(path):
    return {r["SENT_ID"]: r
            for r in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t")}


def load_stark_per_sentid(main, details):
    by_key = {}
    for r in csv.DictReader(open(main, encoding="utf-8"), delimiter="\t"):
        tree, order = r["Tree"], r.get("Order", "")
        by_key[tree + order] = r
        by_key[f"({tree}){order}"] = r
    out, unmatched = {}, 0
    for line in open(details, encoding="utf-8"):  # RAW tabs, not csv-quoted
        row = line.rstrip("\n").split("\t")
        if len(row) < 2:
            continue
        key, sid = row[0], row[1]
        r = by_key.get(key)
        if r is None:
            unmatched += 1
            continue
        out[sid] = r
    return out, unmatched


def norm_mine(value, intish):
    if value is None:
        return "n/a"
    return str(int(round(value))) if intish else f"{value:.2f}"


def norm_syntcomplex(raw, intish):
    if raw is None or raw.strip().lower() in ("", "n/a", "nan"):
        return "n/a"
    return str(int(round(float(raw)))) if intish else f"{float(raw):.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True)
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--stark", type=Path, required=True)
    ap.add_argument("--stark-details", type=Path, required=True)
    ap.add_argument("--syntcomplex", type=Path, required=True)
    ap.add_argument("--summary", type=Path, default=None)
    ap.add_argument("--mismatches", type=Path, default=None)
    args = ap.parse_args()

    sents = parse_conllu(args.corpus)
    synt = load_syntcomplex(args.syntcomplex)
    stark, unmatched = load_stark_per_sentid(args.stark, args.stark_details)

    vs_stark = {m: [0, 0] for m in MEASURES}
    vs_synt = {m: [0, 0] for m in MEASURES}
    mismatches = []
    missing = 0
    for sid, toks in sents:
        mine = metrics(toks)
        s = synt.get(sid)
        k = stark.get(sid)
        if s is None or k is None:
            missing += 1
            continue
        for m in MEASURES:
            intish = m in INT_MEASURES
            ms = norm_mine(mine[m], intish)
            ss = norm_syntcomplex(s[SYNT_COL[m]], intish)
            ks = k[STARK_COL[m]].strip()
            if ms == ss:
                vs_synt[m][0] += 1
            else:
                vs_synt[m][1] += 1
            if ms == ks:
                vs_stark[m][0] += 1
            else:
                vs_stark[m][1] += 1
                kind = ("stark_na_reported_as_zero"
                        if ms == "n/a" and ks == "0.00" else "OTHER")
                mismatches.append({"sent_id": sid, "measure": m,
                                   "referee": ms, "stark": ks,
                                   "syntcomplex": ss, "type": kind})

    other = [x for x in mismatches if x["type"] == "OTHER"]
    edge_sents = sorted({x["sent_id"] for x in mismatches})

    print(f"[{args.split}] sentences={len(sents)} synt={len(synt)} "
          f"stark_mapped={len(stark)} unmatched_stark={unmatched} missing={missing}")
    print(f"{'measure':9}| ref==STARK (ok/bad) | ref==SyntComplex (ok/bad)")
    for m in MEASURES:
        a, b = vs_stark[m], vs_synt[m]
        print(f"{m:9}|  {a[0]:6}/{a[1]:<5}     |  {b[0]:6}/{b[1]:<5}")
    print(f"[{args.split}] edge-case sentences (STARK 0.00 vs reference n/a): "
          f"{len(edge_sents)}")
    print(f"[{args.split}] disagreements OTHER than that edge case: {len(other)}")

    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        with args.summary.open("w", newline="", encoding="utf-8") as wf:
            w = csv.writer(wf, delimiter="\t")
            w.writerow(["split", "metric", "value"])
            w.writerow([args.split, "sentences", len(sents)])
            w.writerow([args.split, "stark_mapped", len(stark)])
            w.writerow([args.split, "unmatched_stark", unmatched])
            w.writerow([args.split, "missing_rows", missing])
            w.writerow([args.split, "edge_case_sentences", len(edge_sents)])
            w.writerow([args.split, "other_disagreements", len(other)])
            for m in MEASURES:
                w.writerow([args.split, f"{m}_ref_vs_stark_match", vs_stark[m][0]])
                w.writerow([args.split, f"{m}_ref_vs_stark_mismatch", vs_stark[m][1]])
                w.writerow([args.split, f"{m}_ref_vs_synt_match", vs_synt[m][0]])
                w.writerow([args.split, f"{m}_ref_vs_synt_mismatch", vs_synt[m][1]])
    if args.mismatches:
        args.mismatches.parent.mkdir(parents=True, exist_ok=True)
        with args.mismatches.open("w", newline="", encoding="utf-8") as wf:
            w = csv.DictWriter(wf, fieldnames=["sent_id", "measure", "referee",
                                               "stark", "syntcomplex", "type"],
                               delimiter="\t")
            w.writeheader()
            for row in mismatches:
                w.writerow(row)


if __name__ == "__main__":
    main()
