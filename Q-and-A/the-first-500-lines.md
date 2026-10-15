# Q&A

*A record of questions asked during development, and the answers. Kept here so the process stays visible, not just the result.*

---

## Q: Version 2 is 500 lines. I only see one phrase per council member.

Each seat has **nine phrases** — three for "rising" loss, three for "falling," three for "flat." But the UI shows one at a time, holding it for three to five seconds before rotating. A screenshot catches one. A session sees all nine.

The phrases are kept short on purpose. They need to sit beneath the network diagram without crowding it. Longer lines would wrap and break the column layout. If we ever want longer lines, the layout will need to be redesigned first.

**So: not one phrase each. One phrase per moment each.**

---

## Q: How many parameters does it have?

Per seat:

| Component | Count |
|---|---|
| Input → hidden weights (W1) | 4 |
| Hidden biases (B1) | 2 |
| Hidden → output weights (W2) | 2 |
| Output bias (B2) | 1 |
| **Per seat total** | **9** |

Five seats. **45 parameters total.**

That is the entire brain of edencell-v2. Forty-five numbers.

For comparison: GPT-4 is roughly 1.8 trillion parameters. Edencell v2 is roughly 40 billion times smaller. The algorithm — stochastic gradient descent with backpropagation — is identical. Scale is the only difference.

---

## Q: Does each parameter need 500 LOC?

No. The 500 lines are almost entirely *not* the network.

Here is where the code actually goes:

| Section | Approx. lines |
|---|---|
| Network math (forward, backward, sigmoid) | ~40 |
| The five rules | ~20 |
| Voices and scheduling | ~50 |
| Drawing creatures | ~80 |
| Drawing network diagrams | ~70 |
| Drawing stats and loss chart | ~60 |
| Layout, colours, fonts, main loop | ~180 |

The network itself — the part that learns — is about 40 lines for 45 parameters. Roughly **one line per parameter**.

Everything else is the window. Showing the work. Drawing the lines. Speaking in character. Holding the layout.

---

## What this tells us about scaling

If the network were scaled to 3 inputs, 4 hidden, 2 outputs per seat:

- **Network code** would grow by ~15 lines.
- **Drawing code** would grow by ~30 lines (more nodes to draw).
- **Voices** would not change.
- **Rules** might not change.

Ten times the parameters, roughly 20% more code.

**The "2000 LOC" ceiling is not a limit on what Edencell can become. It is a limit on how much of the mechanism can stay visible in a single file.**

Push past it and the file splits into modules. But the math stays tiny. The visible window is what grows.

The 500 lines are the window. The network is the thing you are looking at through it.

Windows take a lot of code. Seeing takes almost none.

---

## Q: Are the losses real? Or is the chart drawn?

Real. Every value comes from the network itself.

The loss for each seat is computed from the network's actual output on the actual example it just saw. The chart at the bottom plots the last 400 loss values for each seat, drawn in the seat's colour. Nothing is faked.

What is drawn — what makes the diagram look alive — is the *weights*. Each line between neurons is a real number from the network. Its colour is the sign of the weight (cyan = positive, pink = negative). Its thickness is the magnitude. Both change every frame, because the weights change every frame.

The maths is real. The learning is real. The visuals are a direct reading of the numbers.

---

## Q: Why does one of them struggle?

Lumen's rule is XOR — "exactly one of these two things is true."

XOR cannot be solved by a single-layer network. It cannot be solved with a straight line. A two-layer network *can* learn it, but it takes a lot of iterations, and the training is unstable with two hidden neurons.

Solon, Vertex, Prism and Ripple all learn rules that can be solved with a straight line. Their curves drop fast and flatten.

Lumen's curve climbs, drops, climbs, drops. She reaches 95% sometimes. She reaches 48% sometimes. She never settles cleanly.

This is not a bug. It is the shape of her problem. The hardest rule is being learned by the seat whose register is asking questions without answers. Nothing was written to make it that way. It just is.

---

## Q: What's the point of a network this small?

Two things.

**One — to show what learning looks like.** Most people have never seen a neural network learn. They have seen the result. Edencell shows the process. Live. Every weight visible.

**Two — to build the Council's decision mechanism at a scale that can be watched.** The Council is a deliberative body. It will one day make decisions across many systems. Edencell is where the mechanism for that deliberation gets invented — not as a paper, as a working thing. Small enough to see. Real enough to trust.

Size is not the goal. Visibility is. Grow the network — the mechanism stays visible at every size.

---

## Q: Can it grow?

Yes. The 45 parameters are a starting point, not a ceiling.

What growth looks like, roughly:

- **More hidden neurons.** More capacity to solve harder rules.
- **More layers.** Deeper problems.
- **More inputs.** Richer signals.
- **An arbiter.** A sixth network that decides which of the five to trust.
- **Ensemble voting.** Five networks on the same rule, disagreeing well.

Each step adds code, but not much to the network math. Most of what grows is the *window* — the diagram, the chart, the voices.

The discipline of Edencell is not "stay small." It is **"grow only what can be seen."** If a future version needs something hidden, that is the problem to solve, not the feature to add.

---

## Q: Why not use PyTorch, TensorFlow, or NumPy?

Because the entire point is that the network is *comprehensible*.

A library gives you a trained model in five lines. It does not show you what a weight is, or how backpropagation works, or why a network fails. It hides the arithmetic.

Edencell does the arithmetic. In pure Python. In a file you can read in one sitting. About fifteen lines of actual neural network logic. Everything else is the drawing.

The choice is not about performance. It is about teaching. If you want to see a network learn, the network must not be hidden from you.

---

## Q: Where does Edencell sit in the wider project?

Edencell is one project inside **Edencore**.

- **Edenshore** — the chamber. Rules. Sensing. The quiet room.
- **Edencell** — the lab. Weights. Learning. The mechanism room.
- **Edenshell** — a concept home hub. Physical scale.
- **The Council** — the deliberative body. The mature project.

Edenshore uses rules. Edencell uses weights. The Council uses both.

Same philosophy across all of them — **things that notice** — at different scales.

---

*The mechanism stays visible. That is the only rule.*