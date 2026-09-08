# Part 10 — Build a Transformer

*[← Part 9](ai-internals-09-attention.md) · [Series index](ai-internals-00-index.md) · Next: [Pretraining →](ai-internals-11-pretraining.md)*

Enough drawing.

Here is a complete transformer forward pass in about 150 lines of pure NumPy. Every stage from Parts 1 through 9, on numbers small enough to read with your eyes. We push `"hello world"` through it and watch the plumbing turn.

> **Download it:** [`tiny_transformer.py`](tiny_transformer.py). Runs on any machine with Python and NumPy (`pip install numpy`). No GPU, no framework, nothing to configure.

One honest caveat, and it is the most useful thing in this part. **The weights are random. They were never trained.** So the prediction at the end is nonsense, and it is supposed to be. That separates the two things people constantly confuse, the **mechanism** from the **knowledge**. The plumbing here is exactly right. It simply has not been to school yet.

## If you do not write Python, read this bit and skip the block

The code below is here so that nobody has to take my word for anything. You do not have to read it. **The printouts in the next section are the part that matters**, and they are plain numbers with plain explanations under them, so you can jump straight there and lose nothing.

If you do want to look, four things are worth knowing and then it mostly reads like English.

- `@` is the weighted sum from Part 2, done to a whole batch of numbers at once. Wherever you see it, that is knobs being applied.
- `randn(...)` hands back random numbers. That is us filling the knobs with noise, since this model was never trained.
- `.reshape(...)` changes no number. It deals the same numbers into a different arrangement, like splitting one deck into two piles.
- `(11, 16)` is a shape. Eleven rows, one per token, sixteen numbers in each. Watch that shape, it is the thing that never changes.

## Three things in the code I have not explained yet

The parts so far cover almost everything below, but three pieces turn up in the code that we have not met in prose, and all three are small. They are also in every real model, so they are worth having.

**Position.** Attention, as I described it in Part 9, has no sense of order. Every token looks at every other token in one shot, and a shot has no left or right in it. Which means *dog bites man* and *man bites dog* would arrive as the exact same soup. The fix is blunt and it works: alongside the vector that says which word this is, add a second vector that says where it sat in the sentence. In the code that is `pos_table`, and it gets added straight onto the embedding. Word identity plus seat number, in one vector.

**Adding instead of replacing.** Look at the two lines in the layer loop and you will see `x = x + something` rather than `x = something`. That is a **residual connection**, and it says each layer contributes a correction rather than throwing out the work of every layer before it. Back in the kitchen, each station adjusts the dish and passes it on. It does not start again from raw ingredients. There is a second reason too, and Part 8 already set it up: addition is kind to the learning signal in a way that repeated multiplication is not, so the signal can travel back down through eighty layers without fading to nothing. Residuals are most of why very deep networks can be trained at all.

**Keeping the numbers sane.** `layernorm` rescales a vector so its numbers sit in a sensible range, and it runs before each half of every layer. That is all it does. Without it the numbers drift a little every pass, and thirty-two passes later the whole thing is either enormous or zero. It is the sound engineer levelling every track so nothing blows out the speakers.

Everything else in the block, you already know.

## The code

```python
import numpy as np
np.random.seed(0)
np.set_printoptions(precision=2, suppress=True, linewidth=120)

# --- hyperparameters (tiny, so we can read everything) ---
d_model    = 16                  # length of each token vector (hidden dim, d)
n_heads    = 2                   # parallel attention heads
head_dim   = d_model // n_heads  # = 8
n_layers   = 6                   # stack depth
d_ff       = 4 * d_model         # MLP hidden size (the usual 4x)
block_size = 32                  # max tokens we could handle
text = "hello world"

# --- 1. TOKENIZE (character-level) ---
vocab = sorted(set(text))
stoi  = {c: i for i, c in enumerate(vocab)}
itos  = {i: c for c, i in stoi.items()}
V     = len(vocab)
ids   = np.array([stoi[c] for c in text])
T     = len(ids)

def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x); return e / e.sum(axis=axis, keepdims=True)
def layernorm(x):
    mu = x.mean(-1, keepdims=True); var = x.var(-1, keepdims=True)
    return (x - mu) / np.sqrt(var + 1e-5)
def gelu(x):
    return 0.5 * x * (1 + np.tanh(0.797885 * (x + 0.044715 * x**3)))
def randn(*s): return np.random.randn(*s) * 0.2

# --- 2. EMBED + positional ---
embedding_table = randn(V, d_model)
pos_table       = randn(block_size, d_model)
x = embedding_table[ids] + pos_table[:T]      # (T, d_model)

# --- one transformer layer ---
def attention(x, WQ, WK, WV, WO):
    T = x.shape[0]
    q = (x @ WQ).reshape(T, n_heads, head_dim)
    k = (x @ WK).reshape(T, n_heads, head_dim)
    v = (x @ WV).reshape(T, n_heads, head_dim)
    out = np.zeros((T, n_heads, head_dim))
    for h in range(n_heads):
        scores = q[:, h] @ k[:, h].T / np.sqrt(head_dim)   # (T, T)
        mask = np.triu(np.ones((T, T)), k=1).astype(bool)  # causal
        scores[mask] = -np.inf
        weights = softmax(scores, axis=-1)                 # rows sum to 1
        out[:, h] = weights @ v[:, h]                      # blend Values
    return out.reshape(T, d_model) @ WO

def mlp(x, W1, W2):
    return gelu(x @ W1) @ W2            # linear → nonlinearity → linear

layers = [dict(
    WQ=randn(d_model, d_model), WK=randn(d_model, d_model),
    WV=randn(d_model, d_model), WO=randn(d_model, d_model),
    W1=randn(d_model, d_ff),    W2=randn(d_ff, d_model),
) for _ in range(n_layers)]

# --- 3. run the layers (with residuals + pre-layernorm) ---
for L in layers:
    x = x + attention(layernorm(x), L['WQ'], L['WK'], L['WV'], L['WO'])
    x = x + mlp(layernorm(x), L['W1'], L['W2'])

# --- 4. unembed → probabilities → next token ---
logits = layernorm(x) @ embedding_table.T   # (T, V)
probs  = softmax(logits[-1])
pred   = itos[int(np.argmax(probs))]
```

*(The [full script](tiny_transformer.py) adds print statements that narrate each stage, so run it to see the numbers.)*

## What it prints, which is the machine thinking

**Tokenize.** `"hello world"` becomes 11 integers over an 8-character vocabulary. Note that `'l'` maps to `4` all three times it appears. Same token, same ID, every time, no context yet. Exactly the Part 6 lookup.

```
vocab (8 chars) : [' ', 'd', 'e', 'h', 'l', 'o', 'r', 'w']
token IDs (T=11): [3, 2, 4, 4, 5, 0, 7, 5, 6, 4, 1]
```

**Embed.** Those 11 IDs become 11 vectors of length 16, shape `(11, 16)`. Text is now geometry.

**Attention, and this is the one to stare at.** Here is the real 11 by 11 softmax grid out of layer 0, head 0.

```
[[1.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.  ]   ← 'h' can only see itself
 [0.39 0.61 0.   0.   0.   0.   0.   0.   0.   0.   0.  ]   ← 'e' sees 'h','e'
 [0.11 0.26 0.62 0.   0.   0.   0.   0.   0.   0.   0.  ]   ← 'l' sees 'h','e','l'
 [0.15 0.07 0.6  0.18 0.   0.   0.   0.   0.   0.   0.  ]
 [0.23 0.2  0.15 0.25 0.17 0.   0.   0.   0.   0.   0.  ]
 [0.17 0.06 0.03 0.08 0.26 0.41 0.   0.   0.   0.   0.  ]
 [0.17 0.16 0.11 0.12 0.12 0.16 0.17 0.   0.   0.   0.  ]
 [0.15 0.1  0.27 0.17 0.07 0.04 0.13 0.07 0.   0.   0.  ]
 [0.16 0.07 0.04 0.08 0.16 0.14 0.07 0.14 0.14 0.   0.  ]
 [0.14 0.02 0.1  0.06 0.12 0.18 0.14 0.12 0.1  0.03 0.  ]
 [0.08 0.04 0.31 0.09 0.05 0.02 0.14 0.06 0.04 0.07 0.1 ]]
```

Three things are visible right there, and all three were predicted in Part 9.

**It is triangular.** The entire upper right is zero. That is the **causal mask**: a token is forbidden from seeing the future. Token 0 has nowhere to look but itself, so it gets 1.0. This is the actual reason generation runs left to right, and you are looking at it.

**Every row sums to 1.0.** That is softmax doing what it said it would, distributing exactly 100% of each token's attention.

**It is 11 by 11.** Twenty-two tokens would give a 22 by 22 grid, four times the cells. That is the seating-chart cost from Part 9, sitting in front of you as a printed array. Act IV turns it into gigabytes.

And through all six layers, `x` stays `(11, 16)`. Vector in, same size vector out, every single layer. The shape rule from Part 7, proven rather than asserted.

**The prediction, which is garbage:**

```
'd'   28.7%  ###########
'o'   17.5%  ######
'r'   14.1%  #####
...
greedy next char -> 'd'   (nonsense, because untrained)
```

The machine is perfect. The knowledge is missing. That gap is training.

## What else? Count the parameters

```
embeddings :     128    (V × d_model)
positions  :     512
per layer  :   3,072    (4 attention matrices + 2 MLP matrices)
× 6 layers :  18,432
TOTAL      :  19,072 parameters
```

Nineteen thousand and seventy two knobs.

A 7B model is this exact structure about **367,000 times bigger**. Same embed, same attention plus MLP layers, same unembed. Scale, data and training are the only differences. There is no additional secret ingredient waiting in the larger models, and I want to be clear about that because I half expected there would be.

## Go break it

Stop reading. Grab [`tiny_transformer.py`](tiny_transformer.py) and try these in order.

1. **Change `text` to `"the cat sat"`.** Watch the tokens and the grid resize themselves.
2. **Set `n_layers = 1`, then `20`.** Confirm the output shape never changes. Only the parameter count does.
3. **Comment out the two `mask` lines in `attention`.** Now every token can see the future and the triangle fills in. You have just broken causality, and you can watch it happen.
4. **Set `n_heads = 1`, then `4`.** Watch `head_dim` change and think about why the total stays constant.

Number three first. Breaking a property on purpose and seeing the exact number that moves is worth more than another page of me explaining it.

> **Say this out loud:** "A 7B model is the same nineteen thousand parameter structure, scaled up about 367,000 times. The attention grid is triangular because a token is not allowed to see the future, which is why generation goes left to right."

> **The question that takes you further:** *this is 19,072 parameters and a 7B model is the same shape. So what do the extra billions actually buy?*

### Checkpoint

1. Why is the attention grid triangular, and what would break if it were not?
2. This model has 19,072 parameters. Name the three places they live.
3. Our prediction was nonsense. What single thing is missing, and what would fix it?
4. The vector stays length 16 through every layer no matter how many layers you add. Why does that have to be true?

*Next: [Part 11 — Pretraining →](ai-internals-11-pretraining.md), where we run that same training loop on everything ever written and find out what falls out.*
