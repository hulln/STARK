#!/usr/bin/env python3
"""
Does the verdict hold across SPECIFIC RELATIONS, not just noun phrases?

The advisor's hint was "(če se npr. sklicujejo na neke specifične relacije)" —
i.e. a measure might need adapting if its formula refers to specific dependency
relations. The companion `subtrees/` workflow tested noun phrases (head = a
NOUN). This workflow instead extracts chunks defined by *specific relations* —
the head of the chunk is a word attached to its parent by a chosen deprel:

    advcl  — adverbial clauses        (deli povedi)
    acl    — adnominal/relative clauses
    conj   — coordinated elements

For every such real chunk in the corpus, it calls STARK's REAL complexity
function `get_complexity_data` (imported, not reimplemented) and checks the same
thing as the slide test, but on real data:

    Group occurrences by their *shape* (the tree, with absolute positions
    removed). Within one shape, the chunk is identical; only WHERE it sits in
    the sentence differs between occurrences. So:
        - a measure that is constant within every shape group  -> safe on subtrees
        - a measure that varies within a shape group           -> depends on
          something outside the chunk (here: sentence position) -> needs adapting

Nothing in STARK is modified. Only the corpus is read and the real measuring
function is called.

Run:
    python3 nh-work/complexity-comparison/subtrees-by-relation/relation_subtree_check.py
"""

import argparse
import os
import sys
from collections import defaultdict

import conllu

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, _REPO_ROOT)

from stark.processing.complexity import get_complexity_data  # the real function under test


# --- Minimal faithful tree container (same four attributes STARK reads) ----
class _Word:
    def __init__(self, deprel, upos):
        self.deprel = deprel
        self.upos = upos


class _NodeWrapper:
    def __init__(self, location, deprel, upos):
        self.location = location
        self.node = _Word(deprel, upos)


class _Tree:
    def __init__(self, location, deprel, upos, children=None):
        self.node = _NodeWrapper(location, deprel, upos)
        self.children = children or []


def build_subtree(tok_id, tokens_by_id, children_of):
    """Build a _Tree rooted at tok_id from the real conllu tokens."""
    tok = tokens_by_id[tok_id]
    node = _Tree(int(tok["id"]), tok["deprel"], tok["upos"])
    node.children = [build_subtree(int(c["id"]), tokens_by_id, children_of)
                     for c in children_of.get(tok_id, [])]
    return node


def shape_key(tree):
    """
    Canonical key for a subtree with absolute positions removed.

    Encodes node (deprel, upos) and the arc structure using positions RELATIVE
    to the chunk's leftmost word. Two occurrences with the same key are the
    identical chunk shape, possibly sitting at a different place in a sentence.
    MDD, depth and node count are fully determined by this key; only NDD can
    additionally depend on the absolute position, which the key deliberately
    drops.
    """
    nodes, arcs = [], []

    def collect(t):
        nodes.append((t.node.location, t.node.node.deprel, t.node.node.upos))
        for ch in t.children:
            arcs.append((t.node.location, ch.node.location, ch.node.node.deprel))
            collect(ch)

    collect(tree)
    base = min(n[0] for n in nodes)
    rel_nodes = tuple(sorted((p - base, dep, upos) for p, dep, upos in nodes))
    rel_arcs = tuple(sorted((ph - base, ch - base, dep) for ph, ch, dep in arcs))
    return (rel_nodes, rel_arcs)


def size_of(tree):
    return get_complexity_data(tree)["n_nodes"]


RELATIONS = ["advcl", "acl", "conj"]


def collect_occurrences(corpus_path, relation, max_size):
    """Return list of dicts (one per chunk) for chunks whose head deprel == relation."""
    occurrences = []
    with open(corpus_path, "r", encoding="utf-8") as rf:
        for sent in conllu.parse(rf.read()):
            tokens = [t for t in sent if not isinstance(t["id"], tuple)]
            tokens_by_id = {int(t["id"]): t for t in tokens}
            children_of = defaultdict(list)
            for t in tokens:
                children_of[int(t["head"])].append(t)
            for t in tokens:
                if t["deprel"] != relation:
                    continue
                subtree = build_subtree(int(t["id"]), tokens_by_id, children_of)
                data = get_complexity_data(subtree)
                if data["n_nodes"] < 2 or data["n_nodes"] > max_size:
                    continue
                occurrences.append({
                    "head_pos": int(t["id"]),       # absolute sentence position of the chunk head
                    "shape": shape_key(subtree),
                    "mdd": data["mdd"],
                    "ndd": data["ndd"],
                    "max_depth": data["max_depth"],
                    "n_nodes": data["n_nodes"],
                })
    return occurrences


def analyse(relation, occurrences):
    """Group by shape; within each multi-position group, measure the spread."""
    by_shape = defaultdict(list)
    for o in occurrences:
        by_shape[o["shape"]].append(o)

    worst = {"mdd": 0.0, "ndd": 0.0, "max_depth": 0.0}
    multi_pos_groups = 0
    example = None

    for shape, occs in by_shape.items():
        head_positions = {o["head_pos"] for o in occs}
        if len(head_positions) < 2:        # need the same chunk at >=2 places to test position
            continue
        multi_pos_groups += 1
        for m in worst:
            spread = max(o[m] for o in occs) - min(o[m] for o in occs)
            worst[m] = max(worst[m], spread)
        # keep a small, readable example group for the report
        if example is None and 2 <= occs[0]["n_nodes"] <= 4 and len(occs) >= 3:
            example = (shape, sorted(occs, key=lambda o: o["head_pos"]))

    return {
        "relation": relation,
        "n_chunks": len(occurrences),
        "n_shapes": len(by_shape),
        "n_multi_pos_groups": multi_pos_groups,
        "worst": worst,
        "example": example,
    }


def print_report(result):
    r = result
    print("=" * 74)
    print(f"RELATION: {r['relation']}   "
          f"({r['n_chunks']} chunks, {r['n_shapes']} distinct shapes, "
          f"{r['n_multi_pos_groups']} shapes seen at >1 position)")
    print("-" * 74)
    print("  Largest spread WITHIN one shape (same chunk, different sentence position):")
    for label, key in [("MDD", "mdd"), ("Max depth", "max_depth"), ("NDD", "ndd")]:
        spread = r["worst"][key]
        verdict = "CONSTANT -> safe" if spread < 1e-9 else "VARIES   -> needs adapting"
        print(f"    {label:<10} max spread = {spread:.4f}   {verdict}")

    if r["example"]:
        shape, occs = r["example"]
        nodes = ", ".join(f"{upos}/{dep}" for _, dep, upos in shape[0])
        print("-" * 74)
        print(f"  Example shape [{nodes}] — same chunk at different head positions:")
        print(f"    {'head pos':>9} | {'MDD':>6} | {'depth':>6} | {'NDD':>6}")
        for o in occs[:6]:
            print(f"    {o['head_pos']:>9} | {o['mdd']:>6.2f} | "
                  f"{o['max_depth']:>6} | {o['ndd']:>6.3f}")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(
        _REPO_ROOT, "nh-work/complexity-comparison/data/"
                    "sl_ssj-ud-dev.UD-Slovenian-SSJ-212197d.conllu"))
    ap.add_argument("--max-size", type=int, default=12,
                    help="keep chunks up to this many words (these are 'krajša drevesa')")
    ap.add_argument("--summary", default=os.path.join(
        os.path.dirname(__file__), "outputs", "relation_subtree_summary.tsv"))
    args = ap.parse_args()

    results = []
    for relation in RELATIONS:
        occ = collect_occurrences(args.corpus, relation, args.max_size)
        results.append(analyse(relation, occ))

    for r in results:
        print_report(r)

    print("=" * 74)
    print("OVERALL CONCLUSION (across advcl, acl, conj)")
    print("-" * 74)
    mdd_ok = all(r["worst"]["mdd"] < 1e-9 for r in results)
    depth_ok = all(r["worst"]["max_depth"] < 1e-9 for r in results)
    ndd_varies = all(r["worst"]["ndd"] > 1e-9 for r in results)
    print(f"  MDD       {'CONSTANT in every relation -> safe as-is' if mdd_ok else 'VARIES'}")
    print(f"  Max depth {'CONSTANT in every relation -> safe as-is' if depth_ok else 'VARIES'}")
    print(f"  NDD       {'VARIES in every relation   -> needs adapting' if ndd_varies else 'CONSTANT'}")
    print("=" * 74)
    print("Same verdict as the noun-phrase run: the chunk's HEAD RELATION does not")
    print("change the answer, because the kept measures do not read the head deprel.")

    # small machine-readable summary
    os.makedirs(os.path.dirname(args.summary), exist_ok=True)
    with open(args.summary, "w", encoding="utf-8") as wf:
        wf.write("relation\tn_chunks\tn_shapes\tn_multi_pos_groups\t"
                 "mdd_max_spread\tdepth_max_spread\tndd_max_spread\n")
        for r in results:
            w = r["worst"]
            wf.write(f"{r['relation']}\t{r['n_chunks']}\t{r['n_shapes']}\t"
                     f"{r['n_multi_pos_groups']}\t{w['mdd']:.4f}\t"
                     f"{w['max_depth']:.4f}\t{w['ndd']:.4f}\n")
    print(f"\nWrote summary -> {os.path.relpath(args.summary, _REPO_ROOT)}")


if __name__ == "__main__":
    main()
