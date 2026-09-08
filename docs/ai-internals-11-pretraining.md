# Part 11 — Pretraining: "It's Just Predicting the Next Word"

*[← Part 10](ai-internals-10-tiny-transformer.md) · [Series index](ai-internals-00-index.md)*

Somebody is going to say it to you. Possibly at a dinner party, possibly in a meeting where a budget is at stake.

**"It's just predicting the next word."**

They are right. That is the objection I raised in Part 1b and it is factually correct, and by the end of this part you will understand why it settles nothing, which is a considerably more useful position than either believing the hype or dismissing it.

We have built the whole machine. Part 4 trained a tiny one to say `hello world`. This part is what happens when you run that same four-step loop on everything.

## Same loop, different planet

Nothing about the four steps changes for a frontier model. Forward, loss, backward, update. Here is what does change.

| | Our toy | A real LLM |
|---|---|---|
| Data | 9 examples | trillions of tokens, much of the web |
| Parameters | ~2,000 | billions |
| Model in the middle | one hidden layer | dozens of transformer layers |
| Backprop | by hand, above | `loss.backward()`, automatic |
| Update rule | plain gradient descent | Adam, a smarter step |
| Hardware and time | instant, one CPU | thousands of GPUs, weeks |
| Goal | memorise 11 characters | **generalise** |

That last row is the only one that matters, and it is the entire argument.

## The thing that makes memorisation impossible

Our toy in Part 4 memorised. Nine examples, two thousand weights, plenty of room. It stored the answer and called it a day, and I said at the time that this was a lookup table taking the scenic route.

Now take that option away.

A frontier model is trained on something like ten trillion tokens. It has, generously, a trillion parameters, and each one is a single number. **There is nowhere near enough room to store what it read.** The compression ratio is brutal and it is not optional.

So the model faces a genuinely constrained problem. The loss must come down. Memorising is off the table. The only remaining move is to find the *rules that generate* the text and keep those instead, because rules are enormously smaller than the things they generate.

And when you ask what rules generate human writing, the answer is uncomfortable. Grammar, because ungrammatical continuations are bad guesses and cost you loss. Facts, because "the capital of France is" has a right answer. Arithmetic. Code syntax. That trophies are large and cases hold things. That a person who is angry in the first paragraph is usually still angry in the third. Which way a sarcastic sentence points.

**Nobody put any of that in.** There was no grammar module, no fact database, no reasoning component. Every bit of it got squeezed out under pressure, because knowing it made the next guess better.

This is the part I find genuinely hard to be casual about. We did not build a mind. We built a compressor, pointed it at everything people have written, and turned the pressure up until something that behaves quite a lot like understanding fell out the other side as a side effect.

## So how do you answer at the dinner party

Do not argue that it is not predicting the next word. You will lose, because it is.

Argue about what predicting the next word *well* requires. The move is to grant the premise and attack the conclusion.

> "Yes, that's exactly what it does. But you can't memorise your way there. Twenty-word sentences outnumber the atoms in the universe, so almost every sentence it sees is new. The only way to get good at that game is to learn the structure underneath it, and the structure underneath human writing is most of how the world works."

Then, if you want to be genuinely useful rather than merely right, add the other half:

> "Which also tells you exactly where it will fail. It learned what text usually looks like. Nobody ever optimised it for being correct."

That second sentence is the honest one, it is where Act III begins, and it is why a model will invent a citation with such confidence. It was never trained to be right. It was trained to be plausible, and those two things overlap most of the time, which is the most dangerous possible amount.

## What this cost

Some numbers, because the abstraction hides them.

Training a frontier model runs into the tens or hundreds of millions of dollars in compute. Thousands of GPUs, weeks of wall-clock time, in buildings drawing power measured in megawatts. This is why Part 16's question of who gets the weights file matters commercially, and why open-weight releases are a genuinely strange gift.

It is also why the field cares so much about **scaling laws**, which are empirical curves saying how much better the loss gets when you add parameters, data or compute. They are the reason anyone was willing to spend a hundred million dollars before seeing the result. You could extrapolate the curve and it kept being right.

## What you have now

That closes Act II, and it is worth saying plainly what you can now do.

You know what a neuron is, how it learns, why backprop makes learning possible, why it all failed for twenty years, how text becomes numbers, what layers buy you, what came before attention, what attention does, and what happens when you train the thing on everything.

You could sit down with the 2017 transformer paper and follow it. Not skim it. Follow it.

What you cannot do yet is explain why a raw model trained this way will happily help you with something appalling, why it has a personality, or why anyone trusts a benchmark. A model that has only been pretrained is not a chatbot, it is a very well-read text continuation engine with no manners and no idea it is in a conversation.

Turning that into something you can talk to is a separate process, it happens after pretraining, and it is Act III.

> **Say this out loud:** "It is next-token prediction, and it cannot memorise its way there because it sees more text than it has parameters. So it has to learn the structure that generates the text, and that structure is most of how the world works. It was optimised for plausible, though, never for correct."

> **The question that takes you further:** *if nobody optimised it for truth, what exactly is it that we optimise for after pretraining, and who decides?*

### Checkpoint

1. Why can a frontier model not memorise its training data, in terms of parameters against tokens?
2. Somebody says it is just autocomplete. Give the two-sentence reply.
3. What does the model actually get optimised for during pretraining, and what does that predict about how it fails?
4. A pretrained model is not yet a chatbot. What is missing?

*Act III comes next: how a well-read text engine gets turned into something that will answer your question.*

*[← Back to the series index](ai-internals-00-index.md)*
