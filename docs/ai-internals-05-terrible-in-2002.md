# Part 5 — Why It Was All Kind of Terrible in 2002

*[← Part 4](ai-internals-04-backpropagation.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md) · Next: Tokens & Embeddings (not yet published)*

You now know everything I knew in 2002. Neuron, loss, gradient descent, backprop. All of it was published, none of it was secret, and I could write the training loop from memory.

It worked terribly.

I want to tell you what that was actually like, because there is a version of this history where everyone was a visionary waiting patiently for hardware, and that is not what it was like.

It was 2002. I would set up a network, start it training on a desktop machine, and go do something else. Come back in a few hours. Sometimes the loss had come down and it had learned to classify something modest. Often it had not moved at all, and I could not tell you why. You would change the initialisation, or the learning rate, or the number of hidden units, and try again, and wait again.

The honest assessment among people doing this was that neural networks were an interesting idea that mostly did not work very well. Support vector machines were beating them on real problems, and had actual theory behind them. If you wanted a career, you did not do neural networks.

They were right about the evidence. Everyone was wrong about the conclusion. Working out the difference between those two sentences is the most useful thing in this part.

## Five reasons it did not work

Look at what we actually had.

**The data was a rounding error.** A good dataset was a few thousand hand-labelled examples that a graduate student had assembled, probably by hand. There was no ImageNet, no Common Crawl. If you wanted a hundred thousand labelled anything, you were going to spend a year making it.

**The compute was a desktop.** A single CPU. No GPUs for this, because using graphics hardware for maths was a fringe idea nobody had properly built tools for. A training run was hours or days, so you got a handful of experiments a week. When each attempt costs you a day, you cannot search a space of ideas. You can only poke at it.

**The networks were shallow.** Two hidden layers, maybe three. And it was not that we lacked ambition, it was that deeper ones genuinely trained worse, which felt like a law of nature rather than a solvable problem.

**The blame never reached the front.** This is the technical heart of it, and Part 4 set it up.

Remember that backprop passes blame backwards, layer by layer. Every time it crosses a layer, a bit of the signal is lost. That is survivable for two layers. Across four or five, almost nothing arrives.

So the layers nearest the input got told essentially nothing about what they had done wrong, and therefore never improved. **The front of the network was decoration.** Depth was not helping because the depth was not really training.

The culprit was the S-shaped bend everyone used between layers, called a **sigmoid**. It flattens out at both ends, and anything flat passes almost nothing backwards. That is worth a name because it is the standard story for why deep learning stalled, and you will hear it called **the vanishing gradient problem**.

> 🤫 **Play:** [**The Fade**](playground.html#fade) in the playground is a line of people passing a whisper back. Set it to ten layers with the old bend and watch how much of the message reaches the front: about four hundred-thousandths of one percent. Then press the 2012 bend. **The weights do not change, only the bend does**, and the whisper arrives intact. That single swap is most of what this part is about, and you can do it in one click.

**We initialised badly and we did not know it.** Starting weights were picked by rules of thumb that were, in hindsight, wrong, and that quietly made the vanishing problem worse.

Every one of those was fixable. Not one of them was a flaw in the idea.

## Which is the question worth sitting with

> **Were neural networks wrong, or was the world not ready for them?**

The evidence in 2002 said the approach was weak. The evidence was correct and the interpretation was backwards. What we were measuring was not the ceiling of the method, it was the ceiling of our data and our hardware, and we could not tell those apart because we had never once seen the method with enough of either.

This is a genuinely hard problem and it is not only a story about the past. When something underperforms, you usually cannot distinguish *this idea is bad* from *this idea is starved*. We got that call wrong for roughly twenty years, in public, with good reasons.

I think about that more than is comfortable.

## The moment it turned

**2012. ImageNet.**

ImageNet was Fei-Fei Li's project, and it was not a clever algorithm, it was 1.2 million labelled images. Someone finally built the ingredients. There was an annual competition on it, and progress was the usual grind of hand-designed feature extractors, with error rates improving a point or so a year.

Then Alex Krizhevsky, Ilya Sutskever and Geoffrey Hinton entered a deep network called **AlexNet**, built out of layers that slide a small window over the image looking for one pattern at a time, which is what convolutional means and is the only time you will need the word here. It won with a 15.3% error rate. Second place, using the established methods, got 26.2%.

That is not winning. In a mature competition, a ten point gap is the field being told it has been doing the wrong thing.

Three things made it work, and all three are the fixes to the list above.

**They trained on GPUs.** Two GTX 580 gaming cards, in a bedroom. Krizhevsky wrote the convolution code himself because no framework existed. That is the oven from Part 1a arriving, and it arrived because one person was stubborn enough to write CUDA by hand.

**They had 1.2 million images.** The ingredients.

**They swapped the bend.** Out went the sigmoid, in came something that does not flatten out: negatives become zero, everything else passes through untouched. It is called **ReLU**, it is the least impressive-looking idea in this series, and it is in essentially every model built since.

Because it does not fade, the blame stops evaporating on its way back, and the front layers finally hear about their mistakes. Suddenly deep networks train. One change to one line unlocked the depth we had been unable to use for twenty years.

None of it was a new theory of learning. It was the same backprop from 1986, given hardware, data, and a better bend.

## And then the same thing happened to language

AlexNet was pictures. Language got its own version of that moment a year later, and it is the missing rung between this part and the next one.

In 2013 a team at Google led by Tomas Mikolov published **word2vec**. The idea was almost insultingly plain: train a small network to predict a word from the words sitting around it, then throw the network away and keep the numbers it had assigned to each word along the way. Stanford's **GloVe** followed in 2014, a different route to the same place.

What came out of it was the first evidence anybody really believed that meaning could simply be a position in a space, learned from raw text with no labels and nobody defining what a single direction stood for. That is a strange thing to accept on faith, and before 2013 most people did not. Afterwards they did, and the field spent the next four years building on those numbers, well before the machinery in Part 9 existed.

So when Part 6 hands you a table of vectors and tells you that closeness carries meaning, that is not a property of the modern architecture. It is a 2013 result the modern architecture inherited, and it arrived the same way as everything else in this part. No new theory. Enough text and enough compute to show that the old idea had been working all along.

## What this tells you about the rest of the series

There is a pattern here that will repeat, and once you have it you will spot it in every part that follows.

**Algorithm plus data plus compute plus engineering equals capability.** Not one of those alone. AlexNet is the first clean demonstration, the transformer in Part 9 is the second, and the scaling laws in Part 11 are the field finally writing the pattern down as an equation.

It also means that when you read that some approach was tried and failed, the useful follow-up is not *why was the idea wrong.* It is **at what scale was it tried, and has anything changed since.**

That question is worth more than most of the answers in this series.

> **Say this out loud:** "Neural nets in 2002 were not wrong, they were starved. AlexNet in 2012 changed three things: GPUs, a million labelled images, and a different bend between layers, and that last one is what finally let the blame reach the front of a deep network."

> **The question that takes you further:** *when we say an approach failed, are we measuring the method or the resources it was given?*

### Checkpoint

1. Explain the vanishing gradient problem to somebody without using any maths.
2. AlexNet beat the field by more than ten points. Name the three changes and say which one fixed the depth problem specifically.
3. Everyone in 2002 read the evidence correctly and drew the wrong conclusion. What was the mistake exactly?
4. Word2vec came out in 2013 and attention did not arrive until 2017. What did the field believe in those four years that it had no proof of before 2013?

*Next: Part 6 — Tokens & Embeddings (not yet published), where we stop doing history and start on the machinery that was actually new.*
