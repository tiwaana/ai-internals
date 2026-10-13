# Part 2 — The Perceptron

*[← Part 1b](ai-internals-01b-the-guessing-machine.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md) · Next: [What "Learning" Actually Means →](ai-internals-03-what-learning-means.md)*

Picture yourself picking a college. There are ten things you care about.

- Cost
- Distance from home
- Whether the program is any good
- Weather
- Whether your friend is going
- Class size
- Food
- Whether the campus looks like the brochure
- Sports
- Whether your parents will visit constantly

You probably care about some of these things more than others. Cost could be very important, while sports might not matter much. Maybe your friend's choice matters more than you think.

When I picked Mines for grad school, my real top three were price, whether the program was any good, and friends, which for me meant the Indian community there.

So you give each factor a score, think about how much you care about each one, add everything up, and if the total is high enough, you decide to apply.

Congratulations, you are a perceptron.

Remember the vending machine from Part 1b, where you put in a coin and get chips? This is similar. You have ten factors going in and one decision coming out: apply or skip. A perceptron is the simplest function in this series, and all the bigger ones are built from it.

> 🎓 **Play:** Give the [**Pick a College**](playground.html#college) activity in the playground a try. It uses this type of neuron, with your ten factors and ten adjustable weights. You can use a button to set the weights for you. Mark six or seven colleges as apply or skip, press learn, and it will adjust the weights using Rosenblatt's 1958 rule, which is only one line long. The activity is not animated. If your choices do not follow a clear rule, it will not settle and will let you know.

## This is really all there is to it

This simple process is the foundation for every model we’ll cover in this series.

This process, where you multiply each input by its own number and add up the results, is called a **weighted sum**. It’s the most common idea you’ll hear in this field, and it’s exactly what you just did with the colleges, nothing more.

You might also hear this called a **dot product**, which is just another name for the same thing. When someone says a model is "mostly matrix multiplies," they mean it’s doing lots of weighted sums at the same time.

Frank Rosenblatt came up with this idea in 1958. That July, the Navy showed it to the press, running as a program on an IBM 704. This computer filled an entire room. The New York Times reported that the Navy expected a machine that could walk, talk, see, write, reproduce itself, and even be aware of its own existence.

But in reality, it could only tell if a card was marked on the left or the right.

The hardware version, called the Mark I Perceptron, was released in 1960. It used real motors to turn knobs and adjust the weights, and it learned to tell some letters apart. I am bringing up the press coverage because AI has gone through this kind of hype every fifteen years or so, and we’re in another cycle now.

<svg viewBox="0 0 720 96" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Timeline: 1958 perceptron hype, 1969 the XOR book, 1986 backpropagation, 2012 AlexNet, 2022 ChatGPT">
  <style>
    .tl{stroke:var(--line,#2b3444);stroke-width:2;}
    .td{fill:var(--accent,#4c8dff);}
    .ty{fill:var(--ink,#e6edf3);font:600 12px ui-monospace,monospace;}
    .tc{fill:var(--dim,#9aa7b8);font:11px ui-monospace,monospace;}
  </style>
  <line class="tl" x1="30" y1="40" x2="690" y2="40"/>
  <circle class="td" cx="40" cy="40" r="6"/><text class="ty" x="40" y="24" text-anchor="start">1958</text><text class="tc" x="40" y="64" text-anchor="start">perceptron</text><text class="tc" x="40" y="80" text-anchor="start">hype</text>
  <circle class="td" cx="150" cy="40" r="6"/><text class="ty" x="150" y="24" text-anchor="middle">1969</text><text class="tc" x="150" y="64" text-anchor="middle">the XOR book</text><text class="tc" x="150" y="80" text-anchor="middle">winter</text>
  <circle class="td" cx="320" cy="40" r="6"/><text class="ty" x="320" y="24" text-anchor="middle">1986</text><text class="tc" x="320" y="64" text-anchor="middle">backprop</text>
  <circle class="td" cx="580" cy="40" r="6"/><text class="ty" x="580" y="24" text-anchor="middle">2012</text><text class="tc" x="580" y="64" text-anchor="middle">AlexNet</text>
  <circle class="td" cx="680" cy="40" r="6"/><text class="ty" x="680" y="24" text-anchor="end">2022</text><text class="tc" x="680" y="64" text-anchor="end">ChatGPT</text>
</svg>

## The parts, named

Each part has a name you’ll keep seeing, so let’s get them right from the start.

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Four weighted inputs pour into a gauge; the gauge fills past the dashed bar set by the bias, so the switch flips on and the answer is apply">
  <style>
    .nb{fill:var(--panel2,#1c2230);stroke:var(--line,#2b3444);}
    .nt{fill:var(--ink,#e6edf3);font:600 13px ui-monospace,monospace;}
    .sm{fill:var(--dim,#9aa7b8);font:11px ui-monospace,monospace;}
    .wt{fill:var(--accent,#4c8dff);font:600 11px ui-monospace,monospace;}
    .w{stroke:var(--accent,#4c8dff);fill:none;stroke-linecap:round;}
    .ar{stroke:var(--accent,#4c8dff);stroke-width:2;fill:none;}
    .gf{fill:var(--accent,#4c8dff);opacity:.85;}
    .bar{stroke:#f4b860;stroke-width:2;stroke-dasharray:6 4;}
    .bt{fill:#f4b860;font:600 11px ui-monospace,monospace;}
    .on{fill:var(--accent2,#37d39b);}
    .sw{fill:var(--ink,#e6edf3);}
  </style>
  <text class="sm" x="70" y="18" text-anchor="middle">inputs × weights</text>
  <rect class="nb" x="16" y="30"  width="108" height="30" rx="6"/><text class="nt" x="70" y="50"  text-anchor="middle">cost</text>
  <rect class="nb" x="16" y="74"  width="108" height="30" rx="6"/><text class="nt" x="70" y="94"  text-anchor="middle">distance</text>
  <rect class="nb" x="16" y="118" width="108" height="30" rx="6"/><text class="nt" x="70" y="138" text-anchor="middle">program</text>
  <rect class="nb" x="16" y="162" width="108" height="30" rx="6"/><text class="nt" x="70" y="182" text-anchor="middle">friend</text>
  <path class="w" stroke-width="5.4" d="M124,45  C 190,45  200,120 250,124"/>
  <path class="w" stroke-width="2.4" d="M124,89  C 190,89  200,124 250,128"/>
  <path class="w" stroke-width="4.8" d="M124,133 C 190,133 200,132 250,132"/>
  <path class="w" stroke-width="0.9" d="M124,177 C 190,177 200,140 250,136"/>
  <text class="wt" x="150" y="38">×0.9</text><text class="wt" x="150" y="82">×0.4</text>
  <text class="wt" x="150" y="126">×0.8</text><text class="wt" x="150" y="170">×0.1</text>
  <rect class="nb" x="252" y="30" width="56" height="170" rx="6"/>
  <rect class="gf" x="256" y="70" width="48" height="126" rx="3"/>
  <line class="bar" x1="252" y1="110" x2="330" y2="110"/>
  <text class="bt" x="336" y="106">the bar</text><text class="sm" x="336" y="122">(set by the bias)</text>
  <text class="sm" x="280" y="216" text-anchor="middle">add it all up</text>
  <path class="ar" d="M308,150 C 380,150 400,110 450,110"/>
  <rect class="nb" x="450" y="70" width="70" height="80" rx="10"/>
  <rect x="476" y="84" width="18" height="52" rx="9" style="fill:var(--line,#2b3444)"/>
  <circle class="sw" cx="485" cy="96" r="9"/>
  <text class="nt" x="485" y="170" text-anchor="middle">activation</text>
  <text class="sm" x="485" y="186" text-anchor="middle">over the bar = on</text>
  <path class="ar" d="M520,110 L 590,110"/>
  <circle class="on" cx="634" cy="110" r="34"/><text x="634" y="115" text-anchor="middle" style="fill:#0d1117;font:700 13px ui-monospace,monospace;">apply</text>
  <text class="sm" x="634" y="166" text-anchor="middle">output</text>
</svg>

**Inputs** are the numbers you enter, such as cost, distance, or anything else you need.

**Weights** are paired with each input and show how important each one is. These are the knobs from Part 1b, and they’re the only things the system learns. Everything else in the diagram stays the same.

**Bias** is an extra number added at the end that isn’t connected to any input. It shows how selective you are overall. If you raise it, you accept more. If you lower it, almost nothing gets through. You can think of it as your baseline mood, which is a good comparison.

There was a time when my standards shifted. After I didn’t get a teaching assistantship at my top choice, I became less picky and started looking at other schools where I could get a teaching or research assistantship, since money mattered a lot. The schools didn’t change; my expectations did.

**Activation** is the decision step. The weighted sum gives you a number, say 7.3, and a number on its own decides nothing. Activation turns it into an answer: you are going, or you are not. Rosenblatt's version was a light switch. Over the bar is on, under the bar is off, nothing in between. People call this step **the bend**, because it is where a plain sum turns into a decision. Later models swap the switch for a dimmer, and in Part 7 we will see why that small change mattered so much.

**Output** is just the answer you get at the end.

## Where the knowledge lives

There isn’t a rule about colleges in that diagram. You won’t see a line saying if the cost is over 40000, then reject. There’s also no list of good schools. The structure works the same way whether you’re picking a college, spotting spam, or figuring out that the next word after *"the trophy didn't fit in the case because it was too"* is probably *big*.

All the knowledge is stored in the weights. If you lower the cost setting from 0.9 to 0.1, you start to see money differently, even though you haven’t changed as a person.

That’s why Part 16 of this series discusses who owns the weights file. This is also why the weights are valuable, while the architecture is shared for free in research papers.

## A single neuron has its limits

In 1969, Marvin Minsky and Seymour Papert wrote a book called *Perceptrons*. They proved that a single neuron cannot learn XOR.

Imagine you are throwing a party. Two friends, Alex and Sam, just broke up. Invite either one and the party is great. Invite neither, and it is a bit dull. Invite both, and it is a disaster.

So the rule is **one or the other, but not both.** That rule is XOR, but you do not need to remember the name because it rarely comes up.

A single neuron cannot learn it. Think back to the colleges. Every factor gets its own weight, and the neuron just adds them up. Alex is worth some points and Sam is worth some points. If either one alone is enough to make the party great, then both together are even more points, so the neuron says "great party." It has no knob for *"these two together are trouble."* It scores each guest on their own and never looks at the pair.

There are only four possible guest lists: nobody, Alex, Sam, or both. The reason becomes clear if you draw it. A single neuron can only separate things with one straight line, but you cannot split these four cases like that. If you try with a ruler, you will see it does not work.

<svg viewBox="0 0 720 170" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The four guest lists on a square: no straight line separates the great parties from the bad ones">
  <style>
    .ax3{stroke:var(--line,#2b3444);stroke-width:1.5;}
    .yes{fill:var(--accent2,#37d39b);}
    .no{fill:#f07aa6;}
    .cap3{fill:var(--dim,#9aa7b8);font:11px ui-monospace,monospace;}
    .dl3{fill:var(--ink,#e6edf3);font:600 11px ui-monospace,monospace;}
    .try{stroke:#f4b860;stroke-width:2;stroke-dasharray:5 4;}
  </style>
  <line class="ax3" x1="60" y1="140" x2="220" y2="140"/><line class="ax3" x1="60" y1="140" x2="60" y2="30"/>
  <circle class="no"  cx="60"  cy="140" r="7"/><circle class="yes" cx="200" cy="140" r="7"/>
  <circle class="yes" cx="60"  cy="45"  r="7"/><circle class="no"  cx="200" cy="45"  r="7"/>
  <text class="dl3" x="72"  y="132">nobody</text><text class="dl3" x="212" y="132">Alex</text>
  <text class="dl3" x="72"  y="37">Sam</text><text class="dl3" x="212" y="37">both</text>
  <line class="try" x1="118" y1="22" x2="146" y2="158"/>
  <text class="cap3" x="330" y="40">green = great party,  pink = not</text>
  <text class="cap3" x="330" y="62">a single neuron draws exactly one straight line</text>
  <text class="cap3" x="330" y="84">the dashed line is trying its best</text>
  <text class="cap3" x="330" y="106">it always gets at least one guest list wrong</text>
  <text class="cap3" x="330" y="128">no straight line works</text>
</svg>

The proof was right. The conclusion the field drew from it was that neural networks were a dead end, and the book led to funding drying up for most of the seventies. This period is now known as the first AI winter.

> 🧱 **Try this:** [**The Wall**](playground.html#xor) uses the same tool as before, but now the square is included. Drag the line to try to get all four points right, then let it learn. You’ll see it fail by looping for five hundred passes instead of getting stuck. After that, add a hidden layer and see how the boundary changes and is no longer straight.

Minsky and Papert showed that a single neuron has limits. If you use two layers, you can solve XOR easily. One neuron asks "is at least one of them coming?", another asks "are both coming?", and a third says yes to the first and no to the second. People knew this, but no one knew how to train a stack of neurons until 1986.

For fifteen years, researchers were stuck on a problem even though the solution was already on the whiteboard. This pattern comes up often: sometimes the answer is there, but the field has to wait for something else to make it work. Later in the story, this happens again, but next time, the missing piece is not a method.

> **Try saying this:** "A neuron is a weighted sum plus a bias and a bend. All the knowledge is in the weights, and the architecture is just the shape you pour them into."

> **The question that takes you further:** *if all the knowledge is in the weights, where do those weights come from?*

### Checkpoint

1. Describe a neuron in one sentence, using the words input, weight, bias and activation.
2. What does the bias do that the weights cannot?
3. A single neuron cannot learn "one or the other but not both". What was true about that claim, and what did the field get wrong about what it meant?
4. Somebody says a model is "mostly matrix multiplies". Roughly what are they telling you it spends its time doing?

*Next: [Part 3 — What "Learning" Actually Means →](ai-internals-03-what-learning-means.md), which answers that question.*
