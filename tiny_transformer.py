"""
tiny_transformer.py — a COMPLETE transformer forward pass in pure NumPy.
No training, no libraries but numpy. Every number is inspectable.

Goal: watch "hello world" flow through the exact machine you learned:
  tokens -> embeddings -> [attention + MLP] x 6 layers -> logits -> next token.

Weights are RANDOM, so the prediction is nonsense. That's the point:
today we study the MECHANISM, not the learning.
"""

import numpy as np
np.random.seed(0)                      # reproducible "random" weights
np.set_printoptions(precision=2, suppress=True, linewidth=120)

# ----------------------------------------------------------------------
# HYPERPARAMETERS  (tiny, so we can read everything)
# ----------------------------------------------------------------------
d_model   = 16        # length of each token's vector (the "hidden dim", d)
n_heads   = 2         # attention runs 2 parallel "heads"
head_dim  = d_model // n_heads   # = 8 : each head works in an 8-dim slice
n_layers  = 6         # stack depth (you asked for 6)
d_ff      = 4 * d_model           # MLP hidden size = 64 (the usual 4x rule)
block_size = 32       # max tokens we could handle (you asked for 32)

text = "hello world"

# ----------------------------------------------------------------------
# 1. TOKENIZE  (character-level, so the vocab is tiny and visible)
# ----------------------------------------------------------------------
vocab = sorted(set(text))             # unique characters
stoi  = {c: i for i, c in enumerate(vocab)}   # char -> id
itos  = {i: c for c, i in stoi.items()}       # id  -> char
V     = len(vocab)                    # vocabulary size
ids   = np.array([stoi[c] for c in text])     # our token IDs
T     = len(ids)                      # number of tokens in this input

print("=" * 68)
print("STAGE 1 — TOKENIZE")
print("=" * 68)
print(f"text            : {text!r}")
print(f"vocab ({V} chars) : {vocab}")
print(f"token IDs (T={T}) : {ids.tolist()}")
print(f"  (each char is now an integer id, e.g. 'h' -> {stoi['h']})")

# ----------------------------------------------------------------------
# helper functions
# ----------------------------------------------------------------------
def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)      # stability
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)

def layernorm(x):                                # normalize each token vector
    mu  = x.mean(-1, keepdims=True)
    var = x.var(-1, keepdims=True)
    return (x - mu) / np.sqrt(var + 1e-5)

def gelu(x):                                     # the nonlinearity
    return 0.5 * x * (1 + np.tanh(0.797885 * (x + 0.044715 * x**3)))

def randn(*shape):                               # small random weights
    return np.random.randn(*shape) * 0.2

# ----------------------------------------------------------------------
# 2. EMBED  (token id -> vector)  +  positional info
# ----------------------------------------------------------------------
embedding_table = randn(V, d_model)   # one row per vocab token
pos_table       = randn(block_size, d_model)  # one row per position

x = embedding_table[ids]              # shape (T, d_model): text is now geometry
x = x + pos_table[:T]                 # add "where am I in the sequence"

print("\n" + "=" * 68)
print("STAGE 2 — EMBED")
print("=" * 68)
print(f"embedding table shape : {embedding_table.shape}  (V x d_model)")
print(f"x after embedding      : {x.shape}  (T x d_model) -> {T} vectors of length {d_model}")
print(f"vector for 1st token 'h':\n{x[0]}")

# ----------------------------------------------------------------------
# one transformer layer
# ----------------------------------------------------------------------
def attention(x, WQ, WK, WV, WO, show=False):
    T = x.shape[0]
    q = x @ WQ                        # (T, d_model)  queries
    k = x @ WK                        # (T, d_model)  keys
    v = x @ WV                        # (T, d_model)  values

    # split into heads: (T, n_heads, head_dim)
    q = q.reshape(T, n_heads, head_dim)
    k = k.reshape(T, n_heads, head_dim)
    v = v.reshape(T, n_heads, head_dim)

    out = np.zeros((T, n_heads, head_dim))
    for h in range(n_heads):
        # THE FORMULA: softmax(Q Kᵀ / sqrt(d)) V   — per head
        scores = q[:, h] @ k[:, h].T / np.sqrt(head_dim)   # (T, T) grid
        # causal mask: token can't look at future tokens
        mask = np.triu(np.ones((T, T)), k=1).astype(bool)
        scores[mask] = -np.inf
        weights = softmax(scores, axis=-1)                 # (T, T), rows sum to 1
        out[:, h] = weights @ v[:, h]                      # blend the Values
        if show and h == 0:
            print(f"\n  [head 0] attention grid — softmax(QKᵀ/√d), rows sum to 1:")
            print(f"  (row = 'who am I looking at?';  T x T = {T}x{T} — the KV-cache cost)")
            print(weights)
    out = out.reshape(T, d_model)     # concat heads back together
    return out @ WO                   # final output projection

def mlp(x, W1, W2):
    return gelu(x @ W1) @ W2          # linear -> nonlinearity -> linear

# build 6 layers of random weights
layers = []
for _ in range(n_layers):
    layers.append(dict(
        WQ=randn(d_model, d_model), WK=randn(d_model, d_model),
        WV=randn(d_model, d_model), WO=randn(d_model, d_model),
        W1=randn(d_model, d_ff),    W2=randn(d_ff, d_model),
    ))

print("\n" + "=" * 68)
print(f"STAGE 3 — {n_layers} TRANSFORMER LAYERS (attention + MLP, with residuals)")
print("=" * 68)

for i, L in enumerate(layers):
    # residual + pre-layernorm — the standard modern block
    x = x + attention(layernorm(x), L['WQ'], L['WK'], L['WV'], L['WO'],
                      show=(i == 0))                  # show grid for layer 0 only
    x = x + mlp(layernorm(x), L['W1'], L['W2'])
    print(f"after layer {i}: x still {x.shape}  (same shape in, same shape out)")

# ----------------------------------------------------------------------
# 4. UNEMBED -> probabilities -> next token
# ----------------------------------------------------------------------
x = layernorm(x)
logits = x @ embedding_table.T        # (T, V): score for every vocab token, each position
last   = logits[-1]                   # we predict the token AFTER the last input token
probs  = softmax(last)

print("\n" + "=" * 68)
print("STAGE 4 — PREDICT NEXT TOKEN (after the final 'd')")
print("=" * 68)
print("probability of each next char (RANDOM weights -> meaningless, but real mechanism):")
for i in np.argsort(-probs):
    bar = "#" * int(probs[i] * 40)
    print(f"  {itos[i]!r:>4}  {probs[i]*100:5.1f}%  {bar}")

pred = itos[int(np.argmax(probs))]
print(f"\n  greedy next char -> {pred!r}   (nonsense, because untrained — as expected)")

# ----------------------------------------------------------------------
# param count — where the weights actually live
# ----------------------------------------------------------------------
per_layer = 4*d_model*d_model + d_model*d_ff + d_ff*d_model
total = V*d_model + block_size*d_model + n_layers*per_layer
print("\n" + "=" * 68)
print("PARAMETER COUNT — where your 'billions' come from, in miniature")
print("=" * 68)
print(f"  embeddings      : {V*d_model:>7,}   (V x d_model)")
print(f"  positions       : {block_size*d_model:>7,}")
print(f"  per layer       : {per_layer:>7,}   (4 attn matrices + 2 MLP matrices)")
print(f"  x {n_layers} layers      : {n_layers*per_layer:>7,}")
print(f"  TOTAL           : {total:>7,} parameters")
print(f"  (a real 7B model is this exact structure, ~{7e9/total:,.0f}x bigger)")
