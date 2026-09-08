# Part 7 — Layers & Depth

*[← Part 6](ai-internals-06-tokens-and-embeddings.md) · [Series index](ai-internals-00-index.md) · Next: [The Memory Problem →](ai-internals-08-the-memory-problem.md)*

Let me offer you a bet.

You build a neural network a hundred layers deep. Enormous. Hundreds of millions of weights, stacked up, each one feeding the next. You train it for a month.

I will build one layer.

If you leave one specific ingredient out of yours, I can prove that my single layer computes **exactly** what your hundred layers compute. Not approximately. Identically. Your month was wasted and your ninety-nine extra layers did nothing at all.

That ingredient is the most important idea in deep learning, most people who use these models have never heard of it, and it is a three-line proof. That is this part.

## Where we are in the pipeline

From Parts 1b and 6, the loop looks like this, every single time the model produces a word.

```
text → [tokenize] → token IDs → [embed] → vectors → [STACK OF LAYERS] → vector
     → [unembed] → a score for every word → [sample] → next token → repeat
```

Tokenize and embed we did in Part 6. Unembed is the reverse of embed: the final vector gets scored against the whole vocabulary, softmax turns those scores into percentages, and you sample one. Then the entire loop runs again with the new word on the end, which is why generation happens one token at a time and why it feels like typing.

Everything interesting is in the middle. So what is a layer?

## A layer is a function, and its size is its weight count

A layer is a function. A list of numbers goes in, a list of numbers the same length comes out. Inside, it is Part 2 done many times over: every output number is a weighted sum of all the input numbers, each with its own knob.

So if 512 numbers go in and 512 come out, every one of those 512 outputs needs a knob for each of the 512 inputs.

**512 × 512 = 262,144 knobs in one layer.**

That is the whole answer to "how many weights per layer," and it is why the parameter counts on model cards get large so quickly. Nothing subtler is going on.

## The trap

You have parameters to spend. Two ways to spend them.

**One wide layer.** Your numbers go in, one set of knobs works on them, numbers come out.

**Three stacked layers.** Your numbers go in, the first set of knobs works on them, whatever comes out is handed to a second set, and that gets handed to a third.

Stacking just means the output of one becomes the input of the next. That is the whole idea, there is nothing hidden in it.

Three layers, three times the knobs, obviously more powerful. That is what I would have said, and it is wrong.

<svg viewBox="0 0 720 130" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Linear layers collapse">
  <style>
    .b{fill:var(--panel2,#1c2230);stroke:var(--line,#2b3444);}
    .m{fill:var(--ink,#e6edf3);font:600 14px ui-monospace,monospace;}
    .op{fill:var(--faint,#6b7688);font:600 18px ui-monospace,monospace;}
    .r{fill:#f07aa6;font:600 13px ui-monospace,monospace;}
  </style>
  <rect class="b" x="40"  y="30" width="60" height="40" rx="8"/><text class="m" x="70"  y="55" text-anchor="middle">layer 3</text>
  <rect class="b" x="120" y="30" width="60" height="40" rx="8"/><text class="m" x="150" y="55" text-anchor="middle">layer 2</text>
  <rect class="b" x="200" y="30" width="60" height="40" rx="8"/><text class="m" x="230" y="55" text-anchor="middle">layer 1</text>
  <text class="op" x="285" y="56">→</text>
  <rect x="320" y="30" width="150" height="40" rx="8" fill="#37d39b" opacity="0.18" stroke="#37d39b"/>
  <text class="m" x="395" y="55" text-anchor="middle">one layer</text>
  <text class="r" x="255" y="105" text-anchor="middle">three sets of knobs fold into ONE</text>
</svg>

Here is why. If every layer does nothing but weighted sums, then a weighted sum of weighted sums is still, when you flatten it out, just a weighted sum. The three sets of knobs can be folded together into a single set that produces exactly the same answer, and you can work out that single set once in advance and throw the other two away.

Back to the kitchen for a second, because it makes this concrete. Say every station in your kitchen is allowed to do one thing, scale a quantity up or down. Station one doubles everything, station two halves it, station three triples it. Three stations, three staff, three sets of instructions. And you could have written *multiply by 1.5* on a card and handed it to one person at the door. The kitchen was not doing three things. It was doing one thing in an expensive way.

Nothing was lost in the folding. There was nothing there to lose.

**Three stacked linear layers collapse into a single linear layer.** The depth bought you nothing. It is not close to one layer, it is exactly one layer, and that is a theorem, not an observation. That is the bet, and it is why every real network has something sitting between each pair of layers.

## The bend

Between layers, you apply a simple **nonlinear** function. Historically ReLU, which is just `max(0, x)`, meaning negatives become zero and everything else passes through. Modern LLMs use smoother relatives called SiLU or GELU.

Now the layers cannot be folded together, because you would have to fold the bend in too and a bend does not fold. Each layer's output has been kinked before the next one sees it, so the next layer is genuinely working on something new rather than a rearrangement of the old.

Depth suddenly means something.

> **The single most important internal fact in deep learning.** Linear layers give you reach. **Nonlinearities are what make depth mean anything.** Leave them out and a hundred layer network computes what one layer computes.

## An aside for anyone who did this twenty years ago

The bend was not always ReLU. For a long time it was the **sigmoid**, the S-curve that squashes anything into the range 0 to 1.

If you ever studied fuzzy logic, you have seen that curve before, because it is a **membership function**. Same shape, same textbook. Fuzzy logic argued for graded truth on philosophical grounds: "warm" is not true or false, it is 0.7 warm, and a system that pretends otherwise is lying about the world.

Neural networks ended up needing the same curve for an entirely different reason, and honestly a better one.

The original perceptron used a hard step. Below the threshold, output 0. Above it, output 1. A cliff.

And now recall what Part 3 said training actually is. You ask each knob one question: which way, and how steeply. On a cliff there is no answer. Standing on the flat top you are told the ground is level, so nudging the knob changes nothing and there is no reason to move. Standing at the edge you fall off. Either way nothing tells you which direction is better, so there is no learning signal, so the thing cannot be trained.

Replace the cliff with the S-curve and you have a hillside instead. Every point on a hillside slopes somewhere, so every knob can be told which way to move and by how much. **Graded truth was not only a nicer description of the world, it was the thing that made learning mechanically possible.**

ReLU and its modern cousins look less like membership functions, but they are doing the same two jobs: bend the line, and keep a slope you can follow.

## So what does depth actually buy

| | One wide layer | Three stacked layers with bends |
|---|---|---|
| What it can express | one straight relationship | curved, layered relationships |
| In the kitchen | one cut through the ingredient | fold, cut, fold, cut. Any shape you like |

The reason depth beats width is that it lets the model build concepts on top of concepts.

Early layers pick up simple things. This token is a noun. This word is negated. Middle layers combine those into richer ones. This is a subject-verb clause. The sentiment just flipped. Late layers assemble genuinely abstract ones. This sentence is heading toward a particular answer.

A single layer cannot do that no matter how wide you make it, because one layer is one transform and one bend. Depth is repeated refinement, and refinement is where meaning gets built.

That is why models are advertised by depth. Llama 3 8B is 32 layers. The 70B is 80. Same idea, more refinement steps, wider vectors at each one.

## What else? What a real layer actually contains

A real transformer layer has two halves, and both are present in every one of those 32 or 80.

1. **Attention.** The part that lets tokens look at each other. Part 9, and it is the whole ballgame.
2. **An MLP**, or feed-forward block. Exactly the stacked-linear-with-a-bend we just built, applied at each position separately.

That is where the billions of weights live. Attention matrices plus MLP matrices, multiplied by the number of layers.

And notice what still has not happened. Our sentence is a row of vectors moving up through the stack, each one being refined, but so far **no vector has looked at any other vector.** The word "it" is still being processed in total isolation from "trophy." Everything so far has been each token improving itself, alone.

That is the missing piece. Part 8 is the machinery that came before the fix, and why it was not enough.

> **Say this out loud:** "Without a nonlinearity, stacked linear layers collapse into one matrix. The bend between layers is the only reason depth does anything."

> **The question that takes you further:** *if depth builds concepts on concepts, what decides how deep is deep enough?*

### Checkpoint

1. I stack five linear layers with no activations between them. How powerful is that compared to one linear layer, and why?
2. A layer takes 1024 numbers in and puts 1024 numbers out. Roughly how many knobs does it hold?
3. In one line: what does depth buy that width alone cannot?
4. Why could you not train a network built out of hard step functions, even though a step is perfectly nonlinear?

*Next: [Part 8 — The Memory Problem →](ai-internals-08-the-memory-problem.md), where we look at how machines handled language before 2017, and why it capped out.*
