# Part 1a — What Changed While I Was Away

*[Series index](ai-internals-00-index.md) · Next: [Part 1b — The Guessing Machine →](ai-internals-01b-the-guessing-machine.md)*

Read this sentence.

> **The trophy didn't fit in the case because it was too *big*.**

What is "it"? The trophy. You knew that before you finished the line and you did not work for it.

Now change one word.

> **The trophy didn't fit in the case because it was too *small*.**

Now "it" is the case. You flipped instantly, I did too, and neither of us can say how. There is no rule. Nobody taught me a rule for that. I know what a trophy is and I know what a case is for, and that was enough.

Machines could not do this. Then they could. That sentence is going to follow us through the whole series, and by the end you will be able to point at the exact piece of machinery that resolves it.

## I have done this before, which is the strange part

I did my graduate work at South Dakota School of Mines, 2001 to 2004. Genetic algorithms, neural networks, fuzzy logic.

So none of this is new to me in the way people assume. I have written the training loop. I have watched a network converge and watched one refuse to. Back then a neural network was a few thousand weights, you trained it on a desktop machine, you waited, and if you were lucky it learned to classify something modest. Genetic algorithms were the other half of my world: you breed a population of candidate solutions, keep the ones that score well, mutate them, run it again. Both were considered interesting and slightly fringe. Neither was going to write you an essay.

Then I went and spent twenty years building set-top boxes, and I stopped paying attention.

The first half of that was deep in the Linux kernel. Hard drive failure detection, boot times, the kind of work where you spend your day arguing with hardware. The second half I moved into product, which meant I largely stopped writing the code and became the bridge instead, distilling engineering trade-offs into a story that got executives, marketing and finance people lined up behind one version of the thing. They were going to fund it or kill it, and which one depended on whether I could explain it.

That turned out to be the most useful skill I have. I am good at taking something genuinely technical, finding the one simple thing it is shaped like, and handing that over to somebody without the background. Most of the work is in finding the right analogy. And you have to actually find the right one, because a bad analogy does not just fail quietly. It leaves the person more confused than when you started, and confident about the wrong thing, which is worse.

So that is what this series is. I am taking the one skill I am best at and pointing it at the thing I most want to understand.

And I came back to it because while I was away, the field ate the world. What I left as a fringe research topic is now in everybody's pocket, and I did not want to just get good at using it. I wanted the internals.

Here is what I want to say clearly, because it took me a while to be sure of it and it is the honest headline of this whole series:

> **The neural network was always there. We did not invent a new kind of math. We discovered something substantial about what happens when you make the old kind very, very large.**

Backpropagation, the algorithm that actually trains these things, was published in 1986. The perceptron is from the 1950s. The core of what a modern model does at each layer, multiply by weights, add, squash, is the same thing I was writing by hand in a lab in Rapid City.

## The recipe was fine. We did not have an oven.

That is the analogy I keep coming back to.

We had the recipe written down by the late eighties. What we did not have was an oven hot enough to cook it, anything like enough ingredients, or the one change to the recipe that made cooking it at that size worth doing. Three things showed up, roughly in this order.

**The oven.** GPUs. Graphics cards were built to do millions of small multiplications at once for video games, which happens to be exactly, precisely what training a neural network is. Nobody designed them for this. We noticed.

**The ingredients.** The internet. Not a curated dataset of ten thousand labelled examples, which is what I had. Effectively all the text anyone has ever put online.

**One new idea in the recipe.** In 2017 a paper called *Attention Is All You Need* introduced the transformer. That one is genuinely new, and it gets a whole part to itself.

And then the substantial part, the thing I did not see coming and I do not think many people did. When you cook that recipe at that heat with those ingredients, it does not just come out bigger. **It comes out different.** You get abilities nobody put in and nobody asked for. That is the actual discovery, and everything in this series is downstream of it.

## What we gave up

There is a shadow side to that, and it comes from the third thing I studied.

Fuzzy logic, Zadeh, 1965. The idea was to throw out binary truth. "Tall" is not true or false, it is 0.7 tall. You write membership functions and rules: IF the temperature is warm AND the humidity is high THEN run the fan fast. In the nineties this ran subway brakes and camera autofocus and a great many Japanese washing machines.

That idea won completely. There is nothing inside a modern model that is ever 0 or 1. Everything is a degree. In the next part you will see a model's guesses drawn as a bar chart, and the silliest word on it, `purple`, still does not get zero.

But fuzzy logic had a property these models do not. **A human wrote the rules, and you could read them afterwards and argue with them.** That was the entire point. Encode expert intuition in graded form, then go inspect it.

Nobody writes the rules in a neural network. They are discovered from data, and there is no rule in there to read. We traded away the ability to inspect the thing for the ability to make it enormous, and enormous turned out to be worth a great deal more than anyone expected.

People did try to keep both. Neuro-fuzzy systems, ANFIS around 1993, learned the membership functions from data while keeping them legible. It was a serious line of research in my era and it lost.

That bill has not gone away, it just gets paid later. It is most of why Act III has a whole part about evaluation: we cannot read the model, so we are reduced to poking it from the outside and writing down how it behaves.

> **Say this out loud:** "The math mostly did not change. We got GPUs, we got the whole internet as training data, and we got the transformer in 2017, and it turned out that guessing the next word at that scale produces abilities nobody put in on purpose."

> **The question that takes you further:** *if the algorithm was already there in 1986, what else is sitting in an old paper right now, waiting for hardware that does not exist yet?*

### Checkpoint

1. Backprop is from 1986 and the perceptron is from the 1950s. So what actually changed to get us here? Name three things.
2. In the recipe analogy, what is the oven and what are the ingredients?
3. Fuzzy logic let a human write the rules and read them back. What did we trade that away for, and where does the bill come due?

*Next: [Part 1b — The Guessing Machine →](ai-internals-01b-the-guessing-machine.md), which is the prep work. The small pile of maths you actually need, and the one thing the machine does.*
