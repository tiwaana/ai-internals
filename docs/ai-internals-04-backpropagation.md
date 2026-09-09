# Part 4 — Backpropagation

*[← Part 3](ai-internals-03-what-learning-means.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md) · Next: [Why It Was All Kind of Terrible in 2002 →](ai-internals-05-terrible-in-2002.md)*

You have a network. It got the answer wrong. Somewhere inside are a billion weights, and you need to know, for every one of them, how much of the blame it personally deserves.

The obvious method is to test them. Nudge weight number one, run the whole network again, see if the loss improved. Then put it back and try weight number two.

A billion weights, a forward pass each. If a forward pass takes a millisecond you are done in eleven days, and that gets you **one** training step. You need a few hundred thousand of them.

So the obvious method is not merely slow, it is not on the same planet as feasible. Modern AI exists because there is a much better way, and the better way is a piece of calculus from the seventeenth century.

## The blame flows backwards

Here is the shape of the trick before the mechanics.

You do not need to test each weight, because the weights are not independent. They sit in a chain. The answer came from the last layer, which was working from what the layer before it handed over, and so on all the way back.

So you do not ask each weight separately. You start at the end, where you know exactly how wrong the answer was, and you push that blame backwards one layer at a time.

Think of a kitchen sending out a bad dish. You do not interview every cook individually. You tell the plating station what was wrong, they work out which part was their fault and pass the rest back to the grill, who does the same and passes it back again. One trip through the kitchen and everyone knows what to fix.

The formal name for that trick is the **chain rule**, and it is old and dull and the most valuable thing in this series. Each layer receives "here is how much you contributed to the error," works out how to divide that among its own weights, and passes the remainder further back.

<svg viewBox="0 0 720 190" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Forward pass then backward pass">
  <style>
    .lb5{fill:var(--panel2,#1c2230);stroke:var(--line,#2b3444);}
    .tx5{fill:var(--ink,#e6edf3);font:600 12px ui-monospace,monospace;}
    .fw{stroke:var(--accent,#4c8dff);stroke-width:2.5;fill:none;}
    .bw{stroke:#f07aa6;stroke-width:2.5;fill:none;}
    .cap5{font:11px ui-monospace,monospace;}
  </style>
  <rect class="lb5" x="40"  y="60" width="76" height="40" rx="8"/><text class="tx5" x="78"  y="85" text-anchor="middle">input</text>
  <rect class="lb5" x="176" y="60" width="76" height="40" rx="8"/><text class="tx5" x="214" y="85" text-anchor="middle">layer 1</text>
  <rect class="lb5" x="312" y="60" width="76" height="40" rx="8"/><text class="tx5" x="350" y="85" text-anchor="middle">layer 2</text>
  <rect class="lb5" x="448" y="60" width="76" height="40" rx="8"/><text class="tx5" x="486" y="85" text-anchor="middle">layer 3</text>
  <rect class="lb5" x="584" y="60" width="90" height="40" rx="8"/><text class="tx5" x="629" y="85" text-anchor="middle">loss</text>
  <path class="fw" d="M116,72 L 172,72" marker-end="url(#f5)"/>
  <path class="fw" d="M252,72 L 308,72" marker-end="url(#f5)"/>
  <path class="fw" d="M388,72 L 444,72" marker-end="url(#f5)"/>
  <path class="fw" d="M524,72 L 580,72" marker-end="url(#f5)"/>
  <path class="bw" d="M580,92 L 528,92" marker-end="url(#b5)"/>
  <path class="bw" d="M444,92 L 392,92" marker-end="url(#b5)"/>
  <path class="bw" d="M308,92 L 256,92" marker-end="url(#b5)"/>
  <path class="bw" d="M172,92 L 120,92" marker-end="url(#b5)"/>
  <defs>
    <marker id="f5" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--accent,#4c8dff)"/></marker>
    <marker id="b5" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#f07aa6"/></marker>
  </defs>
  <text class="cap5" x="300" y="36" fill="var(--accent,#4c8dff)">forward: what did we predict?</text>
  <text class="cap5" x="300" y="140" fill="#f07aa6">backward: who is to blame?</text>
  <text class="cap5" x="40" y="170" fill="var(--dim,#9aa7b8)">one backward pass gets the gradient for every weight, at about the cost of one forward pass</text>
</svg>

The remarkable part is the cost. **One backward pass produces the gradient for every weight in the network,** and it costs roughly what one forward pass costs. Not a billion passes. One.

Eleven days becomes two milliseconds. That is the entire reason large models can be trained, and it is why backpropagation is the single most consequential algorithm in the field.

## It is older than the hype

The algorithm has been invented several times by people who did not know about each other. Seppo Linnainmaa published the general method in 1970, as a piece of numerical analysis with no neural networks anywhere near it. Paul Werbos applied it to networks in his 1974 thesis and it went largely unnoticed.

What made it stick was a 1986 paper in *Nature* by Rumelhart, Hinton and Williams, which showed it working and got read by the right people.

So the algorithm behind the 2020s was published the year *Top Gun* came out. It then sat there being mostly disappointing for twenty-six years. Part 5 is about why.

In PyTorch this is a single line, `loss.backward()`, and a whole generation of practitioners has never looked underneath it. That is fine, in the way not knowing how a compiler works is fine. We are going to look anyway, because you are here for internals, and because it turns out to be about six lines.

## Watch it learn "hello world"

Enough. Let us run one.

Small model so the by-hand backprop stays readable: predict the next character from the previous two. Each character is turned into a short list of numbers, those go through one layer of knobs, and softmax turns what comes out into percentages. The four steps are identical to what trains a transformer, and only the model in the middle is bigger.

> **Download and run:** [`train_hello.py`](train_hello.py) (`pip install numpy`). No GPU, no framework.

**If you do not write Python, skip the block.** The printout in the next section is the part that matters and it is plain numbers. If you do want to look, three things and it reads like English: `@` is the weighted sum from Part 2 done to a pile of numbers at once, a name starting with `d` is "the blame belonging to this thing", and `.T` flips a grid on its side so two things line up, which is bookkeeping and not an idea.

```python
for step in range(2001):
    # 1) FORWARD — what does it predict right now?
    probs, (emb, hpre, h, _) = forward(X)
    # 2) LOSS — how wrong is that?
    L = loss_fn(probs, Y)
    # 3) BACKWARD — whose fault, and by how much?
    dlogits = probs.copy(); dlogits[np.arange(N), Y] -= 1; dlogits /= N
    dW2 = h.T @ dlogits;      db2 = dlogits.sum(0)
    dh  = dlogits @ W2.T
    dhpre = dh * (hpre > 0)              # blame stops at the bend (Part 5 names it)
    dW1 = emb.T @ dhpre;      db1 = dhpre.sum(0)
    # ... (scatter gradients back into the embedding table) ...
    # 4) UPDATE — everybody take one step downhill
    for p, g in [(W1,dW1),(b1,db1),(W2,dW2),(b2,db2),(E,dE)]:
        p -= lr * g
```

One line is worth stopping on. The step that works out how wrong the answer was, which looks like it should take a page of algebra, is this:

**what the model predicted, minus what was true.**

That is the whole calculation. If the model was already right, that comes out as zero and nothing moves. The size of the mistake *is* the size of the correction, exactly, with no conversion factor in between.

I remember being shown that and refusing to believe it was that clean. It is that clean.

## The real output

Actual numbers from an actual run.

```
9 training examples (context of 2 chars -> next char):
   ['h', 'e'] -> 'l'      ['o', ' '] -> 'w'      ['o', 'r'] -> 'l'
   ['e', 'l'] -> 'l'      [' ', 'w'] -> 'o'      ['r', 'l'] -> 'd'
   ['l', 'l'] -> 'o'      ['w', 'o'] -> 'r'
   ['l', 'o'] -> ' '

TRAINING (full-batch gradient descent):
 step     loss   prediction so far
    0   2.1885   he[hdhhhhdhh]      <- random weights: guessing
  250   0.0013   he[llo world]      <- already solved
  500   0.0005   he[llo world]
 ...
 2000   0.0001   he[llo world]      <- confidently correct

GENERATION (seed 'he', model writes the rest):
   -> 'hello world'
   target: 'hello world'   MATCH
```

Look at step 0. Loss **2.1885**. In Part 3 I said a model guessing blindly between eight options would score about 2.08, before we had run anything at all, and there it is. The model really is guessing uniformly over eight characters, and the theory told us the number in advance. That is the moment to decide whether you believe this stuff, and I think you should.

By step 250 the loss has collapsed to 0.0013 and the output is already right. A few hundred trips around a four-step loop found weights that encode the sequence.

Then generation. Seeded with only `"he"`, the model feeds its own output back into itself and reconstructs the rest one character at a time. That is the autoregressive loop from Part 1b, now running on weights that know something.

## What it did not do

Before anyone gets carried away, be clear about what just happened. Nine examples, about two thousand weights. It **memorised**. There was more than enough capacity to store the answer, so it stored the answer.

That is not intelligence, it is a lookup table that took the scenic route.

The interesting thing happens when you take memorisation off the table entirely, by showing a model far more data than it could ever store. Then the only remaining way to reduce the loss is to learn the structure that *generates* the data. That is the argument from Part 1b, and it is what Part 11 is about.

But every mechanism you need is now on the table. Four steps, one loop. Everything after this is that loop, on a bigger model, with more data.

> **Say this out loud:** "Backprop pushes blame backwards from the answer through every layer in one trip, so you find out what every weight did wrong for about the cost of running the model once. Without it, training anything large would be arithmetically impossible."

> **The question that takes you further:** *if we had this in 1986, why did it take until roughly 2012 to work?*

### Checkpoint

1. Why can you not just nudge each weight and re-run to find its gradient?
2. In one sentence, why is passing blame backwards through the layers so much cheaper than testing weights one at a time?
3. We predicted a starting loss of 2.08 and got 2.1885. Where did 2.08 come from?
4. Our model memorised nine examples. Why is that not the same as learning?

*Next: [Part 5 — Why It Was All Kind of Terrible in 2002 →](ai-internals-05-terrible-in-2002.md), which is the part where I explain why knowing all of this got you nowhere for twenty years.*
