# How AI Actually Works

A narrative series on what is actually inside a large language model, written by
someone who trained neural networks by hand in 2002 and came back twenty years
later to find out what he had missed.

It assumes no maths. The audience is a highschooler, or an adult who does not
work in technology, and the goal is that you finish able to hold a real
conversation with an AI engineer and push back on parts of it.

**Read it: https://tiwaana.github.io/claude-ai-internals/**

## What is here

- `docs/` — the parts, as markdown.
- `index.html` — the reader. Plain HTML, no build step, no framework.
- `playground.html` — five toys that genuinely compute. The perceptron really
  fits its weights, gradient descent really diverges when you push the learning
  rate up, the attention arcs are real softmax weights. Nothing is animated.
- `tiny_transformer.py` — a full transformer forward pass in ~150 lines of NumPy.
- `train_hello.py` — backpropagation by hand, no framework.

## Running it locally

    python3 -m http.server 8080

Then open <http://localhost:8080/>.

## Corrections

Half the reason this is public is so somebody who knows better can correct it.
Open an issue. Wrong facts get fixed and credited.

Generated from a private source repository by `bin/export-series`. Do not edit
these files here, the change would be overwritten on the next export.
