# Part 1b — The Guessing Machine

*[← Part 1a](ai-internals-01a-what-changed.md) · [Series index](ai-internals-00-index.md) · Next: [The Perceptron →](ai-internals-02-the-perceptron.md)*

That was the story. This is the prep work.

Two things happen here. First the one idea you actually need, which is smaller than you are expecting. Then the one thing the machine does, which is also smaller than you are expecting.

After this part, you are caught up and we go together.

## The only word you need

There is one word doing all the work in this series, and it is **function**.

A function is a thing you put something into and get something out of. A vending machine is a function. You put in a coin, you get out a packet of crisps. A recipe is a function: ingredients in, dinner out.

That is the whole concept, and you already had it.

A model is a function. Enormous, but a function. Text goes in, a guess at the next word comes out. Inside it are smaller functions feeding each other, and inside those are smaller ones still, and at the very bottom is something so simple it is almost disappointing. That bottom piece is what we build in Part 2.

Three words you will meet later. I am naming them now so they are not intimidating when they turn up, and none of them mean what the notation suggests.

- A **weight** is a knob. It says how much one thing matters. All the knobs together are the model's knowledge, and they are the only part that is ever learned.
- A **weighted sum**, also called a **dot product**, is multiplying some things by their knobs and adding up the answers. Two frightening names for arithmetic you could do on paper. This one is worth keeping, because people in this field say it constantly. Part 2 builds it properly.
- **Softmax** turns a list of scores into percentages that add up to 100. You are about to watch one work, in the next section.

That is the toolkit. You do not need algebra, you will never be asked to solve for anything, and where a formula appears later it is there to be pointed at, not worked through.

I am not softening that to make you feel better. I can promise it because I already know what is coming.

## The whole machine does one thing, it guesses the next word

This is the fact that surprised me most on coming back, because it sounds far too small to be true.

You give the model some text. It hands back a probability for every word that could come next. It picks one, sticks it on the end, and runs the whole thing again on the slightly longer text. That is the loop. Entire essays get built one word at a time by something that is never planning further ahead than the next word.

Feed it *"The trophy didn't fit in the case because it was too"* and you get back something like this.

<svg viewBox="0 0 720 190" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Next-word probabilities">
  <style>
    .bar{fill:var(--accent,#4c8dff);}
    .bar2{fill:var(--accent2,#37d39b);}
    .lb{fill:var(--ink,#e6edf3);font:600 13px ui-monospace,monospace;}
    .pc{fill:var(--dim,#9aa7b8);font:12px ui-monospace,monospace;}
    .ax{stroke:var(--line,#2b3444);stroke-width:1.5;}
  </style>
  <line class="ax" x1="120" y1="12" x2="120" y2="172"/>
  <g><rect class="bar" x="120" y="18" width="330" height="22" rx="3"/><text class="lb" x="112" y="34" text-anchor="end">big</text><text class="pc" x="460" y="34">41%</text></g>
  <g><rect class="bar" x="120" y="52" width="215" height="22" rx="3"/><text class="lb" x="112" y="68" text-anchor="end">small</text><text class="pc" x="345" y="68">27%</text></g>
  <g><rect class="bar2" x="120" y="86" width="95" height="22" rx="3"/><text class="lb" x="112" y="102" text-anchor="end">large</text><text class="pc" x="225" y="102">12%</text></g>
  <g><rect class="bar2" x="120" y="120" width="48" height="22" rx="3"/><text class="lb" x="112" y="136" text-anchor="end">heavy</text><text class="pc" x="178" y="136">6%</text></g>
  <g><rect class="bar2" x="120" y="154" width="9" height="22" rx="3"/><text class="lb" x="112" y="170" text-anchor="end">purple</text><text class="pc" x="139" y="170">0.1%</text></g>
</svg>

Look at `purple` at the bottom. It did not get zero. Nothing gets zero. Turn the randomness up far enough and the model will eventually say purple, and that is a fair chunk of what people are pointing at when they say a model hallucinated.

My first reaction was, fine, so it is autocomplete. My phone does this above the keyboard.

## So it is just autocomplete?

Hold onto that objection, because the way it comes apart is the most useful thing in this part.

The picture in my head was a lookup table. The model read an enormous pile of text, remembered which words tend to follow which, and plays it back. A parrot with a very good memory. That is roughly what a language model *was*, in my day.

You can go build that parrot right now, it takes about ten seconds.

> 🦜 **Play:** [**Feed the Parrot**](playground.html#parrot) in the playground. Type some text in, hit train, and it builds exactly that table: for every pair of words, which word came next. Then let it write. It works, genuinely, on your own text, which is the surprising part. Then ask it for something slightly off its script and watch it fall apart.

The parrot does not fail because it needs more text. It fails on arithmetic.

Take a twenty word sentence, drawn from a vocabulary of fifty thousand words. The number of possible twenty word sentences is 50,000²⁰, a number with about 94 digits in it. There are somewhere around 80 digits worth of atoms in the observable universe. Which means almost every sentence you have ever read was the first time that exact sentence had existed anywhere.

So let me put it point blank. There is nothing to look up. A machine that has to guess the next word across all of human writing cannot pass that test by remembering, there is not enough room in the universe to store the answers. Its only option is to compress. It has to work out the rules that generate all those sentences and keep the rules instead.

And the rules of human text turn out to include almost everything we know. It has to learn grammar, because bad grammar leads to bad guesses. It has to learn facts, because "the capital of France is" has one right answer and every wrong guess is punished. It has to learn arithmetic, because sums appear in text and they come out a particular way. It has to learn that trophies are big and cases are things you put objects into. It even has to learn that a person who was angry in the first paragraph is usually still angry in the third, because that changes which word comes next.

Nobody sat down and taught it any of that. All of it got squeezed out under pressure, because knowing it made the next guess better.

I still call it autocomplete. I just stopped thinking that was a small thing to be.

## What else? The machine is a file

This is the other thing that caught me off guard, and it is the bit my twenty-years-ago self would have found strangest.

This machine, the one that knows trophies are big, is a file. You can copy it onto a drive. It is mostly one very long list of decimal numbers and there are billions of them.

There is no line in there that says trophies are large. No database, no rules you could go and grep for. Just numbers, and everything the model knows lives in how those numbers relate to each other. Change enough of them and you change what it believes.

That file is the actual subject of this series. What is in it, how it got that way, who is allowed to have a copy, how you squeeze it down small enough to fit on a cheap graphics card, and how it gets served to a lot of people at once without costing a fortune.

There is a five gigabyte GPU sitting under my desk, which turns out to decide what I am allowed to run .. we get to that in Act III, once there is something worth running.

Part 2 builds the smallest piece of one, and we go up from there.

## Where this is going

By the end of this you should be able to sit with an AI or data engineer, follow the whole conversation, and push back on parts of it.

**Act I, the machine.** What is inside the file. Weights, tokens, layers, attention. We build a working transformer in about 150 lines of Python and watch it run.

**Act II, the making.** How a pile of random numbers turns into something useful. Training data, fine tuning, why models have a personality, and why benchmark scores mostly lie.

**Act III, the delivery.** How it actually gets used. Running one yourself, what it costs per million words, how models look things up, how they use tools, and how they fail.

> **Say this out loud:** "It cannot be looking anything up. There are more possible sentences than there are atoms, so the only way to guess the next word that well is to have compressed the rules that produce them."

That is the sentence my twenty-years-ago self would have argued with, and it is the one that changed my mind.

> **The question that takes you further:** *if memorising is off the table, what does a model have to build internally in order to predict this well?*

### Checkpoint

1. Why can a model not get good at next word prediction just by memorizing text it has seen? Answer it in terms of how many sentences exist.
2. The model gave `purple` 0.1% instead of zero. Why would a model that never says anything unlikely actually be a worse model?
3. Somebody says a model is "mostly matrix multiplies". Roughly what are they telling you it spends its time doing?

If I have got something wrong in here, tell me. Half the reason I am publishing this is so somebody who knows better can correct me.

*Next: [Part 2 — The Perceptron →](ai-internals-02-the-perceptron.md), where we build one neuron and find out that all of this is a weighted sum wearing a hat.*
