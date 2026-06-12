#!/usr/bin/env python3
"""
Subtree-level complexity check: which measures are safe on shorter trees?

Background (task): the existing verification ran complexity only on whole
sentences (config `head = deprel=root`). The new question is whether the
measures are still computed *correctly* when STARK extracts shorter trees
(parts of sentences, phrases), or whether some measure would have to be
adapted for that purpose.

Per the task, the clause / T-unit measures are intentionally NOT examined
(counting clauses inside a phrase is not meaningful). The "other" measures
STARK reports are: MDD, NDD, and max depth (plus node count as a sanity
cross-check). This script checks those.

Method — "same phrase, different position":
    A measure is *self-contained* (safe on subtrees) if its value depends
    only on the shape of the tree it is given. A measure *needs adapting*
    if its value also depends on something OUTSIDE the subtree — here, the
    subtree's absolute position in the sentence.

    So we take one identical phrase and place it at several absolute
    positions in a sentence, feed each version to the REAL STARK function
    `get_complexity_data`, and see which measures stay constant and which
    drift. Nothing is mocked except the tree container: the four attributes
    the function actually reads (node.location, node.node.deprel,
    node.node.upos, children) are reproduced exactly.

Run:
    python3 nh-work/complexity-comparison/subtrees/position_invariance_test.py
"""

import os
import sys

# Make the STARK package importable when run from the repo root.
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, _REPO_ROOT)

from stark.processing.complexity import get_complexity_data  # the real function under test


# --- Minimal faithful tree container -------------------------------------
# get_complexity_data() reads exactly these attributes off each tree node:
#   tree.node.location        (int)  absolute token position in the sentence
#   tree.node.node.deprel     (str)
#   tree.node.node.upos       (str)
#   tree.children             (list of the same kind of node)
# Nothing else is touched, so reproducing just these is faithful.

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


# --- Phrase builders: same shape, parametrised by start position ----------

def noun_phrase(start):
    """'the tall man' — DET(det) ADJ(amod) NOUN(head). Head is last word."""
    det = _Tree(start,     "det",  "DET")
    adj = _Tree(start + 1, "amod", "ADJ")
    return _Tree(start + 2, "obj",  "NOUN", [det, adj])  # head deprel is irrelevant to the measures


def small_clause(start):
    """'he runs fast' — PRON(nsubj) VERB(head) ADV(advmod)."""
    subj = _Tree(start,     "nsubj",  "PRON")
    verb_head = _Tree(start + 1, "advcl", "VERB")
    adv = _Tree(start + 2, "advmod", "ADV")
    verb_head.children = [subj, adv]
    return verb_head


PHRASES = [
    ("noun phrase  'the tall man'", noun_phrase),
    ("small clause 'he runs fast'", small_clause),
]

# Place each phrase at these absolute starting positions in the sentence.
START_POSITIONS = [1, 11, 51]


def fmt(x):
    return f"{x:.4f}" if isinstance(x, float) else str(x)


def main():
    measures = [("mdd", "MDD"), ("ndd", "NDD"),
                ("max_depth", "Max depth"), ("n_nodes", "Nodes")]

    overall_constant = {key: True for key, _ in measures}

    for title, build in PHRASES:
        print("=" * 72)
        print(title)
        print("-" * 72)
        header = f"{'start pos':>10} | " + " | ".join(f"{label:>10}" for _, label in measures)
        print(header)
        print("-" * 72)

        first_vals = None
        for start in START_POSITIONS:
            data = get_complexity_data(build(start))
            row_vals = [data[key] for key, _ in measures]
            print(f"{start:>10} | " + " | ".join(f"{fmt(v):>10}" for v in row_vals))

            if first_vals is None:
                first_vals = row_vals
            else:
                for (key, _), v0, v in zip(measures, first_vals, row_vals):
                    if abs(v - v0) > 1e-9:
                        overall_constant[key] = False

        # per-phrase verdict
        print("-" * 72)
        verdict = []
        for key, label in measures:
            vals = [get_complexity_data(build(s))[key] for s in START_POSITIONS]
            constant = max(vals) - min(vals) < 1e-9
            verdict.append(f"{label}: {'CONSTANT' if constant else 'VARIES'}")
        print("  " + "   ".join(verdict))
        print()

    print("=" * 72)
    print("CONCLUSION  (across all phrases above)")
    print("-" * 72)
    for key, label in measures:
        if overall_constant[key]:
            print(f"  {label:<10} CONSTANT across positions  -> safe on subtrees as-is")
        else:
            print(f"  {label:<10} VARIES with position       -> needs adapting for subtrees")
    print("=" * 72)
    print(
        "\nWhy: MDD, max depth and node count read only the shape of the tree\n"
        "they are given. NDD multiplies in the subtree root's ABSOLUTE sentence\n"
        "position (root_pos = repr_tree.node.location in complexity.py), so the\n"
        "same phrase scores differently depending on where it sits in the\n"
        "sentence. That extra-subtree dependency is the thing to decide on."
    )


if __name__ == "__main__":
    main()
