# Copyright 2024 CJVT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

_CLAUSE_DEPRELS = frozenset({"csubj", "ccomp", "xcomp", "advcl", "acl", "conj", "parataxis"})
_T_UNIT_DEPRELS = frozenset({"conj", "parataxis"})
_EXCLUDED_DEPRELS = frozenset({"punct", "root"})


def _has_cop_child(rtn):
    """Return True if any direct child in the subtree carries deprel 'cop'."""
    return any(child.node.node.deprel == "cop" for child in rtn.children)


def get_complexity_data(repr_tree):
    """
    Compute per-occurrence syntactic complexity metrics for a matched subtree.

    Performs a single DFS over the RepresentationTree, collecting arc endpoint
    positions (for MDD/NDD), node count, max depth, and clause/T-unit counts.

    Intended to be called once per matched occurrence inside
    postprocess_query_results(); results are stored as running sums in
    summary.representation_trees and averaged at write time by
    Writer.get_complexity_measures().

    Metrics follow calculate_metrics.py (SyntComplex), adapted for subtrees:
      - MDD  : mean |head_pos - dep_pos| over non-punct arcs in the subtree
      - NDD  : |log(MDD / sqrt(root_pos * n_arcs))| (Jiang & Liu 2015)
               where n_arcs = number of non-punct arcs = number of
               non-punct, non-subtree-root nodes
      - max_depth : deepest level in the subtree (root = 1)
      - n_nodes   : total number of nodes in the subtree (incl. punct)
      - n_clauses : 1 + verbal clause-introducing dependents within the subtree
      - n_t_units : 1 + verbal conj/parataxis dependents within the subtree

    Note: has_cop_child only inspects children present in the extracted subtree;
    a copula outside the matched pattern will not be counted.

    :param repr_tree: RepresentationTree instance for one matched occurrence
    :return: dict with keys mdd, ndd, max_depth, n_nodes, n_clauses, n_t_units
    """
    arcs = []          # (parent_sentence_pos, child_sentence_pos) — punct excluded
    n_nodes = 0
    n_clauses = 1      # subtree root counts as the main predication
    n_t_units = 1

    def _traverse(rtn, depth):
        nonlocal n_nodes, n_clauses, n_t_units
        n_nodes += 1
        local_max = depth
        for child in rtn.children:
            deprel = child.node.node.deprel
            if deprel not in _EXCLUDED_DEPRELS:
                arcs.append((rtn.node.location, child.node.location))
            is_verbal = child.node.node.upos == "VERB" or _has_cop_child(child)
            if deprel in _CLAUSE_DEPRELS and is_verbal:
                n_clauses += 1
            if deprel in _T_UNIT_DEPRELS and is_verbal:
                n_t_units += 1
            local_max = max(local_max, _traverse(child, depth + 1))
        return local_max

    max_depth = _traverse(repr_tree, 1)

    # MDD — mean dependency distance over non-punct arcs
    mdd_val = sum(abs(p - c) for p, c in arcs) / len(arcs) if arcs else 0.0

    # NDD (Jiang & Liu 2015) — undefined for single-node or punct-only subtrees
    # n_arcs == number of non-punct nodes excluding the subtree root, which
    # mirrors "sentence_length" in the reference (non-punct, non-root tokens)
    root_pos = repr_tree.node.location
    n_arcs = len(arcs)
    if mdd_val > 0 and root_pos > 0 and n_arcs > 0:
        ndd_val = abs(math.log(mdd_val / math.sqrt(root_pos * n_arcs)))
    else:
        ndd_val = 0.0

    return {
        'mdd': mdd_val,
        'ndd': ndd_val,
        'max_depth': max_depth,
        'n_nodes': n_nodes,
        'n_clauses': n_clauses,
        'n_t_units': n_t_units,
    }
