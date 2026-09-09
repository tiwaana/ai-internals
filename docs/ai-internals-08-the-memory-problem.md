# Part 8 — The Memory Problem

*[← Part 7](ai-internals-07-layers-and-depth.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md) · Next: [Attention →](ai-internals-09-attention.md)*

Here is a task. Read a thousand word article, then write down the next word.

To do it properly you need things from paragraph two. A name, a claim, who was arguing what. Now do it under a constraint: **you may not look back at the article.** Everything you are allowed to carry forward has to fit on one index card, written as you read, one pass, no going back.

That is not a metaphor for how machines handled language before 2017. That is precisely the architecture.

This part is about that index card, why it was the bottleneck on everything, and why it is the reason the next part is a big deal. Attention is going to look like an obvious idea when you get there, and it will only feel like a breakthrough if you have felt the thing it replaced.

## Reading one word at a time

A **recurrent neural network** processes a sequence in order. One token at a time.

It keeps a single vector called the **hidden state**, and that is the index card. At each step it takes the next word, combines it with the current card, and produces an updated card. Then it moves on. The old card is gone.

```
    "The"      "trophy"     "didn't"      "fit"
      │           │            │            │
      ▼           ▼            ▼            ▼
card ────► card ────► card ────► card ────► card ──►  predict
     one fixed-size vector, rewritten at every step
```

This was the sensible design and for a long time it was the only one. It handles any length of input with a fixed number of weights, and it processes language the way we do, left to right.

It has two problems, and they are both fatal.

## Problem one: the card is finite and gets overwritten

Every step rewrites the card. Information from word 10 survives to word 900 only if it managed to stay in that vector through 890 successive rewrites, each of which was mostly about some other word.

It does not survive. In practice it fades within a few dozen steps.

And the mechanics of the fading are the vanishing gradient from Part 5, wearing a different hat. To learn that word 900 depends on word 10, backprop has to push a gradient back through 890 multiplications. Those slopes multiply, and the product goes to approximately zero. **The network cannot learn the long-range dependency because no learning signal survives the trip.**

Our sentence is short enough to survive it, barely. But the structure is exactly this: `it` needs `trophy`, and everything between them is pressure on a card with limited room.

## LSTMs, which helped, and did not solve it

In 1997, Hochreiter and Schmidhuber introduced the **LSTM**, or long short-term memory. It was a real piece of engineering and it ran production translation and speech recognition for the better part of two decades.

The idea is to stop overwriting the whole card every step. An LSTM adds a separate memory line running alongside, plus three small learned **gates** that control it.

- A **forget gate** decides what to drop from memory.
- An **input gate** decides what from the current word is worth writing down.
- An **output gate** decides how much of memory to expose right now.

The important structural change is that the memory line is mostly *added to* rather than multiplied through. Addition does not shrink gradients the way repeated multiplication does, so the signal survives much further back. Instead of a few dozen steps you get hundreds.

That is a genuine improvement, and it is not a fix. Hundreds is not thousands. And every piece of context still has to squeeze through one fixed-size vector, so the fundamental compression is untouched. You gave the reader a bigger index card and better handwriting. They are still not allowed to look back at the article.

## Problem two, which is the one that actually mattered

The first problem is about quality. The second is about money, and in hindsight it was decisive.

**Recurrence cannot be parallelised.** To compute step 17 you need the card from step 16, which needs 15, all the way down. The dependency chain is the length of your text and there is no way around it.

Meanwhile GPUs, from Part 5, are machines that do thousands of things simultaneously and are close to useless at doing one thing after another quickly.

So the entire hardware story that had just transformed the field could not be applied here. Training on a long sequence meant a long serial walk, every time, on hardware built for the opposite. You could not make these models much bigger, because making them bigger made them proportionally slower and there was no parallelism to buy your way out with.

**That is the ceiling.** Not that LSTMs were bad at language. That they could not be scaled, and by 2016 everyone had watched what scale did to image recognition.

## So what would you actually want

Sit with the problem before reading the answer, because the answer is genuinely guessable from here.

You want two things. You want each word to reach back and read any earlier word directly, with no relay through 890 rewrites. And you want all of those lookups to happen at the same time, so a GPU can do them in one shot.

Those sound like opposite requirements. Direct access to everything, computed all at once.

Then throw out the assumption that has been sitting underneath all of this. **Why is the model reading in order at all?** Order was inherited from how humans read. It was never a requirement of the maths.

If you drop it, every word can look at every other word simultaneously, in one big parallel operation, and you never need an index card because nothing was ever compressed away in the first place.

That is the next part, and it is why it was worth 2017.

> **Say this out loud:** "Before transformers, a model compressed everything it had read into one fixed-size hidden state, and it had to be computed strictly in order, so it could not use a GPU properly. Attention fixed both at once."

> **The question that takes you further:** *if you let every token see every other token directly, what does that cost, and what breaks when the text gets long?*

### Checkpoint

1. What is the hidden state, and why does information from early in a long text disappear from it?
2. LSTMs improved on plain RNNs. What did the gates change, and what did they leave unsolved?
3. Recurrence could not be parallelised. Explain why that turned out to matter more than the memory problem.
4. Before you read on: knowing GPUs are good at doing many things at once, what would you change about the design?

*Next: [Part 9 — Attention →](ai-internals-09-attention.md), where somebody throws out the index card.*
