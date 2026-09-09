# Part 17 — Size & Quantization

*[← Part 16](ai-internals-16-open-vs-closed-weights.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md)*

There is a graphics card under my desk with 5 gigabytes of memory on it. A Quadro P2200. It is not a bad card, it is just not a 2026 card, and 5 GB is the number that decides what I am allowed to do.

This is the part where that stops being my problem and becomes the interesting one. Because the question "will this model run on my machine" has an exact answer, you can work it out on the back of an envelope, and once you can do that you will never again read a model announcement the same way.

Everything here follows from one idea. **A weight is a number, and you get to choose how carefully to write it down.**

## What does 7B actually mean

B is billion. A 7B model has roughly 7 billion weights, which are the knobs from Part 2.

That number is the model's raw capacity. Roughly, how much it can know and how subtly it can reason. It is the number everyone quotes.

But think about what you are actually being told. Seven billion is *how many* knobs there are. It says nothing about how precisely each knob's position was written down, and those are two different facts about the same model. You can note somebody's weight as 72.4 kilos or as 72, and it is the same person either way, on less paper.

So here is the question a beginner never asks and an engineer always does. **Stored in how many bits?**

That is the hidden second dimension. A model is never just "7B." It is 7B *at some precision*, and all of the memory math lives in the second half of that sentence.

## Floating point, briefly, from nothing

Every weight is a decimal like `0.0273`. Computers store decimals in a format called floating point, and you choose how many bits to spend on each one.

Think of it as how many digits you are allowed to write down. More bits, more digits, more exact. Fewer bits, coarser, but each number takes less room.

| Format | Bits per weight | Bytes | What it is |
|--------|-------------|-------|------------|
| FP32 | 32 | 4 | Full precision. The training default, very exact |
| FP16 / BF16 | 16 | 2 | Half precision. The standard for serving models |
| INT8 | 8 | 1 | Quantized. Each weight squeezed to a whole number |
| INT4 (Q4) | 4 | 0.5 | Aggressively quantized. The workhorse for running things at home |

Eight bits make a byte, so a 4-bit weight costs half a byte. That is all you need to know about the format to do the arithmetic.

## The formula, which is your daily tool

```
Memory (GB) ≈ (params in billions) × (bytes per weight)
```

That is it. Learn it and you can do this in your head for the rest of your life.

A 7B model:

- FP16, 2 bytes per weight: `7 × 2` = **14 GB**
- INT8, 1 byte: `7 × 1` = **7 GB**
- INT4, half a byte: `7 × 0.5` = **3.5 GB**

Look at those numbers against my 5 GB card. At full 16-bit precision, a 7B model needs nearly three times the memory I have. At 4 bits it fits, with room left over.

So quantization is not trivia. It is the entire reason a useful model runs on a modest machine at all.

## What quantization actually does

Take one weight, `0.4823917`. At 16 bits you store all of that detail.

Quantization asks whether you really need every decimal.

1. Take a block of weights, say 32 of them.
2. Find their range, lowest to highest.
3. Chop that range into a small number of **buckets**. Four bits can count to sixteen, so at 4 bits you get 16 buckets. Eight bits gets you 256.
4. Round each weight to its nearest bucket, and store the bucket number plus one shared scale factor for the whole block.

<svg viewBox="0 0 720 170" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Quantization to 16 buckets">
  <style>
    .axis{stroke:var(--line,#2b3444);stroke-width:2;}
    .tick{stroke:var(--faint,#6b7688);stroke-width:1;}
    .t{fill:var(--dim,#9aa7b8);font:11px ui-monospace,monospace;}
    .val{fill:var(--ink,#e6edf3);font:600 12px ui-monospace,monospace;}
    .orig{fill:#f07aa6;}
    .snap{fill:#37d39b;}
  </style>
  <line class="axis" x1="60" y1="90" x2="660" y2="90"/>
  <g>
    <line class="tick" x1="60"  y1="82" x2="60"  y2="98"/>
    <line class="tick" x1="100" y1="82" x2="100" y2="98"/>
    <line class="tick" x1="140" y1="82" x2="140" y2="98"/>
    <line class="tick" x1="180" y1="82" x2="180" y2="98"/>
    <line class="tick" x1="220" y1="82" x2="220" y2="98"/>
    <line class="tick" x1="260" y1="82" x2="260" y2="98"/>
    <line class="tick" x1="300" y1="82" x2="300" y2="98"/>
    <line class="tick" x1="340" y1="82" x2="340" y2="98"/>
    <line class="tick" x1="380" y1="82" x2="380" y2="98"/>
    <line class="tick" x1="420" y1="82" x2="420" y2="98"/>
    <line class="tick" x1="460" y1="82" x2="460" y2="98"/>
    <line class="tick" x1="500" y1="82" x2="500" y2="98"/>
    <line class="tick" x1="540" y1="82" x2="540" y2="98"/>
    <line class="tick" x1="580" y1="82" x2="580" y2="98"/>
    <line class="tick" x1="620" y1="82" x2="620" y2="98"/>
    <line class="tick" x1="660" y1="82" x2="660" y2="98"/>
  </g>
  <text class="t" x="60"  y="118">bucket 0</text>
  <text class="t" x="610" y="118">bucket 15</text>
  <circle class="orig" cx="431" cy="90" r="6"/>
  <text class="val orig" x="431" y="60" text-anchor="middle">0.4823917</text>
  <text class="t orig" x="431" y="45" text-anchor="middle" fill="#f07aa6">exact (16 bits)</text>
  <circle class="snap" cx="420" cy="90" r="6"/>
  <text class="val snap" x="420" y="150" text-anchor="middle">≈ 0.48  →  "bucket 11" (4 bits)</text>
</svg>

So instead of `0.4823917` in 16 bits, you store "bucket 11" in 4 bits, and rebuild an approximation of `0.48` when you need it.

Be honest about what just happened. **Every single weight is now slightly wrong.** You threw precision away and the model got a bit dumber.

## So why does that not wreck it

This is the part I did not expect, and it goes back to something I knew from twenty years ago without appreciating how far it would stretch.

Neural networks are enormously redundant and they are robust to noise. No single weight is critical. The signal is smeared across billions of them, so nudging each one by a rounding error does not break anything important.

You already know what this looks like, because you have seen a JPEG. Save a photo at moderate quality and it throws away fine detail you were not really using. Zoom right in and you can see the damage. Look at the picture and it is obviously the same picture.

Going from 16 bits to 4 typically costs a few percent of quality and buys you **four times less memory**, plus faster inference because you are moving less data around. That is an outrageous bargain, and it is why almost everyone running models locally runs them quantized.

> 🗜️ **Play:** [**Squeeze**](playground.html#squeeze) in the playground trains the little network from Part 2 until it genuinely solves the problem, then saves it badly. Drag the slider down and watch the picture of what it learned survive four bits, survive three, and fall apart at two, with the four test points going red as it goes. Nothing there is a recording. It quantizes the weights for real and runs the squeezed network to draw the second picture.

**Where it breaks.** Push to 2 bits, sometimes 3, and quality falls off a cliff. Too few buckets, the approximation gets crude, and the model starts babbling. **Q4 is the widely agreed sweet spot.** You will see names like `Q4_K_M` in the GGUF files that llama.cpp and Ollama use. K means a smarter blocking method, M means medium size. It is what most people reach for and it is usually right.

## What else? The KV cache

Weights are not the only thing sitting in memory.

As the model reads your prompt it keeps notes in the margin about every token it has already seen, so it does not have to work them out again for the next word. Those notes are the **KV cache**, the thing Part 9 said was sitting in GPU memory next to the weights. More text means more margin, so it grows with your context length.

```
VRAM used ≈ quantized weights + KV cache (grows with context) + overhead
```

On my 5 GB card, a 3.5 GB Q4 7B model leaves about a gigabyte for context. So I run short contexts, or push some layers onto the CPU and accept that it gets slower. That layer split is a knob you learn to tune. Ollama and llama.cpp set it automatically and let you override.

Why the cache grows the way it does is the seating chart from Part 9: every word scored against every other word, so twice the words is four times the squares.

## Putting it together

| Model | Params | Q4 size | Fits a 5 GB GPU? |
|-------|--------|---------|------------------|
| Qwen2.5 3B | 3B | ~2 GB | Yes, comfortably, with context room |
| Qwen2.5 7B | 7B | ~4.5 GB | Yes, tight. Short context or slight offload |
| Gemma 2 9B | 9B | ~5.5 GB | Partly. Some layers spill to CPU and it slows down |
| Llama 3 70B | 70B | ~40 GB | Nowhere close |

You can now predict what fits before you download anything. That reflex, doing the arithmetic before the download, is most of what separates somebody who runs models from somebody who reads about them.

> **Say this out loud:** "It is not 7B, it is 7B at some precision. Four bit quantization costs a few percent of quality and four times less memory, which is why it fits on my card at all."

> **The question that takes you further:** *quantization costs a few percent on benchmarks. A few percent of what, and would you notice which few percent?*

### Checkpoint

1. A model is advertised as 13B. Using the formula, how much memory at INT4? At FP16?
2. In one sentence, why does chopping every weight down to 4 bits not destroy the model?
3. Besides the weights, what else eats your VRAM, and what makes it grow?
4. Someone tells you they are running a 70B model on a gaming laptop. What is the question you ask them?

*[← Back to the series index](ai-internals-00-index.md)*
