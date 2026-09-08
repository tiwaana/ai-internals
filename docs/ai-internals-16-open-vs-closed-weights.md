# Part 16 — Open vs. Closed Weights

*Act IV · [Series index](ai-internals-00-index.md) · Next: [Size & Quantization →](ai-internals-17-size-and-quantization.md)*

In February 2023 Meta released a model called LLaMA. Not to the public. You filled in a form, said you were a researcher, and they sent you a download link.

About a week later somebody posted the files on BitTorrent, and then somebody opened a pull request on Meta's own GitHub repository helpfully adding the magnet link to the README. The weights were gone. There was no getting them back, in the way there is no getting a song back.

Here is the part I find interesting. Meta's response, five months later, was to release the next version deliberately and for free. They looked at what had actually been lost and decided it was not very much, and that having everyone build on their model was worth more than keeping it.

To understand why that was a reasonable call, you have to know exactly what was in those files.

## A model is two things, and only one of them is expensive

From Part 2: a weight is a knob on a weighted sum, and a model is billions of them.

So a trained model is really two separate things.

**The architecture** is the shape. How many layers, how wide, how the knobs are wired together, what order the operations run in. This is math and code. It is almost always published, described in papers, and reimplemented by other people within days.

**The weights** are the actual values of those billions of knobs. This is the part that cost millions of dollars in electricity and months of compute to find.

> The intelligence of a model *is* the specific values of those weights. Nothing else. Change the weights and you have changed its mind.

Nobody is hiding the architecture. Everybody is deciding what to do about the weights. So the whole open versus closed argument reduces to one question, and it is a question about a file.

**Who gets the numbers?**

## Closed means you rent the behaviour

With Claude, GPT or Gemini, the weights sit on the company's servers and you never see them. You send text over the internet, their machines run the model, text comes back.

You are renting the behaviour, not the model. It works well, it is usually the most capable thing available, and you cannot look inside.

With Llama, Qwen, Gemma, Mistral or DeepSeek, the company publishes the weight file. Often many gigabytes. You download it and run it on your own hardware. No internet, nobody watching what you asked, and you can take it apart.

That single difference, whether you possess the numbers, cascades into everything else.

| | Closed weight (API) | Open weight (download) |
|---|---|---|
| Where it runs | Their servers | **Your** machine |
| Your data | Sent to them | Stays local |
| Cost model | Pay per token, forever | Free to run, you pay hardware and electricity |
| Inspect internals? | **No** | **Yes**, which is the whole game for us |
| Modify it? | No | Yes. Fine-tune, quantize, surgery |
| Capability ceiling | Highest | Behind the frontier, closing fast |
| Works offline? | No | Yes |

## The trap: open weight is not open source

This is the bit that separates people who understand this from people repeating headlines, and I want to be careful with it because I got it wrong myself at first.

It is a spectrum, not a switch.

<svg viewBox="0 0 720 150" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Openness spectrum">
  <style>
    .bar{fill:none;stroke-width:8;}
    .cap{fill:var(--ink,#e6edf3);font:600 13px ui-monospace,monospace;}
    .sub{fill:var(--faint,#6b7688);font:11px ui-monospace,monospace;}
  </style>
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#f07aa6"/>
      <stop offset="0.5" stop-color="#f4b860"/>
      <stop offset="1" stop-color="#37d39b"/>
    </linearGradient>
  </defs>
  <line class="bar" x1="60" y1="40" x2="660" y2="40" stroke="url(#grad)"/>
  <circle cx="60" cy="40" r="7" fill="#f07aa6"/>
  <circle cx="360" cy="40" r="7" fill="#f4b860"/>
  <circle cx="660" cy="40" r="7" fill="#37d39b"/>
  <text class="cap" x="60"  y="70" text-anchor="middle">CLOSED</text>
  <text class="cap" x="360" y="70" text-anchor="middle">OPEN WEIGHT</text>
  <text class="cap" x="660" y="70" text-anchor="middle">OPEN SOURCE</text>
  <text class="sub" x="60"  y="90" text-anchor="middle">Claude, GPT</text>
  <text class="sub" x="360" y="90" text-anchor="middle">Llama, Qwen, Gemma</text>
  <text class="sub" x="660" y="90" text-anchor="middle">OLMo</text>
  <text class="sub" x="60"  y="120" text-anchor="middle">API only</text>
  <text class="sub" x="360" y="120" text-anchor="middle">weights, no recipe</text>
  <text class="sub" x="660" y="120" text-anchor="middle">weights + data + recipe</text>
</svg>

**Closed.** You get an API and nothing else.

**Open weight.** You get the finished weights, usually under a license with conditions attached. You do not get the training data and you do not get the recipe. You can run it and adapt it. You could not reproduce it from scratch if your life depended on it.

**Fully open source.** Weights, plus the training data, plus the training code and the recipe. In principle you could rebuild it yourself. AllenAI's OLMo aims here. It is rare, because the data and the recipe are the actual crown jewels.

Watch the license too. Open weight does not mean do whatever you like. Llama's license has conditions at large commercial scale, while Qwen and Mistral often ship under Apache 2.0, which is genuinely permissive. Quite often **"weights available"** is the honest phrase and "open" is the marketing one.

## The kitchen

This is the analogy that made it stick for me, and we are going to keep using this kitchen for the rest of the series.

**Closed weight is a restaurant.** The food is excellent. You order through a window, you never go into the kitchen, and you pay again every time you visit.

**Open weight is them handing you the finished dish and the keys to a home kitchen.** You can reheat it, re-plate it, take it apart, add to it, work out what is in it by tasting. What you do not get is the recipe or the farm the ingredients came from.

**Open source is the recipe, the ingredient list, and the address of the farm.**

If you want to learn to cook, you need to be standing in a kitchen with real food in front of you. That is open weight, and it is why everything hands-on in this series uses models you can download.

## What this means for us

You cannot learn internals from a closed model. Point blank. An API is a locked box and you only ever see what went in and what came out.

Every question worth asking needs the file.

- What is layer 14 actually representing?
- What happens if I squash this from 16 bits per weight down to 4?
- Show me the full probability distribution over the next token, not just the word it picked.
- What breaks if I edit these particular weights?

None of those are answerable through a window. And here is the good news, which surprised me: **size is a constraint on your hardware, not on your learning.** A 3 billion parameter model has the same parts as a 400 billion parameter one. Same architecture, same attention, same everything, just fewer and smaller. You can learn the entire mechanism on a model that fits on a laptop.

Which is fortunate, given what is under my desk.

> **Say this out loud:** "Open weight and open source are not the same thing. You get the cake, not the recipe, and usually with a license attached."

> **The question that takes you further:** *if the weights are public but the training data is not, what can you still not find out about a model?*

### Checkpoint

1. Why can you not study a model's internals through a closed API?
2. Which is the expensive secret, the architecture or the weights? Why is the other one given away freely?
3. What do you get with fully open source that you do not get with open weight?
4. Meta lost control of the LLaMA weights and then chose to give the next version away. What does that tell you about where they thought the value actually was?

If I have got something wrong in here, tell me.

*Next: [Part 17 — Size & Quantization →](ai-internals-17-size-and-quantization.md), where "7B" turns into gigabytes and we work out what fits on a small card.*
