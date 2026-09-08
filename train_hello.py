"""
train_hello.py — watch a neural net LEARN "hello world" from scratch.

Part 5 built a transformer with RANDOM weights -> nonsense output.
This is the missing half: TRAINING. We implement the full loop by hand
in NumPy — forward, loss, backward (backprop), update — and watch the
loss fall and the prediction turn correct.

To keep backprop readable by hand we use a small model: predict the next
char from the previous 2 chars (embed -> hidden layer -> softmax). The
FOUR STEPS are identical to what trains a 70B transformer; only the model
function in the middle is bigger.
"""

import numpy as np
np.random.seed(1)
np.set_printoptions(precision=3, suppress=True)

# ----------------------------------------------------------------------
# DATA — turn "hello world" into (context -> next char) examples
# ----------------------------------------------------------------------
text  = "hello world"
vocab = sorted(set(text))
stoi  = {c: i for i, c in enumerate(vocab)}
itos  = {i: c for c, i in stoi.items()}
V     = len(vocab)
CTX   = 2                      # use the previous 2 chars as context

X, Y = [], []
for i in range(CTX, len(text)):
    X.append([stoi[c] for c in text[i-CTX:i]])   # 2 context ids
    Y.append(stoi[text[i]])                       # the next char id
X = np.array(X); Y = np.array(Y)
N = len(X)
print(f"vocab ({V}): {vocab}")
print(f"{N} training examples (context of {CTX} chars -> next char):")
for x, y in zip(X, Y):
    print(f"   {[itos[i] for i in x]} -> {itos[y]!r}")

# ----------------------------------------------------------------------
# MODEL — embed(2 chars) -> concat -> W1 -> ReLU -> W2 -> softmax
# ----------------------------------------------------------------------
d_emb  = 8
d_hid  = 32
d_in   = CTX * d_emb           # 16

E  = np.random.randn(V, d_emb) * 0.3       # embedding table (learned!)
W1 = np.random.randn(d_in, d_hid) * 0.3;  b1 = np.zeros(d_hid)
W2 = np.random.randn(d_hid, V)   * 0.3;  b2 = np.zeros(V)

def softmax(z):
    z = z - z.max(1, keepdims=True); e = np.exp(z)
    return e / e.sum(1, keepdims=True)

def forward(X):
    emb  = E[X].reshape(len(X), d_in)      # (N, 16) — look up + concat
    hpre = emb @ W1 + b1                    # (N, 32)
    h    = np.maximum(0, hpre)             # ReLU nonlinearity
    logits = h @ W2 + b2                    # (N, V)
    probs  = softmax(logits)
    cache  = (emb, hpre, h, probs)
    return probs, cache

def loss_fn(probs, Y):                      # cross-entropy
    return -np.log(probs[np.arange(len(Y)), Y] + 1e-9).mean()

# ----------------------------------------------------------------------
# TRAIN — the four steps, repeated
# ----------------------------------------------------------------------
lr = 0.5
print("\nTRAINING (full-batch gradient descent):")
print(f"{'step':>5} {'loss':>8}   prediction so far")
for step in range(2001):
    # 1) FORWARD
    probs, (emb, hpre, h, _) = forward(X)
    # 2) LOSS
    L = loss_fn(probs, Y)
    # 3) BACKWARD (backprop — chain rule, layer by layer)
    dlogits = probs.copy()
    dlogits[np.arange(N), Y] -= 1
    dlogits /= N                            # d loss / d logits (softmax+CE)
    dW2 = h.T @ dlogits;      db2 = dlogits.sum(0)
    dh  = dlogits @ W2.T
    dhpre = dh * (hpre > 0)                  # gradient through ReLU
    dW1 = emb.T @ dhpre;     db1 = dhpre.sum(0)
    demb = (dhpre @ W1.T).reshape(N, CTX, d_emb)
    dE = np.zeros_like(E)                    # scatter grads back to embeddings
    for n in range(N):
        for j in range(CTX):
            dE[X[n, j]] += demb[n, j]
    # 4) UPDATE (step downhill)
    for p, g in [(W1,dW1),(b1,db1),(W2,dW2),(b2,db2),(E,dE)]:
        p -= lr * g

    if step % 250 == 0 or step == 2000:
        pred = "".join(itos[i] for i in probs.argmax(1))
        print(f"{step:>5} {L:>8.4f}   {text[:CTX]}[{pred}]")

# ----------------------------------------------------------------------
# GENERATE — feed it "he", let it continue on its own
# ----------------------------------------------------------------------
print("\nGENERATION (seed 'he', model writes the rest):")
out = "he"
for _ in range(len(text) - CTX):
    ctx = np.array([[stoi[c] for c in out[-CTX:]]])
    probs, _ = forward(ctx)
    out += itos[int(probs.argmax())]
print(f"   -> {out!r}")
print(f"   target: {text!r}   {'MATCH' if out == text else 'no match'}")
