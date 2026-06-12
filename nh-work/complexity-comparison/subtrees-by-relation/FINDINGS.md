# Does the verdict hold across specific relations, not just noun phrases?

## Why this workflow exists

The advisor's hint was: a measure might need adapting *"če se npr. sklicujejo na
neke specifične relacije"* — if its formula refers to specific dependency
relations. The companion [`../subtrees/`](../subtrees/FINDINGS.md) workflow
tested **noun phrases** (chunks headed by a noun). This one tests chunks defined
by **specific relations**, to show the conclusion does not depend on which
relation we picked:

| Relation | What the chunk is |
|---|---|
| `advcl` | adverbial clauses (deli povedi) |
| `acl` | adnominal / relative clauses |
| `conj` | coordinated elements |

> First, the relevant background fact (from reading
> [`stark/processing/complexity.py`](../../../stark/processing/complexity.py)):
> of the measures we keep, **max depth and node count reference no relations at
> all**, and **MDD / NDD reference only `punct` and `root`** — and only to
> exclude them, which works the same on a phrase as on a sentence. The measures
> that are *stuffed* with specific relations (`csubj`, `advcl`, `conj`, …) are
> the **clause / T-unit** counts — which the advisor told us to skip. So the
> "specific relations" hint mostly describes the skipped measures. This
> workflow confirms, on real data, that the kept measures behave the same no
> matter which relation defines the chunk.

## What we did

**Part A — real per-occurrence check (the rigorous one).**
[`relation_subtree_check.py`](relation_subtree_check.py) reads the dev corpus,
finds every real chunk headed by `advcl` / `acl` / `conj`, and calls STARK's
**real** `get_complexity_data` on each one (imported, not reimplemented). It then
groups occurrences by **shape** (the tree with absolute positions removed) and
measures, within each shape, how much each measure moves. Same chunk shape =
identical chunk; the only thing that differs between occurrences is **where it
sits in the sentence**. So a measure that stays constant within a shape is safe;
one that moves is leaking sentence position.

**Part B — STARK-side corroboration.**
The same extraction was run through STARK's own pipeline with
`head = deprel=advcl` (then `acl`, `conj`) — see
[`stark_subtrees_by_relation.ini`](stark_subtrees_by_relation.ini). STARK
extracted the chunks and computed the measures with **no error** for all three
relations.

Nothing in STARK was changed in either part.

## Results

Largest spread of each measure **within one shape** (i.e. caused purely by the
chunk sitting in a different place), per relation:

| Relation | chunks | MDD spread | Max-depth spread | NDD spread |
|---|---:|---:|---:|---:|
| `advcl` | 179 | 0.0000 ✅ | 0.0000 ✅ | 1.0075 ⚠️ |
| `acl` | 317 | 0.0000 ✅ | 0.0000 ✅ | 0.7408 ⚠️ |
| `conj` | 1018 | 0.0000 ✅ | 0.0000 ✅ | 1.5890 ⚠️ |

(`✅` = never moves → safe; `⚠️` = moves → leaks sentence position.) Machine-
readable copy: [`outputs/relation_subtree_summary.tsv`](outputs/relation_subtree_summary.tsv).

A concrete real example (`conj` chunk `CCONJ/cc + NOUN/conj`) — identical chunk,
three sentence positions:

| head position | MDD | Max depth | NDD |
|---:|---:|---:|---:|
| 3 | 1.00 | 2 | 0.549 |
| 4 | 1.00 | 2 | 0.693 |
| 5 | 1.00 | 2 | 0.805 |

MDD and depth don't budge; NDD changes purely because the chunk is further into
the sentence. (NDD is a function of the head's absolute position, so it is not
position-invariant; it happens to climb monotonically here, but in general two
different positions can land on the same `|log(…)|` value — the point is only
that it depends on position at all, which is why it is unsafe on subtrees.)

## Conclusion

**Same verdict as the noun-phrase run, now confirmed across three specific
relations on real data:**

- **MDD, max depth, node count** — correct on shorter trees as-is.
- **NDD** — needs adapting (it leans on the chunk head's absolute sentence
  position).

And the deeper point answering the "specific relations" worry: the chunk's
**head relation does not change the answer**, because the kept measures never
read the head's deprel. Choosing `advcl` vs `acl` vs `conj` vs noun-phrase makes
no difference to which measure is safe. So we did not have to guess the "right"
relations to extract — the audit of the code plus this cross-relation check
together show the conclusion is relation-independent.

## Files

- `relation_subtree_check.py` — per-occurrence check across advcl/acl/conj
  (run: `python3 nh-work/complexity-comparison/subtrees-by-relation/relation_subtree_check.py`).
- `stark_subtrees_by_relation.ini` — base STARK config; override `--head deprel=<rel>` and `--output` per relation.
- `outputs/relation_subtree_summary.tsv` — the spread table above.
- `outputs/stark_{advcl,acl,conj}_dev.tsv` — STARK's own extraction of each relation, with measures.

## Independent check

A second model independently reproduced `relation_subtree_check.py` (summary
written to `/tmp`) and got the same spreads (MDD/depth = 0.0000; NDD spread
1.0075 / 0.7408 / 1.5890 for advcl / acl / conj), verified the CoNLL-U
extraction (tuple IDs skipped, 1-based `location`, 0 bad heads/IDs in dev), and
confirmed STARK was untouched. See the shared
[`../SUBTREE_REVIEW_PROMPT.md`](../SUBTREE_REVIEW_PROMPT.md); the two wording
refinements from that review (extraction depends on more than `head`; NDD is
position-dependent but can numerically coincide) are reflected above.
