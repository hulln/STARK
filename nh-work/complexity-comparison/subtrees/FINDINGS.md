# Do STARK's complexity measures work on smaller chunks, not just whole sentences?

## The question, in plain words

STARK can measure how grammatically "complex" a piece of text is. Until now it
only did this for **whole sentences**. The task: check whether the measures are
still correct when STARK looks at **smaller chunks** — phrases / parts of
sentences (e.g. "the tall man") — or whether some measure has to be **adapted**
for that.

We were told to **skip the "clause" and "T-unit" counts**, because counting
clauses inside a single phrase is meaningless. So we checked the rest.

## The measures, one line each

- **Node count** — how many words are in the chunk.
- **Max depth** — how many layers the grammar tree has (boss word → the words
  under it → the words under those …).
- **MDD** — on average, how far apart two grammatically-connected words are.
  It's about the **gap between connected words**.
- **NDD** — MDD pushed through an extra formula that *also* mixes in **where the
  chunk sits in the sentence**.

## How we checked it

**Check 1 — slide the same phrase around (made-up examples).**
We took one phrase, e.g. "the tall man", and placed it at different spots in a
sentence (starting at word 1, then word 11, then word 51). We asked STARK's real
measuring code for the numbers each time.

The idea: a phrase's complexity should NOT change just because it appears later
in a sentence. So if a measure changes when we slide the same phrase along, that
measure is secretly depending on something *outside* the phrase → it needs
fixing.

**Check 2 — real Slovenian phrases (real corpus run).**
We ran STARK on the real dev corpus, but told it (via the config's `head`
setting) to pull out **noun phrases** (chunks headed by a noun, 2–6 words long)
instead of whole sentences. It found **762 different phrase shapes** and computed
every measure with **no error** — proving it works on real shorter trees, not
just made-up ones.

> Nothing in the STARK tool was changed for any of this — only a copied config
> file, where `head = deprel=root` (whole sentences) became `head = upos=NOUN`
> (noun phrases), with `size` set to keep the trees short. (Which trees get
> extracted is governed by several settings — `head`, `size`, `complete`,
> queries — not `head` alone; the complexity function itself is agnostic to all
> of them.)

## What we found

| Measure | On smaller chunks | Verdict |
|---|---|---|
| **Node count** | same no matter where the chunk is | ✅ fine as-is |
| **Max depth** | same no matter where the chunk is | ✅ fine as-is |
| **MDD** | same no matter where the chunk is | ✅ fine as-is |
| **NDD** | **changes** when the same chunk moves | ⚠️ **needs adapting** |
| Clauses / T-units / Clauses-per-T-unit | — | skipped (meaningless below sentence level) |

Here is the slide test for the phrase "the tall man" — same phrase, three
positions:

| where the phrase starts | MDD | NDD | Max depth | Nodes |
|---:|---:|---:|---:|---:|
| word 1 | 1.50 | **0.49** | 2 | 3 |
| word 11 | 1.50 | **1.22** | 2 | 3 |
| word 51 | 1.50 | **1.93** | 2 | 3 |

MDD, depth and node count don't move. NDD does — same phrase, different score,
purely from sitting elsewhere. (Strictly: NDD is a function of the head's
absolute position, so it is **not** position-invariant. It won't differ for
*every* pair of positions — the `|log(…)|` formula can land on the same value
for particular position pairs — but it is position-dependent, so it is not safe
on subtrees as-is.)

## Why MDD is fine but NDD isn't (the key idea)

Both use word positions — but in **different ways**:

- **MDD uses the GAP between two words** ("word #3 minus word #1 = 2 apart").
  That's a subtraction. If you slide the whole phrase 10 words to the right,
  *both* words move together, so the gap is still 2. **Gaps don't care where you
  are, only how far apart things are.**
- **NDD uses the head word's actual POSITION NUMBER** ("the head is the 3rd
  word"). That single number changes the instant you move the phrase (3 → 13),
  so NDD changes too.

Picture two people holding a rope: MDD is the rope's *length* (unchanged if they
both walk right together); NDD also asks *"how far is one of them from the
door"* — and that changes when they walk. Same rope, different door-distance.

## The one to fix: NDD

NDD's formula is `| ln( MDD ÷ √(position-of-head × number-of-arrows) ) |`. The
"position-of-head" part is the head word's **absolute position in the sentence**
(in the code: `root_pos = repr_tree.node.location` in
[`stark/processing/complexity.py`](../../../stark/processing/complexity.py)).
That is the only ingredient that comes from *outside* the chunk, and it is what
makes the same phrase score differently in different spots.

This makes sense given where NDD comes from: it was invented for **whole
sentences** (Jiang & Liu 2015), where "position of head" = where the sentence's
main verb sits, and "number of arrows" ≈ sentence length. Neither idea transfers
cleanly to a phrase, which isn't a sentence and has no sentence-level root.

Ways it *could* be adapted (this is a research decision, not just a code tweak):

1. **Don't report NDD for chunks** — only for whole sentences.
2. **Use the head's position *within the chunk*** (so it becomes position-proof
   like MDD), instead of its absolute sentence position.
3. **Define a separate "chunk NDD"** with its own clearly written formula, and
   leave the whole-sentence NDD as it is.

MDD, max depth and node count need no change.

## The files in this folder

- `position_invariance_test.py` — the slide test (Check 1).
  Run: `python3 nh-work/complexity-comparison/subtrees/position_invariance_test.py`
- `stark_subtrees_np_sl_ssj_dev.ini` — the config for the real noun-phrase run
  (Check 2). It's a copy of the whole-sentence config with the `head` (and
  `size`) lines changed.
- `outputs/stark_subtrees_np_sl_ssj_dev.tsv` — that run's result table (762
  phrase shapes with their measures).

## Independent check

A second model re-derived this from scratch (read-only; STARK untouched,
confirmed via `git status`). It reproduced the MDD/depth/nodes vs. NDD math, the
slide-test numbers, and the edge case, and confirmed the verdict. Two
refinements were folded in above:

- Tree extraction is governed by several config settings (`head`, `size`,
  `complete`, queries), not `head` alone — `head` is just the knob we used. The
  complexity function itself is agnostic to extraction settings.
- NDD is position-*dependent* (hence unsafe on subtrees), but not strictly
  different for every position pair: the `|log(…)|` can coincide for particular
  positions. The conclusion is unchanged.
