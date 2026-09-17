# Glossary

*[Series index](ai-internals-00-index.md) · Every word this series has defined, in one place*

This page exists because you will meet these words out of order. Somebody says "the KV cache is eating my VRAM" in a meeting three weeks after you read Part 9, and you want one line that puts it back, not a re-read.

Two things worth knowing before you use it.

**Some of these you need and some you can forget.** The series sorts every technical word into one of two piles. If an AI or data engineer will actually say it out loud, it is worth owning, and it is listed here plainly. If it is only how something works under the hood, the idea matters and the name does not, and I have marked those *(mechanism)*. You are allowed to forget every one of them and still hold the conversation.

**Everything here is defined somewhere in the series**, and each entry says where. Nothing has been added that a part has not already built up to, so if a word you heard is missing, it is because we have not got there yet. The list grows as Acts III and IV land.

---

---

## A

**Activation** · *Part 2*. The bend applied to a neuron's output. Rosenblatt used a hard threshold, over the bar or not. Everything modern uses something with a slope, for the reason under **vanishing gradient**.

**Autoregressive** · *Part 4*. Generating one token at a time, sticking each one on the end and running the whole model again on the slightly longer text. It is why output arrives the way it does, and why nothing is planned further ahead than the next word.

## B

**Backpropagation** · *Part 4*. Working out how much every weight contributed to the error by pushing the blame backwards from the answer, one layer at a time. One backward pass gets you the answer for every weight and costs about what one forward pass costs. Without it, training anything large would be arithmetically impossible.

**Bias** · *Part 2*. One extra number added at the end of a neuron's sum that is not attached to any input. How picky it is in general. Its baseline mood.

## C

**Chain rule** *(mechanism)* · *Part 4*. The piece of calculus that makes backpropagation work. Old, dull, and the most valuable thing in the series. Nobody will say it to you; they will say backprop.

**Cross-entropy** · *Part 3*. The usual way to put a number on how wrong a prediction was. It asks how surprised the model should have been by the right answer, and it punishes confident wrongness far harder than uncertain wrongness. It scores a whole spread of possibilities rather than one guess, which is why it is the one used for prediction.

## D

**Dot product** · *Part 2*. See **weighted sum**. Same operation, more intimidating name. Both get said constantly.

## F

**Forward pass** · *Part 4*. Running the model to get a prediction. The other direction is the backward pass, which works out the blame.

**Function** · *Part 1b*. A thing you put something into and get something out of. A vending machine. A recipe. A model is one of these, enormous, with smaller ones inside it all the way down.

## G

**Gradient** · *Part 3*. For one weight: which way, and how steeply. Nudge it a little and does the loss get better or worse, by how much. Every weight gets its own answer, and learning is stepping each one in the direction its answer said was better.

**Gradient descent** · *Part 3*. The whole training loop in four words: roll downhill, repeatedly. Standing somewhere random on a landscape of every possible setting of the weights, and walking towards a valley.

## L

**Learning rate** · *Part 3*. How big a step to take downhill. The knob that will waste more of your time than any other. Too small and you creep; too large and you overshoot, bounce harder each time, and the loss becomes `NaN`.

**Local minimum** · *Part 3*. A dip you can roll into and get stuck in because the ground rises in every direction. The field was frightened of these for years. With a billion directions the odds that not one of them slopes down are effectively nil, so it turned out to be mostly an artifact of drawing the picture in two dimensions.

**Loss** · *Part 3*. A single number that is large when the model is wrong and zero when it is perfect. That is the whole specification, and which loss you choose decides what the machine actually aims at.

## P

**Perceptron** · *Part 2*. One neuron, 1958. Score each input, multiply by how much it matters, add it up, and if the total clears a bar, act. The smallest piece of everything that follows.

## R

**ReLU** · *Part 5*. The bend that does not flatten out: negatives become zero, everything else passes through. The least impressive-looking idea in the series and it is in essentially every model built since 2012, because it stops the blame evaporating on its way back and finally let deep networks train.

## S

**Sigmoid** · *Part 5*. The S-shaped bend that squashes anything into 0 to 1, and the same curve fuzzy logic calls a membership function. It flattens at both ends, and anything flat passes almost nothing backwards, which is what stalled deep learning for twenty years. People still say *"the sigmoid saturates."*

**Softmax** · *Part 1b*. Turns a list of scores into percentages that add up to 100. It is how raw scores become "41% big, 27% small", and how attention distributes exactly all of a token's attention across the sentence.

## T

**Temperature** · *Part 1b*. How much randomness to allow when picking the next word. Turn it down and the model takes the safe option every time; turn it up far enough and it will eventually say `purple`.

## V

**Vanishing gradient** · *Part 5*. Every time the blame crosses a layer, a little of the signal is lost. Across four or five layers almost nothing arrives, so the layers nearest the input never learn and the front of the network is decoration. The standard story for why deep learning stalled, and ReLU is most of the fix.

## W

**Weight** · *Part 1b*. A knob. It says how much one thing matters. All the knobs together are the model's knowledge, and they are the only part that is ever learned. Everything else is fixed plumbing.

**Weighted sum** · *Part 2*. Multiply each input by its own knob and add up the results. The single most common thing anyone in this field will say to you, and it means exactly that and nothing more. Also called a **dot product**. When somebody says a model is "mostly matrix multiplies", they mean it is doing enormous numbers of these at once.

**Word2vec** · *Part 5*. 2013, Google. Train a small network to predict a word from the words around it, throw the network away, keep the numbers. The first evidence anybody really believed that meaning could just be a position in a space, learned from raw text with nobody defining what a direction stood for.

---

*Missing a word, or think one of these is wrong? That is the point. Tell me.*

*[← Back to the series index](ai-internals-00-index.md)*
