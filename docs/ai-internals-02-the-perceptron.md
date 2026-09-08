# Part 2 — The Perceptron

*[← Part 1b](ai-internals-01b-the-guessing-machine.md) · [Series index](ai-internals-00-index.md) · Next: [What "Learning" Actually Means →](ai-internals-03-what-learning-means.md)*

Before we go anywhere near a language model, I want to build the smallest possible piece of one, because everything after this is that piece repeated a few billion times with better organisation.

Say you are picking a college. You have ten things you care about.

- Cost
- Distance from home
- Whether the programme is any good
- Weather
- Whether your friend is going
- Class size
- Food
- Whether the campus looks like the brochure
- Sports
- Whether your parents will visit constantly

You do not weigh those equally. Cost might matter enormously and sports not at all. Your friend going might matter more than you would admit out loud.

So you score each factor, mentally multiply each score by how much you care, add it all up, and if the total clears some bar you apply.

Congratulations, you are a perceptron.

> 🎓 **Play:** [**Pick a College**](playground.html#college) in the playground is this neuron, with your ten factors and ten weights you can drag. The interesting button is the one that sets the weights for you. Label six or seven colleges as apply or skip, hit learn, and it fits the weights with Rosenblatt's own 1958 rule, which is one line long. Nothing there is animated. If your labels do not follow a consistent rule it genuinely never settles, and it tells you so.

## The whole thing, honestly

Score each thing you care about. Multiply each score by how much you care. Add up the answers. If the total clears a bar, act.

That is it. That is the entire object, and it is the smallest piece of every model in this series.

That operation, **multiply each input by its own number and add up the results**, is called a **weighted sum**. Learn that phrase. It is the single most common thing anyone in this field will say to you, and it means exactly what you just did with the colleges and nothing more.

You will also hear it called a **dot product**, which is the same operation with a more intimidating name. When somebody says a model is "mostly matrix multiplies," they mean it is doing enormous numbers of weighted sums at once. That is the whole sentence decoded. Frank Rosenblatt built it in 1958, and there was a physical machine, the Mark I Perceptron, with actual motors turning actual knobs to adjust the weights. It was meant to recognise shapes. The New York Times went to see it and reported that the Navy expected a machine that would be able to walk, talk, see, write, reproduce itself and be conscious of its existence.

It could tell some triangles from some squares.

I want to flag that early, because AI has had this exact news cycle roughly every fifteen years since, and we are in one now. Knowing what the machine actually does is the only defence.

## The parts, named

Each piece has a name you will see for the rest of your life, so let us do them properly.

<svg viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A single neuron: inputs, weights, sum, activation, output">
  <style>
    .nb{fill:var(--panel2,#1c2230);stroke:var(--line,#2b3444);}
    .nt{fill:var(--ink,#e6edf3);font:600 12px ui-monospace,monospace;}
    .sm{fill:var(--dim,#9aa7b8);font:11px ui-monospace,monospace;}
    .wl{fill:var(--accent,#4c8dff);font:600 11px ui-monospace,monospace;}
    .ln{stroke:var(--line,#2b3444);stroke-width:1.5;fill:none;}
    .hot{stroke:var(--accent,#4c8dff);stroke-width:2;fill:none;}
  </style>
  <g>
    <rect class="nb" x="16" y="24"  width="96" height="26" rx="5"/><text class="nt" x="64" y="42" text-anchor="middle">cost</text>
    <rect class="nb" x="16" y="66"  width="96" height="26" rx="5"/><text class="nt" x="64" y="84" text-anchor="middle">distance</text>
    <rect class="nb" x="16" y="108" width="96" height="26" rx="5"/><text class="nt" x="64" y="126" text-anchor="middle">programme</text>
    <rect class="nb" x="16" y="150" width="96" height="26" rx="5"/><text class="nt" x="64" y="168" text-anchor="middle">friend</text>
  </g>
  <text class="sm" x="64" y="14" text-anchor="middle">inputs</text>
  <path class="hot" d="M112,37  C 170,37  190,90 240,98"/>
  <path class="hot" d="M112,79  C 170,79  195,92 240,100"/>
  <path class="ln"  d="M112,121 C 170,121 195,110 240,104"/>
  <path class="ln"  d="M112,163 C 170,163 200,120 240,108"/>
  <text class="wl" x="150" y="30">w₁ = 0.9</text>
  <text class="wl" x="150" y="72">w₂ = 0.4</text>
  <text class="wl" x="150" y="140" fill="var(--faint,#6b7688)">w₃ = 0.8</text>
  <text class="wl" x="150" y="182" fill="var(--faint,#6b7688)">w₄ = 0.1</text>
  <circle class="nb" cx="272" cy="102" r="32"/><text class="nt" x="272" y="107" text-anchor="middle">Σ</text>
  <text class="sm" x="272" y="152" text-anchor="middle">weighted sum</text>
  <text class="sm" x="272" y="167" text-anchor="middle">+ bias</text>
  <path class="hot" d="M306,102 L 356,102"/>
  <rect class="nb" x="356" y="80" width="104" height="44" rx="8"/><text class="nt" x="408" y="107" text-anchor="middle">activation</text>
  <text class="sm" x="408" y="142" text-anchor="middle">the bend</text>
  <path class="hot" d="M462,102 L 512,102"/>
  <rect class="nb" x="512" y="80" width="92" height="44" rx="8"/><text class="nt" x="558" y="107" text-anchor="middle">output</text>
  <text class="sm" x="558" y="142" text-anchor="middle">apply / don't</text>
</svg>

**Inputs.** The numbers going in. Cost, distance, whatever you have.

**Weights.** One per input, saying how much that input matters. These are the knobs from Part 1b, and they are the only thing that is ever learned. Everything else in the diagram is fixed plumbing.

**Bias.** One extra number added at the end that is not attached to any input. It is how picky you are in general. Turn it up and you apply everywhere, turn it down and nothing clears the bar. Your baseline mood, and yes, that is roughly how it behaves.

**Activation.** The bend. Rosenblatt used a hard threshold, over the bar or not, nothing in between. That turns out to be the thing that made these impossible to train in a stack, and we pay for it in Part 4.

**Output.** The answer.

## Where the knowledge lives

Here is the thing worth stopping on.

Nowhere in that diagram is there a rule about colleges. There is no `if cost > 40000 then reject`. There is no list of good schools. The structure is identical whether you are picking a college, detecting spam, or predicting the next word in a sentence.

**All of the knowledge is in the weights.** Change `w₁` from 0.9 to 0.1 and you have become a different person about money, using the same brain.

That is the whole reason Part 3 of this series is about who owns the weights file, and the reason the weights are the expensive part while the architecture gets published in papers for free. The shape is cheap. The numbers are the thing.

## One neuron cannot do very much

In 1969, Marvin Minsky and Seymour Papert wrote a book called *Perceptrons* which proved, carefully and correctly, that a single one of these cannot learn XOR.

The thing it cannot learn is this: **one or the other, but not both.** Cheese or ham, not cheese and ham. A five-year-old has this. (It has a name, XOR, which you can forget immediately. Nobody will say it to you.)

The reason is easy to see once drawn. One neuron splits the world with a single straight cut, and no single straight cut separates these four cases. Try it with a ruler, it genuinely cannot be done.

<svg viewBox="0 0 720 170" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="XOR is not linearly separable">
  <style>
    .ax3{stroke:var(--line,#2b3444);stroke-width:1.5;}
    .yes{fill:var(--accent2,#37d39b);}
    .no{fill:#f07aa6;}
    .cap3{fill:var(--dim,#9aa7b8);font:11px ui-monospace,monospace;}
    .try{stroke:#f4b860;stroke-width:2;stroke-dasharray:5 4;}
  </style>
  <line class="ax3" x1="60" y1="140" x2="220" y2="140"/><line class="ax3" x1="60" y1="140" x2="60" y2="30"/>
  <circle class="no"  cx="60"  cy="140" r="7"/><circle class="yes" cx="200" cy="140" r="7"/>
  <circle class="yes" cx="60"  cy="45"  r="7"/><circle class="no"  cx="200" cy="45"  r="7"/>
  <line class="try" x1="40" y1="60" x2="230" y2="130"/>
  <text class="cap3" x="140" y="165" text-anchor="middle">no straight line works</text>
  <text class="cap3" x="330" y="60">green = yes,  pink = no</text>
  <text class="cap3" x="330" y="82">a single neuron draws exactly one line</text>
  <text class="cap3" x="330" y="104">the dashed line is trying its best</text>
  <text class="cap3" x="330" y="126">it will always get one point wrong</text>
</svg>

The proof was right. The conclusion the field drew from it was that neural networks were a dead end, and funding dried up for most of the seventies. People call that the first AI winter.

> 🧱 **Play:** [**The Wall**](playground.html#xor) is the same toy with the square above in it. Drag the line and try to get all four points right, then press let it try to learn and watch it fail properly, going round in circles for five hundred passes rather than getting stuck. Then add the hidden layer and watch the boundary stop being straight.

What Minsky and Papert had actually shown was that *one* neuron is limited. Stack two layers and XOR is trivially solvable. Everybody knew that. What nobody had was a way to *train* a stack, and that would not arrive properly until 1986.

So the field spent fifteen years stuck on a problem whose solution was already on the whiteboard, waiting for a method to make it learnable. If that sounds like Part 5, where the same thing happens again with data and GPUs, then you are already reading this series correctly.

> **Say this out loud:** "A neuron is a weighted sum plus a bias plus a bend. All the knowledge is in the weights, and the architecture is just the shape you pour them into."

> **The question that takes you further:** *if all the knowledge is in the weights, where do the weights come from?*

### Checkpoint

1. Describe a neuron in one sentence, using the words input, weight, bias and activation.
2. What does the bias do that the weights cannot?
3. A single neuron cannot learn "one or the other but not both". What was true about that claim, and what did the field get wrong about what it meant?

*Next: [Part 3 — What "Learning" Actually Means →](ai-internals-03-what-learning-means.md), which answers the question you should be asking by now.*
