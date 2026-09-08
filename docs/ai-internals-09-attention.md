# Part 9 — Attention

*[← Part 8](ai-internals-08-the-memory-problem.md) · [Series index](ai-internals-00-index.md) · Next: [Build a Transformer →](ai-internals-10-tiny-transformer.md)*

In 2017, eight researchers at Google published a paper about machine translation. They called it *Attention Is All You Need*, which is a nod to a Beatles song, and they put a footnote on the author list saying the order was random because everyone contributed equally.

You already know what they were up against, because that was Part 8. The index card. Everything compressed into one hidden state, computed strictly in order, unable to use a GPU properly.

And their idea was the one you were invited to guess at the end of that part. **Throw the sequence out.** Let every word look at every other word directly, all at once, in a single operation a GPU can do in parallel.

Nobody in that paper predicted anything like what came next. They were trying to translate German faster. What they had actually done was remove the bottleneck that was keeping these models small, and once it was gone, people found out what happens when you make them enormous.

This is the part that makes a transformer a transformer, and it is where our sentence finally gets solved.

## The problem, stated exactly

From Part 6, every token gets a vector by lookup, and the lookup is context-free. `" it"` gets the identical vector whether it points at the trophy or the case. From Part 7, the layers refine each vector, but no vector has yet been allowed to look at any other one.

Meaning does not work that way. *River bank* and *savings bank* are the same token with opposite senses. And our sentence hangs entirely on a word that has no content of its own:

> **The trophy didn't fit in the case because it was too big.**

So the need is precise. **Let each token gather relevant information from the other tokens and update itself.** That gathering is attention.

## Query, Key, Value

Picture a room full of people, and you need something.

You say out loud what you are looking for. That is your **Query**. Everyone in the room is wearing a badge describing what they are. Those are the **Keys**. You look around, work out whose badge best matches what you asked for, and then that person tells you what they actually know. That is the **Value**.

The important part of the analogy is that the badge and the knowledge are different things. What makes you *findable* is not the same as what you have to *give*. That is exactly why a key and a value are separate.

Now in the model. Every token produces all three, each from its own weight matrix:

- A **Query.** *Here is what I am looking for.* The token "it" says: I am a pronoun, I need the noun I refer to.
- A **Key.** *Here is what I am, if you are looking.* The token "trophy" says: I am a concrete object, a likely antecedent.
- A **Value.** *Here is the actual information I hand over if you pick me.*

<svg viewBox="0 0 720 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Query Key Value flow">
  <style>
    .tok{fill:var(--panel2,#1c2230);stroke:var(--line,#2b3444);}
    .tl{fill:var(--ink,#e6edf3);font:600 13px ui-monospace,monospace;}
    .q{stroke:#4c8dff;} .v{stroke:#37d39b;}
    .qq{fill:#4c8dff;} .kk{fill:#f4b860;} .vv{fill:#37d39b;}
    .lbl{font:600 12px ui-monospace,monospace;}
    .note{fill:var(--dim,#9aa7b8);font:11px ui-monospace,monospace;}
  </style>
  <rect class="tok" x="40" y="90" width="70" height="34" rx="8"/><text class="tl" x="75" y="112" text-anchor="middle">"it"</text>
  <text class="qq lbl" x="150" y="70">Query →</text>
  <path class="q" d="M115,100 C 200,60 260,60 330,80" fill="none" stroke-width="2" marker-end="url(#q)"/>
  <rect class="tok" x="360" y="60" width="90" height="34" rx="8"/><text class="tl" x="405" y="82" text-anchor="middle">"trophy"</text>
  <text class="kk lbl" x="470" y="60">Key: "I'm a noun"</text>
  <text class="vv lbl" x="470" y="90">Value: trophy-meaning</text>
  <text class="note" x="230" y="150">Q·K match is high → attention weight ≈ 0.7</text>
  <path class="v" d="M450,100 C 380,150 200,150 110,118" fill="none" stroke-width="2" marker-end="url(#v)"/>
  <text class="vv lbl" x="230" y="185">Value flows back into "it"</text>
  <defs>
    <marker id="q" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#4c8dff"/></marker>
    <marker id="v" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#37d39b"/></marker>
  </defs>
</svg>

The mechanism, in four steps:

1. Each token's Query is compared against **every** token's Key.
2. A good match gives a high score. "Trophy" is what "it" was looking for.
3. The scores are turned into weights that sum to 1. *Seventy percent of my attention on "trophy," ten percent on "case," and so on.*
4. Each token pulls in a weighted blend of everyone's Values and adds it to its own vector.

And there it is. **The vector for "it" absorbs a large dose of the vector for "trophy." It now knows what it refers to.** The sentence we started with in Part 1a has just been resolved, mechanically, by a dot product and a weighted average. That is the whole trick, and I still find it slightly outrageous that it works.

> 🔦 **Play:** [**Spotlight**](playground.html#spotlight) in the playground is one real attention head. You set the query with sliders, the arcs you see are the real match scores against real keys, and the output really is a blend of the values. Four puzzles. Go be the query.

## The formula, which you only have to read

Each token's vector gets run through three separate sets of knobs, one set for the query, one for the key, one for the value. Those knobs are learned like everything else, which is to say they started out random and training sanded them into shape.

The whole operation then fits on one line. You will see this line everywhere, on slides and in papers, so it is worth being able to read out loud. Reading it is all you ever have to do with it.

```
Attention(Q, K, V) = softmax( Q·Kᵀ / √d ) · V
```

Take it a piece at a time, with the room still in mind. Q is everybody's question, K is everybody's badge, V is what everybody knows.

| Piece | Say it as | In the room |
|-------|-------------|-----|
| `Q · Kᵀ` | check every question against every badge, which fills in a grid of match scores | you glance at all the badges at once and rate how well each one answers what you asked |
| `/ √d` | shrink all the scores by the same amount | housekeeping. Longer vectors make bigger numbers, and this keeps them in a sane range |
| `softmax(…)` | turn one row of scores into percentages that add to 100 | you decide how to split your attention across the room, and it has to add up to all of it |
| `… · V` | use those percentages to blend what everyone knows | you walk away with a mixture, mostly from the person who matched, a little from everyone else |

Two bits of notation, so they stop being scary. The raised `T` on `Kᵀ` says the badges are laid out sideways so they line up against the questions, which is bookkeeping and nothing more. And `d` is just the length of the vectors, the number from Part 6. Neither one is an idea. They are both furniture.
The output is a new, context-aware vector for each token, the same length as the one that came in. It flows into the MLP half of the layer from Part 7, and that completes one transformer layer.

## Where the memory goes

Look at that first step again. Every token compared against every token. Think of it as a seating chart with every word down the side and the same words across the top, and a score written in every square. Ten words is a hundred squares. Twenty words is four hundred.

So double the length of your text and you **quadruple** the grid.

This is the **KV cache**, the thing sitting in GPU memory alongside the weights, and it is the honest reason long context is expensive in both compute and VRAM. It is not a billing decision, it is a square. Act III turns this into actual gigabytes on my actual card.

## Multi-head

The model does not do this once. It runs the whole thing several times side by side, each run with its own three sets of knobs, so each run asks a different kind of question about the same sentence. Each run is a **head**.

One head might track grammar, subject to verb. Another tracks pronouns, "it" to "trophy". Another tracks topic. At the end their answers get stapled together into one vector and passed on.

Same mechanism, run as a team of specialists, so that a token can attend to several different kinds of relationship at the same time.

## What else? The whole thing, assembled

```
tokens → embeddings
   │
   ▼  (repeat for every layer, e.g. ×32)
┌──────────────────────────────┐
│  Attention                   │  ← Q/K/V, softmax(QKᵀ/√d)·V, multi-head
│  (tokens read each other)    │
│      +                       │
│  MLP (per-token refinement)  │  ← linear → bend → linear
└──────────────────────────────┘
   │
   ▼
final vectors → unembed → probabilities → sample → next token → (loop)
```

That is the complete skeleton of every large language model in existence. Claude, GPT, Llama, Qwen, all of them. They differ in size, in training data, and in tuning. They do not differ in this shape.

Which is a good moment to say something out loud: you now know the architecture. Not a summary of it, the actual thing. What is left in Act I is running it and training it.

> **Say this out loud:** "Attention is every token asking every other token how relevant it is, then taking a weighted average of what they know. And it is an n by n grid, which is why doubling your context quadruples the cost."

> **The question that takes you further:** *attention lets every token see every other token. So what is the model doing with all the layers it spends after that?*

### Checkpoint

1. In *"The chicken didn't cross the road because it was too tired,"* when the model processes "it", which token should its Query match best, and what flows back into "it"?
2. Why does doubling the number of tokens quadruple the attention grid, and what does that do to your VRAM?
3. In one line, what is the difference between a Key and a Value for the same token?
4. The 2017 paper was about translation. Why did removing recurrence turn out to matter so much more than the authors were claiming?

*Next: [Part 10 — Build a Transformer →](ai-internals-10-tiny-transformer.md). We stop drawing it and run one, in about 150 lines of Python.*
