# Part 3 — What "Learning" Actually Means

*[← Part 2](ai-internals-02-the-perceptron.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md) · Next: [Backpropagation →](ai-internals-04-backpropagation.md)*

You have a neuron. It has weights. All of its knowledge is in those weights, which is a lovely thing to say right up until somebody asks where the numbers come from.

The answer is that you start with random ones and then improve them, and "improve" is doing a suspicious amount of work in that sentence.

The short version comes first. Learning means measuring how wrong you are, nudging the knobs so you are a little less wrong, and doing that thousands of times. There is no insight step. Nobody has an idea. It is closer to sanding something down than to thinking.

## Nothing improves until wrong is a number

You cannot improve what you cannot measure, and "the model is doing badly" is not a number.

Think of a test handed back with "could be better" written across the top and nothing else. You cannot study from that. Now think of the same test marked 62 out of 100, with the wrong answers circled. Next week you can aim at 70, and you will know whether you got there. A machine has no common sense to fall back on, so the number is all it has.

So we define one, called the **loss**. It is a single number that is large when the model is wrong and zero when it is perfect. That is the whole specification. Training never looks at anything else, so everything from here on is about making that one number smaller.

The usual one for prediction is **cross-entropy**, which sounds worse than it is:

```
loss = −log(the probability the model gave to the correct answer)
```

Read that out loud as: **how surprised should the model have been by the right answer.** `log` is there to turn a probability into a penalty, one that climbs without limit as the probability heads toward zero. You will never have to compute one. What you want is how the penalty behaves, which is this:

| The model gave the right answer... | Loss |
|---|---|
| 100%, certain and correct | **0**, nothing to fix |
| 50%, hedging | **0.7** |
| 5%, mostly wrong | **3.0** |
| 0.1%, confidently backing something else | **6.9** |

Being wrong is bad. Being *confidently* wrong is far worse, and the penalty keeps climbing the more certain you were. That is a deliberate choice, and it is why a freshly trained model spreads its bets rather than going all in.

Try it on the trophy sentence from Part 1b. The model gave *big* 41%, so when the right answer really is big, the loss is about 0.9. Had the right word somehow been *purple*, sitting at 0.1%, the loss would have been 6.9, the bottom row of that table.

Which should leave you with an obvious objection. If confident mistakes cost that much, why does a chatbot so often state something false in a perfectly calm voice? Two reasons.

First, the penalty only exists in training, on the pile of text the model was marked against. Ask about something that pile barely covered and nothing ever marked it there, so it falls back on what usually comes next, a fluent sentence shaped like an answer. A student drilled only on past papers does the same with a question they have never seen.

Second, the calm voice is not the model's confidence. The penalty is about the probabilities on each next word, and you never see those. The model can be torn between three dates, pick one, and wrap it in a sentence that sounds completely sure, because that is how the text it learned from sounds. The confidence you hear is in the wording, and the doubt is in numbers nobody shows you. Part 14 is about exactly this.

One prediction you can hold onto. A model guessing blindly between 8 options scores about **2.08** on this. In Part 4 we run one, before any training, and it comes out at 2.1885.

## The loss you pick decides what the machine aims at

Cross-entropy is not the only way to put a number on wrong, and the other common one is older and more obvious. Measure how far off the answer was, square it so that big misses hurt more than small ones, add it all up. If you have ever fitted a line through a scatter of points, that is the rule you were using.

It is a perfectly good rule, and it has a consequence I did not properly respect for years. Suppose the honest answer to some input is genuinely two different things. You show the machine a frame of video of a car approaching a junction, and the next frame is the car turning left or the car turning right. Both are real and both are in the training data. What does that scoring rule reward?

You might expect it to reward committing to one of them. It does not, and you can check that in your head.

Picture the junction from above. Say the left turn is 2 steps to the left of straight ahead, and the right turn is 2 steps to the right. Half the videos go each way. The machine guesses where the car ends up, and every miss gets squared.

- **Guess "left" every time.** Half the time it is spot on, a miss of 0. The other half it is off by 4 steps, which squared is 16. The average cost is 8.
- **Guess "straight ahead" every time.** It is never right. But it is only ever off by 2 steps, which squared is 4. The average cost is 4.

Straight ahead wins, by half. Squaring makes one big miss cost far more than two small ones, so the cheapest place to stand is always halfway between the real answers. And halfway between turning left and turning right is driving straight on into the curb, which is the one thing no car in the training data ever did.

The machine is not hedging and it is not being careful. It is doing exactly what it was told, and what it was told to find was the middle.

You can see this with your own eyes. Image models trained that way came out blurry, and for years that got treated as fuzziness to engineer away with more layers and more data. The blur was the average of every plausible picture, drawn faithfully. No amount of extra capacity fixes a machine that has been asked for the mean.

Cross-entropy, the rule used for prediction, never asks for a single answer. It asks how likely each of the possibilities is, so both futures for the car can hold real weight, and the score depends on how well the whole spread matches reality rather than on how near one guess landed.

Keep that difference somewhere safe. When somebody complains that these things write bland, average-sounding prose, the useful question is which of those two rules the blandness came from, and the answer is not the one most people reach for. We come back to it in Act III.

## Then you roll downhill

Now imagine the loss as a landscape. Every possible setting of the weights is a location, and the height at that location is how wrong the model is. Training is standing somewhere random on that landscape and walking downhill until you reach a valley.

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

Then learning is: nudge each weight a small step in whichever direction its answer said was better, then do it again, and keep doing it.

There is no second mechanism hiding behind this one. The largest models in the world were trained by repeating that.

## The learning rate will ruin your week

How big a step you take is called the **learning rate**, and it is the knob that will personally waste more of your time than any other.

Too small, and you creep. Technically converging, in the sense that a glacier is technically moving.

Too large, and you overshoot the valley, land partway up the far side, overshoot back, and each bounce is bigger than the last. The loss becomes `NaN` and your afternoon is gone. I spent genuine hours of graduate school on this, changing one number and rerunning, and it did not feel like doing mathematics. It felt like tuning a carburetor.

> ⛷️ **Play:** [**Downhill**](playground.html#downhill) in the playground is exactly this, computed for real on two weights. Drag the ball, watch the gradient arrow, then push the learning rate up. Somewhere around 0.22 it genuinely diverges and flies off the screen. Nothing there is animated, so when it explodes it is because the math exploded.

## Where the local minimum worry went

Twenty years ago I was taught to be frightened of **local minima**. You roll downhill into a small dip, every direction around you goes up, so you stop, and you never find the real valley. On a whiteboard, drawn in two dimensions, that looks terrifying.

With a few billion weights it is mostly a non-issue. To trap you, a dip has to curve upward in *every single direction*, and with a billion directions the odds that not one of them slopes down are effectively nil. What you actually meet are saddle points, which look flat and are not, and you slide off them eventually.

So one of the field's central anxieties turned out to be an artifact of drawing the diagram in two dimensions. I find that genuinely funny and slightly humbling.

> **Say this out loud:** "Training is putting a number on how wrong you are, then nudging every weight in whichever direction makes that number smaller. The learning rate is how big the nudge is, and too big and it never settles."

> **The question that takes you further:** *fine, but with a billion weights, how do you work out the gradient for every single one without doing a billion separate experiments?*

### Checkpoint

1. Two plausible answers, both correct, both in the training data. Explain what the squared-distance rule rewards and why, without using any math.
2. Cross-entropy punishes being confidently wrong far more than being uncertainly wrong. Why is that a sensible design choice?
3. Why is the local-minimum problem less frightening in a billion dimensions than in two?

*Next: [Part 4 — Backpropagation →](ai-internals-04-backpropagation.md), which answers that question and is the reason any of this is possible at all.*
