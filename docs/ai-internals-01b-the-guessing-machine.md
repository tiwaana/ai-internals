# Part 1b — The Guessing Machine

*[← Part 1a](ai-internals-01a-what-changed.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md) · Next: [The Perceptron →](ai-internals-02-the-perceptron.md)*

That was the story. Now, let us get ready.

Two things happen next. First, you learn the one idea you need, and it is easier than you might think. Then, you see how the machine works, and that is also easier than you expect.

Once we are done here, you will be ready to move on with me.

## The one word you need

There is one word that does most of the work in this series, and it is **function**.

A function works like a magic box. You put something in and get something out. Imagine a vending machine: you put in a coin, press B4, and get a bag of chips. If you do the same thing the next day, you get the same chips. The key idea is that with functions, the same input always gives the same output, because the rule inside does not change.

The next thing to know is that you do not need to see inside a function to use it. Most people have never opened a vending machine, and they do not need to. All that matters is knowing what you put in and what you get out.

Another important point is that functions can work together in a sequence. A recipe is like a function too: you put in ingredients and get dinner out, but there are smaller steps along the way. Chopping turns an onion into pieces. The pan cooks those pieces and gives you something browned. The result of one step becomes the input for the next. Nobody finds that complicated, it is just cooking.

That is the whole idea, and you already understand it.

A model is just a big function. You give it text, and it gives back a guess at the next word. Inside, it is a chain of smaller functions, each one feeding the next, and inside those are even simpler ones. At the very bottom is something so basic it might surprise you. We build that simple part in Part 2.

You will come across three terms later. I am introducing them now so they do not seem intimidating, and none of them mean exactly what they sound like.

- A **weight** is like a knob that controls how much something matters. All these knobs together make up the model's knowledge, and they are the only part that ever gets learned.
- A **weighted sum**, also known as a **dot product**, means multiplying some things by their knobs and adding up the results. The names sound complicated, but it is simple arithmetic you could do by hand. This idea comes up constantly in this field, so it is worth remembering. We build it properly in Part 2.
- **Softmax** takes a list of scores and turns them into percentages that add up to 100. You will see one work in the next section.

That is the toolkit. There is no algebra in this series, and the odd formula that shows up is there to be read, not solved.

## The entire system has one job, it guesses the next word

This was the most surprising thing to me when I came back, because it seems almost too simple to believe.

You give the model some text, and it gives you a probability for each possible next word. It chooses one, adds it to the end, and then repeats the process on the new, longer text. That loop is the whole thing. Whole essays are built one word at a time by something that never looks further ahead than the next word.

Give it *"The trophy didn't fit in the case because it was too"* and you get results like this.

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

Notice that `purple`, at the bottom, still gets a small chance. Nothing gets a probability of zero. The function itself gives the same list every time you feed it the same words, just like the vending machine. The randomness comes afterwards, when one word gets picked from that list. Turn the randomness up enough and the model will eventually choose purple. The randomness setting is called **temperature**. Lower it, and the model always picks the safest word. Raise it, and the model starts choosing less likely options.

At first I thought, okay, so it is just autocomplete. My phone does the same thing above the keyboard.

## So, is it really just autocomplete?

Keep that question in mind, because taking it apart is the most useful part of this whole piece.

I used to imagine it as a big lookup table. The model would read tons of text, remember which words usually follow which, and repeat them back. Like a parrot with a great memory. That is basically what a language model was, back in my day.

You could build that parrot yourself right now. It takes about ten seconds.

> 🦜 **Play:** [**Feed the Parrot**](playground.html#parrot) in the playground. Type in some text, hit train, and it builds exactly that table, showing which word comes next for every pair of words. Then let it write using your own text, which works surprisingly well. But ask it for something a bit different and you will see it fall apart quickly.

The parrot does not fail because it needs more text. It fails on arithmetic.

Imagine a sentence of twenty words, drawn from a vocabulary of fifty thousand words. The number of possible twenty word sentences is 50,000 to the twentieth power, a number with about 94 digits. For comparison, there are only about 80 digits worth of atoms in the observable universe. So a long sentence you read today has very likely never been written down before, by anyone.

Let me be clear. There is nothing to look up. A machine trying to guess the next word across all of human writing cannot just remember everything, because there is not enough room in the universe for that. Its only choice is to compress. It has to figure out the rules behind all those sentences and remember the rules instead.

And the rules of human language cover almost everything we know. The model has to learn grammar, since bad grammar leads to bad guesses. It needs to learn facts, because "the capital of France is" has only one correct answer and every mistake counts against it. It also has to learn arithmetic, since sums show up in text and come out a particular way. It needs to know that trophies are big and cases are things you put objects into. It even has to understand that if someone is angry in the first paragraph, they are probably still angry in the third, because that affects which word comes next.

No one sat down and taught the model any of this. It picked all of it up because each of those things made its next guess a little better, and training keeps whatever makes the guess better.

I still call it autocomplete. I just do not think that is such a small thing anymore.

## What else? The machine is just a file

This one caught me off guard too, and I think my younger self would have found it the strangest of all.

This machine, the one that knows trophies are big, is really just a file. You can copy it onto a drive. It is mostly one huge list of decimal numbers, billions of them.

You will not find a line in the file that says trophies are large. There is no database and no set of rules to search. It is just numbers, and everything the model knows comes from how those numbers relate to each other. Change enough of them and you change what the model believes.

That file is the main subject of this series. We will look at what is inside it, how it was made, who can get a copy, how to make it small enough for an affordable graphics card, and how to serve it to a lot of people without spending a fortune.

That last part is not abstract for me. The graphics card under my desk has five gigabytes of memory, and a model has to fit in it to run at any decent speed, so the size of that file decides which models I can run at home .. we get to that in Act IV.

In Part 2 we start by building the smallest piece of a model, and then add to it step by step.

If you want to see the whole route before we set off, the map of the series is on the [series index](ai-internals-00-index.md).

> **Say this out loud:** "It cannot be looking anything up. There are more possible sentences than there are atoms, so the only way to guess the next word that well is to have compressed the rules that produce them."

> **The question that takes you further:** *if memorizing is not an option, what does a model need to build inside itself to predict this well?*

### Checkpoint

1. Why can a model not get good at next word prediction just by memorizing text it has seen? Answer it in terms of how many sentences exist.
2. The model gave `purple` 0.1% instead of zero. Why would a model that never says anything unlikely actually be a worse model?
3. A model is "just a function". What goes in, what comes out, and what does it do with the output before it runs again?

If I have got something wrong in here, tell me.

*Next: [Part 2 — The Perceptron →](ai-internals-02-the-perceptron.md), where we build one neuron and find out that all of this is a weighted sum wearing a hat.*
