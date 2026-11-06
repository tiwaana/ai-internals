# Part 4 — Backpropagation

*[← Part 3](ai-internals-03-what-learning-means.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md) · Next: [Why It Was All Kind of Terrible in 2002 →](ai-internals-05-terrible-in-2002.md)*

Part 3 ended with a cook tasting a dish and deciding for each ingredient whether to add more or less. That's easy when there are only three ingredients. In a real network, though, there are a billion knobs, and step 2 has to do this for every single one.

The simplest way is to test each knob one by one. You adjust the first knob, cook the dish again, taste it, and see if the loss (Part 3's score for how far off the dish is) went down. Then you put the knob back and try the next one.

If there are a billion knobs, you'd have to run the whole network for each one. If each run takes a millisecond, just one training step would take eleven days. And you have to repeat this hundreds of thousands of times.

That's thousands of years of training, and slow is too kind a word for it. Modern AI works because there's a much better way, and it comes from calculus invented in the seventeenth century.

## The blame flows backwards

You don't need to test each knob separately because they're all linked in a chain, and each one influences the final answer through the layers that come after. So, you begin at the end, where you know how the answer was graded, and then move backwards through each layer.

This is where the single cook from Part 3 becomes a whole kitchen. In a network, each station works with what the previous one gives it. Imagine the kitchen sends out a bad dish. You give the plating station a note: if you change what you send out like this, the score changes like that. The plating station uses the note to figure out what its own knobs did. Then it writes a new note for the grilling station, explaining how the score would change if the grilling station handed over something different. The grilling station doesn't need to meet the customer because the note already covers everything that happens after it. After one trip through the kitchen, every station knows what to change.

I'll keep calling that number **blame**, with one warning. Blame here means how much the final score would change if this thing changed a bit. It's not like sharing a pie. Two stations can both have a lot of blame, and if one has more, it doesn't mean the other has less.

Let's use numbers. Suppose adding a tiny pinch of salt at plating station changes the final score by 3. That's plating's note. Now, if a tiny pinch at the grilling station adds 2 pinches to what the plating station gets, the grilling station's blame is 2 times 3, which is 6. Nobody had to cook again to figure this out because the 3 was already on the note.

That multiplying along the line is called the **chain rule**. It might seem old and boring, but it's the most valuable idea in this series. Backpropagation uses the chain rule in reverse through the network, with each note worked out once and reused by everything before it. That reuse is what saves time.

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
  <text class="cap5" x="40" y="170" fill="var(--dim,#9aa7b8)">one backward pass gets the gradient for every weight, for about the cost of a few forward passes</text>
</svg>

What's really surprising is how little it costs. With just one backward pass, you get the **gradient** for every weight in the network. It tells you which way to move each knob, and how strongly, like more salt or less. Whether you call it blame in the kitchen, slope on a mountainside, or gradient in a meeting, it's the same idea: one number, just with different names. A backward pass costs about as much as a few forward passes, so instead of paying for a billion trips through the kitchen, you only pay for one round trip.

With our network, something that would have taken eleven days now takes just a few milliseconds. That's why training large models is possible.

> 🍳 **Play:** [**Check the Blame**](playground.html#blame) in the playground uses a real network with 121 weights, and it calculates the blame both ways. If you press the slow button, you'll see the counter go up to 121 as it cooks the dish again for each weight. If you press the fast button, it just says 1. Look at the bars: both methods give you the same answer, accurate to six decimal places. So backprop doesn't lose any accuracy.

## It is older than the hype

Several people discovered the algorithm independently, unaware of each other's work. Seppo Linnainmaa first introduced the general method in 1970 as part of numerical analysis, with no link to neural networks. A few years later, Paul Werbos applied it to networks in his 1974 thesis, but people largely overlooked his work at the time.

The algorithm gained widespread attention after Rumelhart, Hinton, and Williams published a paper about it in *Nature* in 1986. Their work showed how the method could be used and reached many influential people.

In PyTorch, the tool most people use to train models, this process happens with just one line: `loss.backward()`. Many people who use it have never looked under the hood, which makes sense. After all, you can drive a car without knowing how the engine works. Still, let's take a look, since the main idea only takes about a dozen lines.

## Watch how it learns to say "hello world"

Enough. Let's run one.

This is a small model, so doing backpropagation by hand is easy to follow. It predicts the next character using the previous two. Each character turns into a short list of numbers, which go through two sets of knobs with a gate in between. In Part 2, this step was called the bend, where a simple sum becomes a decision. Softmax then changes the output into percentages. The loop comes from Part 3, now with four steps: first, cook the dish (the forward pass), then taste it (the loss). Next, figure out what to change for each knob (backpropagation, which is new here), and finally, adjust each knob by its slope times the step size.

> If you want to try it yourself, download and run [`train_hello.py`](train_hello.py). You'll need to install numpy with pip (`pip install numpy`). You don't need a GPU or any special framework.

If you don't write Python, skip this block. The main thing to focus on is the printout in the next section, which is just plain numbers. If you do want to look, a few things help: `@` stands for a weighted sum from Part 2, applied to a group of numbers at once. Any name starting with `d` means "the blame belonging to this thing." `.T` flips a grid on its side so things line up, which is just bookkeeping. `logits` are the raw scores for each character before softmax turns them into percentages.

One line is worth highlighting: the one with `hpre > 0`. In this model, the gate changes any negative value to zero. If a unit is below zero, its gate is closed. Adjusting its dial has no effect, so no blame passes through. Part 5 will introduce the proper name for this gate.

```python
for step in range(2001):
    # 1) FORWARD: what does it predict right now?
    probs, (emb, hpre, h, _) = forward(X)
    # 2) LOSS: how wrong is that?
    L = loss_fn(probs, Y)
    # 3) BACKWARD: whose fault, and by how much?
    dlogits = probs.copy()               # what the model predicted...
    dlogits[np.arange(N), Y] -= 1        # ...minus what was true
    dlogits /= N                         # averaged over the examples
    dW2 = h.T @ dlogits
    db2 = dlogits.sum(0)
    dh  = dlogits @ W2.T
    dhpre = dh * (hpre > 0)              # no blame passes a shut gate
    dW1 = emb.T @ dhpre
    db1 = dhpre.sum(0)
    # ... the same again for E, the table of character numbers ...
    # 4) UPDATE: everybody take one step downhill
    for p, g in [(W1,dW1),(b1,db1),(W2,dW2),(b2,db2),(E,dE)]:
        p -= lr * g
```

Two lines are worth stopping on. Backprop's first job is deciding which way each output score should change. You would expect a page of algebra here. With softmax and Part 3's grading, it comes down to one subtraction:

**Take what the model predicted and subtract what was actually true.**

For example, let's say the correct character is `l`. The model gives `l` a 0.70 chance (70%) and `d` a 0.20 chance. The true values are 1 for `l` and 0 for `d`. So for `l`, you do 0.70 minus 1, which is -0.30. A negative result means you should raise this score. For `d`, you do 0.20 minus 0, which is 0.20, so you should lower it.

You might expect the model to get a zero if it picks the right character, but that's not how it works. The numbers only reach zero when the model is totally sure of the right answer. So even if it's right but not confident, it still gets changed.

That subtraction is only the first note in the kitchen. Backprop uses this information and sends it back through each station. The step size from Part 3 still controls how much each knob moves.

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

Let's look at step 0. The loss is **2.1885**. We could have roughly predicted this before running the model. If the model is equally unsure about all eight characters, it gives each one a 12.5% chance. Part 3's grading turns 12.5% into a loss of about 2.08. So, 2.08 is the loss you get for a completely even guess.

We got 2.19, which is close but not exactly the same. Random settings don't guess perfectly evenly. In this run, the model gave the right characters anywhere from 4% to 19%, so the score was a bit higher than the even-guess score. Engineers check this number because if it starts much higher, it's a sign to review the setup before training.

By step 250, the loss drops to 0.0013 and the output is already correct. The answer stays the same after that, but the loss keeps going down to 0.0001 as the model gets even more confident.

Next is generation. Starting with just `"he"`, the model uses its own output as input and rebuilds the rest one character at a time. This is the autoregressive loop from Part 1b, but now the weights have learned something.

## What it did not do

Let's take a step back. The model had nine examples and 872 weights. It simply **memorized** them. There was enough space to store the answers, so that's what happened.

Call it a lookup table that took the scenic route. As mentioned at the end of Part 3, what really matters is how the model does on examples it hasn't seen before. We didn't test that.

Things get interesting when you give a model much more data than it can possibly memorize. That's the point made in Part 1b, and it comes up again in Part 11.

Our simple model couldn't handle the sentence this series is focused on: *"The trophy didn't fit in the case because it was too big."* Since it only looks at two characters at a time, by the time it gets to "it," the trophy is already out of view. To figure out what "it" refers to, a model needs much more advanced processing. That's what Act II is about. The training method is already set: cook, taste, blame, adjust, and go around again. From here, it's the same process, just with a bigger model and more data.

> **Say this out loud:** "Backprop pushes blame backwards from the answer through every layer in one trip, so you find out how every weight moves the loss for about the cost of running the model a few times. Without it, training anything large would be arithmetically impossible."

> **The question that takes you further:** *if we had this in 1986, why did the major breakthrough not happen until around 2012?*

### Checkpoint

1. Why can you not just nudge each weight and re-run to find its gradient?
2. In one sentence, why is passing blame backwards through the layers so much cheaper than testing weights one at a time?
3. We expected a starting loss near 2.08 and got 2.1885. Where did 2.08 come from, and why was the real number not exactly that?
4. Our model got all nine examples right. Why does that not show it would do well on text it has never seen?

*Next: [Part 5 — Why It Was All Kind of Terrible in 2002 →](ai-internals-05-terrible-in-2002.md). There, I'll explain why having all this knowledge didn't actually help for twenty years.*
