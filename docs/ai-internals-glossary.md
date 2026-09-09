# Glossary

*[Series index](ai-internals-00-index.md) · Every word this series has defined, in one place*

This page exists because you will meet these words out of order. Somebody says "the KV cache is eating my VRAM" in a meeting three weeks after you read Part 9, and you want one line that puts it back, not a re-read.

Two things worth knowing before you use it.

**Some of these you need and some you can forget.** The series sorts every technical word into one of two piles. If an AI or data engineer will actually say it out loud, it is worth owning, and it is listed here plainly. If it is only how something works under the hood, the idea matters and the name does not, and I have marked those *(mechanism)*. You are allowed to forget every one of them and still hold the conversation.

**Everything here is defined somewhere in the series**, and each entry says where. Nothing has been added that a part has not already built up to, so if a word you heard is missing, it is because we have not got there yet. The list grows as Acts III and IV land.

---

## Numbers and initials

**7B, 3B, 70B** · *Part 17*. How many weights the model has, in billions. It is the number everyone quotes and it is only half the story, because it says nothing about how precisely each weight was written down. Ask the second question: at what precision?

**FP32, FP16, BF16, INT8, INT4** · *Part 17*. How many bits are spent storing each weight. FP32 is 32 bits, or 4 bytes, and is the training default. FP16 is the standard for serving. INT8 and INT4 are quantized, meaning squeezed. Multiply billions of parameters by bytes per weight and you have the memory it needs: 7B at FP16 is 14 GB, at INT4 it is 3.5 GB.

**GGUF, Q4_K_M** · *Part 17*. GGUF is the file format llama.cpp and Ollama use for a quantized model. `Q4_K_M` describes how it was squeezed: 4 bits per weight, `K` a smarter blocking method, `M` medium size. It is what most people reach for and it is usually right.

---

## A

**Activation** · *Part 2*. The bend applied to a neuron's output. Rosenblatt used a hard threshold, over the bar or not. Everything modern uses something with a slope, for the reason under **vanishing gradient**.

**Attention** · *Part 9*. Every token asking every other token how relevant it is, then taking a weighted average of what they know. It is the thing that lets "it" find "trophy", and it is what makes a transformer a transformer.

**Autoregressive** · *Part 4*. Generating one token at a time, sticking each one on the end and running the whole model again on the slightly longer text. It is why output arrives the way it does, and why nothing is planned further ahead than the next word.

## B

**Backpropagation** · *Part 4*. Working out how much every weight contributed to the error by pushing the blame backwards from the answer, one layer at a time. One backward pass gets you the answer for every weight and costs about what one forward pass costs. Without it, training anything large would be arithmetically impossible.

**Base model** · *Part 11*. A model that has only been pretrained. Very well read, no manners, no idea it is in a conversation. Turning one into something you can talk to happens afterwards, in Act III.

**Bias** · *Part 2*. One extra number added at the end of a neuron's sum that is not attached to any input. How picky it is in general. Its baseline mood.

**BPE, byte pair encoding** · *Part 6*. How the tokenizer's vocabulary gets built. Start with every character, repeatedly merge whichever pair occurs together most often, stop when you have as many tokens as you wanted. Frequent things become single units, rare things stay in pieces.

## C

**Causal mask** · *Part 10*. The rule that a token may not look at tokens that come after it. It is why the attention grid is triangular and why generation runs left to right. You can see it as the empty upper half of a printed array.

**Chain rule** *(mechanism)* · *Part 4*. The piece of calculus that makes backpropagation work. Old, dull, and the most valuable thing in the series. Nobody will say it to you; they will say backprop.

**Context window** · *Parts 6 and 17*. How much text the model can hold at once, counted in tokens. It costs memory while it runs, for the reason under **KV cache**.

**Cosine similarity** · *Part 6*. Asking whether two vectors point the same way and ignoring how long they are. It is the usual way to measure whether two pieces of meaning are close.

**Cross-entropy** · *Part 3*. The usual way to put a number on how wrong a prediction was. It asks how surprised the model should have been by the right answer, and it punishes confident wrongness far harder than uncertain wrongness. It scores a whole spread of possibilities rather than one guess, which is why it is the one used for prediction.

## D

**Dot product** · *Part 2*. See **weighted sum**. Same operation, more intimidating name. Both get said constantly.

## E

**Embedding** · *Part 6*. The list of numbers a token gets turned into, so the maths has something to work with. A token ID is just a name and there is nothing to multiply; an embedding is a position in a space with hundreds or thousands of directions, and closeness in that space carries meaning.

**Embedding matrix** · *Part 6*. The big lookup table holding one embedding per token in the vocabulary. The point where text becomes geometry.

## F

**Floating point** · *Part 17*. How a computer stores a decimal. Think of it as how many digits you are allowed to write down. More bits, more digits, more room taken.

**Forward pass** · *Part 4*. Running the model to get a prediction. The other direction is the backward pass, which works out the blame.

**Function** · *Part 1b*. A thing you put something into and get something out of. A vending machine. A recipe. A model is one of these, enormous, with smaller ones inside it all the way down.

## G

**Gates** *(mechanism)* · *Part 8*. The forget, input and output gates inside an LSTM, deciding what to drop, what to write down and what to expose. They matter historically. Nobody builds with them now.

**Gradient** · *Part 3*. For one weight: which way, and how steeply. Nudge it a little and does the loss get better or worse, by how much. Every weight gets its own answer, and learning is stepping each one in the direction its answer said was better.

**Gradient descent** · *Part 3*. The whole training loop in four words: roll downhill, repeatedly. Standing somewhere random on a landscape of every possible setting of the weights, and walking towards a valley.

## H

**Head** · *Part 9*. One run of attention, with its own three sets of knobs. Models do several side by side, so one head can track grammar while another tracks which noun a pronoun points at. Their answers get stapled together.

**Hidden dimension** · *Part 6*. How long each token's vector is. 512 in a small model, 4096 in a large one. Written `d` when it turns up in a formula.

**Hidden state** · *Part 8*. The single fixed-size vector an RNN carried everything in, rewritten at every word. The index card. Its size was the ceiling on everything before 2017.

## K

**Key** · *Part 9*. What a token advertises about itself, so other tokens can find it. The badge. Deliberately a different thing from what it hands over, which is its **value**.

**KV cache** · *Parts 9 and 17*. The notes the model keeps in the margin about every token it has already read, so it does not have to work them out again for the next word. It sits in GPU memory next to the weights and it grows with your context. Doubling the text quadruples the attention grid, which is the honest reason long context costs what it does. Not a billing decision, a square.

## L

**Layer** · *Part 7*. A function taking a list of numbers in and putting the same number of numbers out. Inside, it is Part 2 done many times over. Real transformer layers hold two halves, attention and an MLP, and models are advertised by how many they stack.

**Layernorm** *(mechanism)* · *Part 10*. Rescaling a vector so its numbers stay in a sensible range, before each half of every layer. Without it the numbers drift a little every pass and thirty-two passes later the whole thing is enormous or zero. The sound engineer levelling every track.

**Learning rate** · *Part 3*. How big a step to take downhill. The knob that will waste more of your time than any other. Too small and you creep; too large and you overshoot, bounce harder each time, and the loss becomes `NaN`.

**Local minimum** · *Part 3*. A dip you can roll into and get stuck in because the ground rises in every direction. The field was frightened of these for years. With a billion directions the odds that not one of them slopes down are effectively nil, so it turned out to be mostly an artifact of drawing the picture in two dimensions.

**Logits** · *Part 10*. The raw scores over every word in the vocabulary, before softmax turns them into percentages.

**Loss** · *Part 3*. A single number that is large when the model is wrong and zero when it is perfect. That is the whole specification, and which loss you choose decides what the machine actually aims at.

**LSTM** · *Part 8*. Long short-term memory, 1997. A better index card: a separate memory line that is mostly added to rather than overwritten, so the learning signal survives hundreds of steps instead of dozens. A real improvement, and not a fix, because everything still had to squeeze through one vector and it still could not be parallelised.

## M

**MLP** · *Part 7*. The other half of a transformer layer, alongside attention. Stacked knobs with a bend in the middle, applied to each position on its own. Also called a feed-forward block. A lot of the weights live here.

**Multi-head** · *Part 9*. Running attention several times in parallel with different knobs. See **head**.

## N

**Nonlinearity** · *Part 7*. The bend between layers, and the single most important internal fact in deep learning. Without one, stacked layers fold into a single layer and a hundred of them compute exactly what one computes. It is the only reason depth does anything.

## O

**Open source** · *Part 16*. Weights, plus the training data, plus the recipe. In principle you could rebuild it yourself. Rare, because the data and the recipe are the actual crown jewels. The recipe, the ingredient list, and the address of the farm.

**Open weight** · *Part 16*. The company publishes the finished weights and you download them, usually under a license with conditions. You do not get the training data or the recipe. This is not the same as open source, and *"weights available"* is often the honest phrase. The finished dish and the keys to a kitchen.

## P

**Parameter** · *Part 7*. Another word for a weight. A knob. Model sizes are counted in these.

**Perceptron** · *Part 2*. One neuron, 1958. Score each input, multiply by how much it matters, add it up, and if the total clears a bar, act. The smallest piece of everything that follows.

**Positional embedding** · *Part 10*. A second vector added alongside a token's own, saying where in the sentence it sat. Attention sees everything at once and a shot has no left or right in it, so without this, *dog bites man* and *man bites dog* arrive as the same soup.

**Pretraining** · *Part 11*. Running the four-step training loop on an enormous pile of text. It is next-token prediction and nothing else, and because the model sees far more text than it has room to store, the only way to bring the loss down is to learn the structure that generates the text.

## Q

**Quantization** · *Part 17*. Lossy compression for weights. Take a block of them, chop their range into a small number of buckets, and store which bucket each one landed in. Every weight comes out slightly wrong and the model gets a bit dumber, and it is an outrageous bargain: 16 bits down to 4 costs a few percent of quality and four times less memory. It is a JPEG.

**Query** · *Part 9*. What a token is looking for. What you say out loud in a room full of people before you read anyone's badge.

## R

**RAG** · *Part 6*. Embed everything you have, then find the nearest neighbours to the question in that space and hand them to the model. When somebody says their product does semantic search, this is the machinery. Properly covered in Act IV.

**Recurrent neural network, RNN** · *Part 8*. Reading a sequence strictly in order, one token at a time, carrying everything in one hidden state. Two fatal problems: the state gets overwritten, and it cannot be parallelised, so the hardware that had just transformed the field was useless to it.

**ReLU** · *Part 5*. The bend that does not flatten out: negatives become zero, everything else passes through. The least impressive-looking idea in the series and it is in essentially every model built since 2012, because it stops the blame evaporating on its way back and finally let deep networks train.

**Residual connection** · *Part 10*. `x = x + something` rather than `x = something`, so each layer contributes a correction instead of throwing out the work of every layer before it. Addition is kind to the learning signal in a way repeated multiplication is not, which is most of why very deep networks can be trained at all.

## S

**Scaling laws** · *Part 11*. Empirical curves saying how much better the loss gets when you add parameters, data or compute. They are the reason anyone was willing to spend a hundred million dollars before seeing the result. You could extrapolate the curve and it kept being right.

**Sigmoid** · *Part 5*. The S-shaped bend that squashes anything into 0 to 1, and the same curve fuzzy logic calls a membership function. It flattens at both ends, and anything flat passes almost nothing backwards, which is what stalled deep learning for twenty years. People still say *"the sigmoid saturates."*

**Softmax** · *Part 1b*. Turns a list of scores into percentages that add up to 100. It is how raw scores become "41% big, 27% small", and how attention distributes exactly all of a token's attention across the sentence.

## T

**Temperature** · *Part 1b*. How much randomness to allow when picking the next word. Turn it down and the model takes the safe option every time; turn it up far enough and it will eventually say `purple`.

**Token** · *Part 6*. What the model actually reads. Not characters and not quite words, but word-pieces. Common words are usually one token, rarer ones come apart into several, and the leading space is part of the token. This is why counting letters is structurally hard, why arithmetic is worse than you would expect, and why the same sentence can cost three times more in Hindi than in English.

**Tokenizer** · *Part 6*. The thing that does the chopping, before the model sees anything. Its vocabulary is fixed, typically 30,000 to 150,000 tokens, and the model can only ever see the world through it.

**Transformer** · *Parts 9 and 10*. The architecture, 2017. Embed, then a stack of layers each holding attention plus an MLP, then unembed to a score for every word and sample one. That is the complete skeleton of every large language model in existence. They differ in size, data and tuning, not in this shape.

## U

**Unembed** · *Part 7*. The reverse of embedding. The final vector gets scored against the whole vocabulary, and softmax turns those scores into the percentages you sample from.

## V

**Value** · *Part 9*. What a token actually hands over when another token decides it is relevant. Separate from the **key** on purpose: what makes you findable is not the same as what you have to give.

**Vanishing gradient** · *Part 5*. Every time the blame crosses a layer, a little of the signal is lost. Across four or five layers almost nothing arrives, so the layers nearest the input never learn and the front of the network is decoration. The standard story for why deep learning stalled, and ReLU is most of the fix.

**Vector** · *Part 6*. A list of numbers. That is genuinely all. When somebody says a word "is a vector", they mean it has been turned into a position in a space.

**Vector database** · *Part 6*. Storage that finds things by nearest neighbour in embedding space rather than by matching text. See **RAG**.

**VRAM** · *Part 17*. The memory on the graphics card. Quantized weights plus the KV cache plus overhead have to fit in it, and when they do not, layers spill onto the CPU and everything slows down.

## W

**Weight** · *Part 1b*. A knob. It says how much one thing matters. All the knobs together are the model's knowledge, and they are the only part that is ever learned. Everything else is fixed plumbing.

**Weighted sum** · *Part 2*. Multiply each input by its own knob and add up the results. The single most common thing anyone in this field will say to you, and it means exactly that and nothing more. Also called a **dot product**. When somebody says a model is "mostly matrix multiplies", they mean it is doing enormous numbers of these at once.

**Word2vec** · *Part 5*. 2013, Google. Train a small network to predict a word from the words around it, throw the network away, keep the numbers. The first evidence anybody really believed that meaning could just be a position in a space, learned from raw text with nobody defining what a direction stood for.

---

*Missing a word, or think one of these is wrong? That is the point. Tell me.*

*[← Back to the series index](ai-internals-00-index.md)*
