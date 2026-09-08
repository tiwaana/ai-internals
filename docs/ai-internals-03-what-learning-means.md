# Part 3 — What "Learning" Actually Means

*[← Part 2](ai-internals-02-the-perceptron.md) · [Series index](ai-internals-00-index.md) · Next: [Backpropagation →](ai-internals-04-backpropagation.md)*

You have a neuron. It has weights. All of its knowledge is in those weights, which is a lovely thing to say right up until somebody asks where the numbers come from.

The answer is that you start with random ones and then improve them, and "improve" is doing a suspicious amount of work in that sentence. This part is about what it actually means.

Here is the shape of it before the details. **Learning is being wrong in a measurable way, then being slightly less wrong, several thousand times.** There is no insight step. Nobody has an idea. It is closer to sanding something down than to thinking.

## First you need a number for wrong

You cannot improve what you cannot measure, and "the model is doing badly" is not a number.

So we define one, called the **loss**. It is a single number that is large when the model is wrong and zero when it is perfect. That is the whole specification.

The usual one for prediction is **cross-entropy**, which sounds worse than it is:

```
loss = −log(the probability the model gave to the correct answer)
```

Read that out loud as: **how surprised should the model have been by the right answer.** `log` is a squashing function, and it is there to turn a probability into a penalty. You will never have to compute one, and nobody will ask you to. What you want is how the penalty behaves, which is this:

| The model gave the right answer... | Loss |
|---|---|
| 100%, certain and correct | **0** — nothing to fix |
| 50%, hedging | **0.7** |
| 5%, mostly wrong | **3.0** |
| 0.1%, confidently backing something else | **6.9** |

Being wrong is bad. Being *confidently* wrong is far worse, and the penalty keeps climbing the more certain you were. That is a deliberate choice and it is a large part of why models hedge.

One prediction you can hold onto. A model guessing blindly between 8 options scores about **2.08** on this. In Part 4 we run one and it comes out at 2.1885, and watching a number you predicted in advance turn up in a real run is the moment to decide whether you believe any of this.

## The loss you pick decides what the machine aims at

Cross-entropy is not the only way to put a number on wrong, and the other common one is older and more obvious. Measure how far off the answer was, square it so that big misses hurt more than small ones, add it all up. If you have ever fitted a line through a scatter of points, that is the rule you were using.

It is a perfectly good rule, and it has a consequence I did not properly respect for years. Suppose the honest answer to some input is genuinely two different things. You show the machine a frame of video of a car approaching a junction, and the next frame is the car turning left or the car turning right. Both are real. Both are in the training data. What does that scoring rule reward?

The tempting answer is that it rewards committing to one of them. It does not. Squaring the distance means the cheapest place to stand is halfway between, because being a little bit wrong about both costs less than being completely wrong about one. The machine is not hedging and it is not being careful. It is doing exactly what it was told, and what it was told to find was the middle.

You can see this with your own eyes. Image models trained that way came out blurry, and for years that got described as a quality problem, some fuzziness to be engineered away with more layers and more data. The blur was the average of every plausible picture, drawn faithfully. No amount of extra capacity fixes a machine that has been asked for the mean.

Cross-entropy does not do that, which is why it is the one used for prediction. It never asks for a single answer. It asks how likely each of the possibilities is, so both futures for the car can hold real weight, and the score depends on how well the whole spread matches reality rather than on how near one guess landed.

Keep that difference somewhere safe. When somebody complains that these things write bland, average-sounding prose, the useful question is which of those two rules the blandness came from, and the answer is not the one most people reach for. We come back to it in Act III.

## Then you roll downhill

Now imagine the loss as a landscape.

Every possible setting of the weights is a location, and the height at that location is how wrong the model is. Training is standing somewhere random on that landscape and walking downhill until you reach a valley.

<svg viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Gradient descent down a loss curve">
  <style>
    .curve{fill:none;stroke:var(--accent,#4c8dff);stroke-width:2.5;}
    .ball{fill:#f07aa6;}
    .t4{fill:var(--dim,#9aa7b8);font:12px ui-monospace,monospace;}
    .ax4{stroke:var(--line,#2b3444);stroke-width:1.5;}
    .step{stroke:#37d39b;stroke-width:2;fill:none;}
  </style>
  <line class="ax4" x1="50" y1="170" x2="670" y2="170"/>
  <line class="ax4" x1="50" y1="170" x2="50" y2="20"/>
  <path class="curve" d="M70,40 C 200,190 300,175 360,150 C 430,120 520,60 660,35"/>
  <circle class="ball" cx="110" cy="110" r="8"/>
  <path class="step" d="M120,116 L 168,150" marker-end="url(#ar)"/>
  <defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#37d39b"/></marker></defs>
  <circle class="ball" cx="360" cy="150" r="8" opacity="0.45"/>
  <text class="t4" x="110" y="95" text-anchor="middle">you start here</text>
  <text class="t4" x="360" y="182" text-anchor="middle">the valley</text>
  <text class="t4" x="20" y="95" transform="rotate(-90 20,95)">loss</text>
  <text class="t4" x="600" y="188">weights →</text>
</svg>

To walk downhill you need to know which way is down. For each individual weight, that means asking one question.

**If I nudge this weight a tiny bit, does the loss get better or worse, and by how much?**

The answer has a name. It is called the **gradient**, and it means nothing more exotic than *which way, and how steeply*. Every weight gets its own answer.

Then learning is: nudge each weight a small step in whichever direction its answer said was better. Then do it again. And again.

That is the whole thing. I want to be blunt that there is no second mechanism hiding behind this one. The largest models in the world were trained by repeating that.

## The learning rate will ruin your week

How big a step you take is called the **learning rate**, and it is the knob that will personally waste more of your time than any other.

Too small, and you creep. Technically converging, in the sense that a glacier is technically moving.

Too large, and you overshoot the valley, land partway up the far side, overshoot back, and each bounce is bigger than the last. The loss becomes `NaN` and your afternoon is gone. I spent genuine hours of graduate school on this, changing one number and rerunning, and it did not feel like doing mathematics. It felt like tuning a carburettor.

> ⛷️ **Play:** [**Downhill**](playground.html#downhill) in the playground is exactly this, computed for real on two weights. Drag the ball, watch the gradient arrow, then push the learning rate up. Somewhere around 0.22 it genuinely diverges and flies off the screen. Nothing there is animated, so when it explodes it is because the maths exploded.

Go and break it. It takes ten seconds and it will teach you more about learning rates than the rest of this section.

## Where the local minimum worry went

If you did any of this twenty years ago, there is a thing you were taught to be frightened of, and it is worth updating.

The fear was **local minima**. You roll downhill into a small dip, you are surrounded by higher ground in every direction so you stop, and you never find the real valley. In two dimensions that is obviously a problem, which is why the picture above makes it look terrifying.

In two dimensions. With a few billion weights it turns out to be mostly a non-issue, and the reason is quite pretty. For a point to be a local minimum, the ground has to curve upward in *every single direction*. With a billion directions, the odds that not one of them slopes down are effectively nil. What you actually get is saddle points, which look flat and are not, and you slide off them eventually.

So one of the field's central anxieties turned out to be an artifact of drawing the diagram in two dimensions. I find that genuinely funny and slightly humbling.

> **Say this out loud:** "Training is putting a number on how wrong you are, then nudging every weight in whichever direction makes that number smaller. The learning rate is how big the nudge is, and too big and it never settles."

> **The question that takes you further:** *fine, but with a billion weights, how do you work out the gradient for every single one without doing a billion separate experiments?*

### Checkpoint

1. Two plausible answers, both correct, both in the training data. Explain what the squared-distance rule rewards and why, without using any maths.
2. Cross-entropy punishes being confidently wrong far more than being uncertainly wrong. Why is that a sensible design choice?
3. Describe what you would see happen if the steps were far too big.
4. Why is the local-minimum problem less frightening in a billion dimensions than in two?

*Next: [Part 4 — Backpropagation →](ai-internals-04-backpropagation.md), which answers that question and is the reason any of this is possible at all.*
