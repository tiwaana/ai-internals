# Part 6 — Tokens & Embeddings

*[← Part 5](ai-internals-05-terrible-in-2002.md) · [Series index](ai-internals-00-index.md) · Next: [Layers & Depth →](ai-internals-07-layers-and-depth.md)*

Ask a model how many times the letter r appears in "strawberry."

For a long stretch, and still on smaller models today, you would get "two." Confidently. A machine that can write you a working sorting algorithm cannot count the letters in a fruit.

People took this as proof the whole thing was hollow. It is not. It is a completely mechanical consequence of something that happens before the model sees a single weight, and once you know what it is, that failure stops being spooky and becomes obvious.

**The model never saw the letters.**

## Text gets chopped up first

A model does not read characters and it does not really read words. It reads **tokens**, which are word-pieces, and the chopping happens before anything else.

Common words are usually a single token. Rarer words get split. Depending on the tokenizer, "strawberry" comes apart into something like `straw` + `berry`, or `st` + `raw` + `berry`. Either way, by the time the model gets it, there is no sequence of letters left to count. There are two or three chunks, and the letter r is a property of a spelling the model never received.

Here is our sentence, chopped.

<svg viewBox="0 0 720 130" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A sentence split into tokens">
  <style>
    .tok{fill:var(--panel2,#1c2230);stroke:var(--line,#2b3444);}
    .tk{fill:var(--ink,#e6edf3);font:600 13px ui-monospace,monospace;}
    .id{fill:var(--faint,#6b7688);font:10px ui-monospace,monospace;}
    .cap{fill:var(--dim,#9aa7b8);font:12px ui-monospace,monospace;}
  </style>
  <text class="cap" x="20" y="22">"The trophy didn't fit"</text>
  <g>
    <rect class="tok" x="20"  y="40" width="52"  height="34" rx="5"/><text class="tk" x="46"  y="62" text-anchor="middle">The</text><text class="id" x="46"  y="90" text-anchor="middle">976</text>
    <rect class="tok" x="80"  y="40" width="62"  height="34" rx="5"/><text class="tk" x="111" y="62" text-anchor="middle"> trophy</text><text class="id" x="111" y="90" text-anchor="middle">31314</text>
    <rect class="tok" x="150" y="40" width="52"  height="34" rx="5"/><text class="tk" x="176" y="62" text-anchor="middle"> didn</text><text class="id" x="176" y="90" text-anchor="middle">3287</text>
    <rect class="tok" x="210" y="40" width="30"  height="34" rx="5"/><text class="tk" x="225" y="62" text-anchor="middle">'t</text><text class="id" x="225" y="90" text-anchor="middle">956</text>
    <rect class="tok" x="248" y="40" width="44"  height="34" rx="5"/><text class="tk" x="270" y="62" text-anchor="middle"> fit</text><text class="id" x="270" y="90" text-anchor="middle">5052</text>
  </g>
  <text class="cap" x="320" y="62">← five tokens, five integer IDs</text>
  <text class="id"  x="320" y="90">note the leading spaces are part of the token</text>
</svg>

Notice the space is inside the token. `" trophy"` with a leading space and `"trophy"` without are **different tokens with different IDs.** That is not a detail, it is the source of a whole family of real bugs where a trailing space in a prompt template quietly changes the model's behaviour.

## Where the chopping rules come from

Nobody sat down and wrote a list of word-pieces. The vocabulary is learned from data, by an algorithm usually called **BPE**, byte pair encoding, and it is refreshingly simple.

Start with every individual character as a token. Then look through a huge pile of text and find the pair of tokens that occurs together most often. Merge it into a single new token. Repeat, tens of thousands of times, until you have as many tokens as you wanted.

That is the whole algorithm. Frequent things become single units, rare things stay broken up. The result is a fixed **vocabulary**, typically 30,000 to 150,000 tokens, and the model can only ever see the world through it.

Back to the kitchen. This is the prep work, the dicing that happens before any cooking. And the crucial bit is that **you decide how to dice once, in advance, based on what you usually cook.** If your kitchen mostly does English, the knife is set up for English.

## Why an engineer cares, in four ways

This is the part that gets talked about in real conversations, so it is worth having ready.

**Spelling and counting are hard for structural reasons.** Strawberry, reversing a string, counting characters, rhyming. The model is reasoning about objects whose insides it cannot see. It can often work around this, but it is fighting its own input format to do it.

**Arithmetic is worse than you would expect.** The number 1234 might come in as `12` + `34`, or `1` + `234`, depending on the tokenizer and what came before it. The digits are not reliably individual things, so column arithmetic has no stable columns to work with.

**Some languages cost several times more than others.** Vocabularies are built from training data that skews heavily English. English text tends to run near one token per short word. Hindi, Thai, or Tamil written in their own scripts can take several tokens per word, sometimes one per character. Since you are billed per token and context windows are counted in tokens, **the same sentence can cost three or four times as much in one language as another.** That is a real, ongoing fairness problem and it is a good thing to raise if you ever want to see whether someone has actually thought about this.

**Whitespace and formatting matter more than they look.** A trailing space, a newline, whether the prompt template ends mid-token. All of it changes the IDs and therefore the prediction.

> 🦜 **Play:** go back to [**Feed the Parrot**](playground.html#parrot). It treats whole words as its atoms, which is the simple version of this. Real models chop finer, which is exactly why they can handle a word they have never seen before and the parrot cannot.

## From integers to geometry

So the text is now a list of integers. `976, 31314, 3287, …`

An integer is useless to the math. There is nothing to multiply. Token 5052 is not "half of" token 10104, the ID is just a name.

So the first thing the model does is look each ID up in a big table and pull out a **vector**, a list of numbers. Say 512 of them, or 4096 in a large model. That length is called the **hidden dimension**, written `d`.

This table is the **embedding matrix**, and it is the point where **text becomes geometry.** Every token is now a position in a space with hundreds or thousands of directions.

And because it is a space, closeness means something. During training, tokens used in similar ways drift into similar neighbourhoods.

<svg viewBox="0 0 720 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Words positioned in an embedding space">
  <style>
    .ax2{stroke:var(--line,#2b3444);stroke-width:1.5;}
    .pt{fill:var(--accent,#4c8dff);}
    .pt2{fill:var(--accent2,#37d39b);}
    .wl{fill:var(--ink,#e6edf3);font:600 12px ui-monospace,monospace;}
    .nt{fill:var(--faint,#6b7688);font:11px ui-monospace,monospace;}
    .arw{stroke:#f07aa6;stroke-width:2;fill:none;stroke-dasharray:4 3;}
  </style>
  <line class="ax2" x1="40" y1="180" x2="680" y2="180"/>
  <line class="ax2" x1="40" y1="180" x2="40" y2="20"/>
  <g>
    <circle class="pt" cx="150" cy="60" r="6"/><text class="wl" x="162" y="64">king</text>
    <circle class="pt" cx="150" cy="130" r="6"/><text class="wl" x="162" y="134">man</text>
    <circle class="pt" cx="300" cy="60" r="6"/><text class="wl" x="312" y="64">queen</text>
    <circle class="pt" cx="300" cy="130" r="6"/><text class="wl" x="312" y="134">woman</text>
  </g>
  <line class="arw" x1="150" y1="130" x2="150" y2="60"/>
  <line class="arw" x1="300" y1="130" x2="300" y2="60"/>
  <text class="nt" x="95" y="98">royalty</text>
  <text class="nt" x="245" y="98">royalty</text>
  <g>
    <circle class="pt2" cx="520" cy="50" r="6"/><text class="wl" x="532" y="54">cat</text>
    <circle class="pt2" cx="552" cy="72" r="6"/><text class="wl" x="564" y="76">dog</text>
    <circle class="pt2" cx="536" cy="96" r="6"/><text class="wl" x="548" y="100">horse</text>
    <circle class="pt2" cx="600" cy="155" r="6"/><text class="wl" x="612" y="159">bicycle</text>
  </g>
  <text class="nt" x="470" y="130">animals cluster</text>
</svg>

The famous demonstration is that directions carry meaning, and it is worth knowing whose demonstration it was. It comes from **word2vec** in 2013, Mikolov and colleagues at Google, five years before any of the machinery in this part existed. Take the vector for "king," subtract "man," add "woman," and you land near "queen." The step from man to woman and the step from king to queen turn out to be roughly **the same move in the same direction**, which means the space has learned something like a gender axis without anyone defining one.

Nobody built that. It fell out of trying to predict text well, which is the Part 1b argument showing up again in a place you can actually see it.

One honest footnote, since the result is almost always quoted without it. When you go looking for the word nearest to where you landed, the standard implementation excludes the three words you started from, and "king" itself sits very close to that spot. So the exclusion is doing real work in making the answer come out as "queen." The structure in the space is genuinely there, but the demonstration is a little more stage-managed than it sounds.

Measuring closeness is usually done with **cosine similarity**, which asks whether two vectors point in the same direction and ignores how long they are. It is a dot product with the lengths divided out, and a dot product, from the refresher, is a weighted sum.

This is also, exactly, what a **vector database** stores. When somebody says their product does semantic search, or RAG, this is the machinery: embed everything, then find the nearest neighbours to your question in that space. We do that properly in Act III.

## The catch that sets up everything after this

There is a problem with what I just described, and it is the reason the rest of Act I exists.

The embedding table is a **lookup**. One token, one vector, always the same.

Which means "bank" gets an identical vector in *river bank* and *savings bank*. And in our sentence, `" it"` gets exactly the same vector whether it refers to the trophy or the case. The embedding knows what the word tends to mean in general. It knows nothing about the sentence it is currently sitting in.

This is precisely the ceiling the field lived under for four years. Word2vec handed everybody vectors that carried meaning, and everybody then ran into the fact that one fixed vector per word is as far as you can go, because a good half of what a word means is decided by the words sitting next to it. From 2013 until 2017 that was simply the cost of doing business.

So at this point in the pipeline, the trophy sentence is a row of context-free vectors and the ambiguity is completely unresolved. Everything from here on is about fixing that: pushing those vectors through layers that let them look at each other and update themselves.

That is Part 7 onwards.

> **Say this out loud:** "It cannot count the r's in strawberry because it never saw the letters. It saw two tokens. And that same tokenizer is why the API costs three times more per sentence in Hindi than in English."

> **The question that takes you further:** *if meaning is a position in space, what happens to a word that genuinely has two unrelated meanings?*

### Checkpoint

1. Why is counting letters structurally hard for a language model, when writing code is not?
2. `"trophy"` and `" trophy"` have different token IDs. Give one concrete way that could cause a bug.
3. In one sentence, how does BPE decide what becomes a single token?
4. What does the embedding table give you that a token ID does not, and what can it still not tell you about the word "it"?

*Next: [Part 7 — Layers & Depth →](ai-internals-07-layers-and-depth.md), where we stack the machinery and find out why one ingredient makes depth mean anything at all.*
