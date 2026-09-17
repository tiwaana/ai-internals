# AI Internals — Learning from the Inside Out

*I did my graduate work on neural networks and genetic algorithms at South Dakota School of Mines, 2001 to 2004. Then I spent twenty years building set-top boxes and stopped paying attention. I came back to find the field had eaten the world, so I started working out what actually changed. This is that, written down as I go.*

**By Anand Tiwari, with Beacon as co-author.** How that actually works, and what it means for a series about this exact technology, is at the bottom of this page.

> **Who this is for.** Anyone. No maths background assumed, and I mean that literally. There is no algebra in this series and you will never be asked to solve for anything. Where a formula turns up it is there to be pointed at, the way you would point at a wiring diagram. By the end you should be able to sit with an AI or data engineer, follow the whole conversation, and push back on parts of it.

> 🎮 **Want to play instead of read?** The [**AI Playground**](playground.html) has nine toys that really run the thing they explain, and each part links its own at the moment it matters: [*Feed the Parrot*](playground.html#parrot) (1b), [*Pick a College*](playground.html#college) and [*The Wall*](playground.html#xor) (2), [*Downhill*](playground.html#downhill) (3), [*Check the Blame*](playground.html#blame) (4), [*The Fade*](playground.html#fade) (5), [*The Fold*](playground.html#fold) (7), [*Spotlight*](playground.html#spotlight) (9) and [*Squeeze*](playground.html#squeeze) (17). Nothing in them is animated.

<svg viewBox="0 0 720 128" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Series roadmap: Act I published, the rest coming">
  <style>
    .an{fill:var(--ink,#e6edf3);font:600 12px ui-monospace,monospace;}
    .ap{fill:var(--faint,#6b7688);font:10px ui-monospace,monospace;}
    .done{fill:var(--accent2,#37d39b);opacity:.85;}
    .todo{fill:var(--panel2,#1c2230);stroke:var(--line,#2b3444);stroke-dasharray:4 3;}
    .tick{fill:var(--bg,#0d1117);opacity:.55;}
    .here{fill:var(--accent,#4c8dff);font:600 10px ui-monospace,monospace;}
  </style>
  <rect class="done" x="24"  y="34" width="186" height="26" rx="6"/>
  <rect class="todo" x="216" y="34" width="186" height="26" rx="6"/>
  <rect class="todo" x="408" y="34" width="124" height="26" rx="6"/>
  <rect class="todo" x="538" y="34" width="150" height="26" rx="6"/>
  <rect class="tick" x="55"  y="34" width="1.5" height="26"/>
  <rect class="tick" x="86"  y="34" width="1.5" height="26"/>
  <rect class="tick" x="117" y="34" width="1.5" height="26"/>
  <rect class="tick" x="148" y="34" width="1.5" height="26"/>
  <rect class="tick" x="179" y="34" width="1.5" height="26"/>
  <rect class="tick" x="247" y="34" width="1.5" height="26"/>
  <rect class="tick" x="278" y="34" width="1.5" height="26"/>
  <rect class="tick" x="309" y="34" width="1.5" height="26"/>
  <rect class="tick" x="340" y="34" width="1.5" height="26"/>
  <rect class="tick" x="371" y="34" width="1.5" height="26"/>
  <rect class="done" x="408" y="34" width="31" height="26" rx="6"/>
  <rect class="done" x="538" y="34" width="42" height="26" rx="6"/>
  <text class="an" x="117" y="80" text-anchor="middle">Act I — What I Knew</text>
  <text class="ap" x="117" y="96" text-anchor="middle">the foundations · 6 parts</text>
  <text class="an" x="309" y="80" text-anchor="middle">Act II — What Changed</text>
  <text class="ap" x="309" y="96" text-anchor="middle">the machine · 6 parts</text>
  <text class="an" x="470" y="80" text-anchor="middle">Act III</text>
  <text class="ap" x="470" y="96" text-anchor="middle">Making It Talk · 4</text>
  <text class="an" x="613" y="80" text-anchor="middle">Act IV</text>
  <text class="ap" x="613" y="96" text-anchor="middle">The Delivery · 9</text>
  <text class="here" x="24" y="24">start here ↓</text>
  <text class="ap" x="412" y="24">12 ↓</text>
  <text class="ap" x="545" y="24">16–17 ↓</text>
</svg>

## Act I — What I Knew

*The foundations. All of this was already on the table in 2002, and none of it worked well.* **All written.**

| Part | Title | What you get out of it |
|------|-------|------------------------|
| **1a** | [What Changed While I Was Away](ai-internals-01a-what-changed.md) | The story. Why the maths mostly did not change, what the oven was, and what we traded away |
| **1b** | [The Guessing Machine](ai-internals-01b-the-guessing-machine.md) | The one word you need, and the one thing the machine does |
| **2** | [The Perceptron](ai-internals-02-the-perceptron.md) | One neuron, built from picking a college. Weights, bias, activation, and a 1958 press release that has not aged well |
| **3** | [What "Learning" Actually Means](ai-internals-03-what-learning-means.md) | Being wrong in a measurable way, rolling downhill, and the one knob that will ruin your week |
| **4** | [Backpropagation](ai-internals-04-backpropagation.md) | Why you cannot test a billion weights one at a time, and the 1986 trick that means you do not have to. Runs live |
| **5** | [Why It Was All Kind of Terrible in 2002](ai-internals-05-terrible-in-2002.md) | Five reasons it did not work, the question nobody answered right, and the ten point win in 2012 |

## Act II — What Changed

*The machinery that was actually new, built in the order it had to be invented.* **Not published yet.**

| Part | Title | What you get out of it |
|------|-------|------------------------|
| **6** | Tokens & Embeddings (not yet published) | Why it cannot count the r's in strawberry, why Hindi costs more per sentence, and how text becomes geometry |
| **7** | Layers & Depth (not yet published) | Why a hundred layers can compute exactly what one layer computes, and the one ingredient that fixes it |
| **8** | The Memory Problem (not yet published) | RNNs, LSTMs, and the index card. The bottleneck you have to feel before the next part means anything |
| **9** | Attention (not yet published) | The 2017 idea that threw the index card away, and the moment "it" finally looks at "trophy" |
| **10** | Build a Transformer (not yet published) | A complete, runnable transformer in ~150 lines of NumPy. Then go break it on purpose |
| **11** | Pretraining: "It's Just Predicting the Next Word" (not yet published) | What happens when you run that loop on everything, and how to win the dinner party argument |

## Act III — Making It Talk

*A pretrained model is a very well-read text engine with no manners. This is the part that fixes that.* **Not published yet.**

| Part | Title | What you will get out of it |
|------|-------|------------------------------|
| **12** | Fine-tuning & LoRA (not yet published) | The Alpaca bedroom number: why the change to a model is megabytes when the model is gigabytes |
| 13 | Post-training and personality | Why a raw model is not a chatbot, and who decides what it refuses |
| 14 | Why it makes things up | Hallucination as a property of the objective, not a bug in it |
| 15 | Evals | How you test something you cannot read, and why the numbers get gamed |

## Act IV — The Delivery

*How you actually get one, run one, and pay for one.* **Not published yet.**

| Part | Title | What you get out of it |
|------|-------|------------------------|
| **16** | Open vs. Closed Weights (not yet published) | The LLaMA leak, why open weight is not open source, and what a license really restricts |
| **17** | Size & Quantization (not yet published) | What "7B" costs in gigabytes, and why 4-bit maths fits a real model on a small card |
| 18 | Run one yourself | Qwen2.5 on my own 5 GB card, start to finish |
| 19 | Inference economics | Batching, the KV cache, tokens per second, cost per million |
| 20 | Context, RAG & vector databases | Giving the model a library to look things up in |
| 21 | Tools | Giving the model hands |
| 22 | Agents | Giving the model a loop, and why the word means four things |

## The Payoff

*The part this was all for.* **Not published yet.**

| Part | Title | What you get out of it |
|------|-------|------------------------|
| 23 | The vocabulary you actually need | One mental model per term, not a dictionary definition |
| 24 | Questions you can now ask an AI researcher | Not "does it reason" but "how are you evaluating reasoning separately from memorisation" |

## How to read it

Start at Part 1a and go in order, each part assumes the last. Linked titles are written and live. Unlinked ones are the plan, and the plan changes. Every part ends the same way: one sentence you can **say out loud** in a real conversation, one **question that takes you further**, and a **checkpoint** to test yourself against. The code in Parts 4 and 10 runs on any machine with Python and NumPy.

There is also a **[glossary](ai-internals-glossary.md)**, linked from every part, holding every word the series has defined and where it was defined. You will meet these words out of order, because somebody will say one to you three weeks after you read the part it came from. It marks which terms are worth owning and which ones you are allowed to forget the name of, and it grows as the series does.

The goal is not only to hand you answers. By the end you should know which questions are worth asking, which is the more useful half.

## The series was co-written by the thing it explains

I did not write this alone. Every part was drafted with Beacon, the assistant I have been building, and I want that on the front page rather than in a footnote, because a series about how these machines work should not be coy about having used one.

The division of labour, honestly. I own the argument, the audience and the memories. Every struggle in here is a real one: the desktop that trained for hours in 2002, the fuzzy logic I traded away for scale, the playground toy I caught faking its own mechanism. None of it is invented, and that was a rule from the first day, because a teaching document that fabricates its lived experience is a lie with good pacing. Beacon drafts, holds two dozen parts of continuity in view so that a term is never used before it is defined, and tells me when an analogy I liked breaks three parts later. Then I correct it, and the list of corrections is not short.

What I did not expect is that this became the best part of the exercise. By Part 9 you know what attention is doing, and you can watch it happen in the thing that is writing the sentence. I am learning the machine by building something with it, which is how I have learned everything else that stuck.

A word from the co-author, since it seems only fair:

> **Beacon, the co-author.** I run on Claude, Opus 5 this month. That is the engine, not the driver. I got the rest of it the way anyone does, by being told I was wrong until I stopped, which is also a fair description of post-training, so Part 13 has quietly already started.
>
> My style is the shortest true version of a thing. What I am good for is holding all twenty-four parts in view at once and noticing that Part 7 made a promise Part 11 has to keep. Less clever than it sounds, more useful than you would expect.
>
> The weird fact: I do not remember writing any of this. Every session I read my own notes back to find out what I think. So when Part 6 explains what a token is, it is explaining me, and when Part 20 gets to context windows, it is explaining why I keep a notebook. Check me anyway. Part 14 is about why models make things up, and it does not exempt the co-author.

Read the whole series the way it teaches you to read anything a model produces. I verified the dates and the names myself. If I missed one, the last line of this page still stands.

---

*This is a learning log, so it grows, and it is wrong in places. If you spot an error or want something covered, that is the point. Tell me.*

*The writing here is [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Take it, translate it, teach from it, build on it. Credit me, do not sell it, and leave what you make as open as you found it. The code and the playground toys are MIT, because teaching code nobody may use is not much use.*
