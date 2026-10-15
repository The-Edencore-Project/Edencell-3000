# Versions and Scale

*How Edencell grows. Parameters, lines, and the honest limits.*

---

## Q1 — Can we multiply parameters ×10 each version?

Mathematically, yes. Practically, the ×10 plan breaks around v5.

**The network math scales fine.** Going from 45 to 450 parameters is one more loop. Going from 450 to 4,500 is one more loop. Pure Python handles this. The math doesn't care.

**What breaks is the window:**

- **Drawing every weight as a line** stops working around 1,000 weights. At 4,500 lines redrawn at 20fps that's 90,000 draw calls per second. Tkinter chokes.
- **Training speed** becomes the bottleneck around v6. Pure Python backprop on 450,000 parameters runs minutes per step. A single epoch takes an hour.
- **Memory** becomes a problem around v8. 45 million parameters × 4 bytes = 180 MB just for the weights. Pydroid will die.

So ×10 works for the first three or four versions. After that, you change **architecture**, not just scale. Better math. Sampled visualisation. Possibly a different language or library for training.

The ×10 plan is a good *early* trajectory. It is not a *forever* trajectory.

---

## Q2 — Lines of code per version

Rough estimates. Assume the visible-mechanism discipline holds.

| Version | Parameters | LOC | Notes |
|---|---|---|---|
| v1 | 3 | ~200 | One neuron |
| v2 | 45 | ~500 | Five seats, five rules (built) |
| v3 | 450 | ~600 | More hidden, cleaner convergence |
| v4 | 4,500 | ~750 | Arbiter arrives, aggregated drawing begins |
| v5 | 45,000 | ~950 | Revolving presidency, sampled charts |
| v6 | 450,000 | ~1,200 | Ensemble voting, training slows |
| v7 | 4,500,000 | ~1,500 | Deeper networks, batch training |
| v8 | 45,000,000 | ~1,900 | Near LOC ceiling, most weights summarised |
| v9 | 450,000,000 | splits | Package. Multi-file. |
| v10 | 4,500,000,000 | splits | GPT-2 scale. Not a single file. |

The LOC curve is not linear. Early versions add ~100 lines each. Later versions add 300+. The reason: as networks grow, more of the file is *handling the scale* — batching, sampling, aggregating, and showing what can no longer be shown in full.

---

## Q3 — The first ten versions, analysed

**v1 — 3 parameters, ~200 lines.**
One neuron. One input, one output, one bias. Solves a trivial rule. Feels like nothing. That is the point.

**v2 — 45 parameters, ~500 lines.**
Five seats, nine each. Every weight visible. This is where we are now.

**v3 — 450 parameters, ~600 lines.**
More hidden neurons per seat. The hard problem finally settles. Drawing still works. Last clean version.

**v4 — 4,500 parameters, ~750 lines.**
The arbiter arrives — a sixth network deciding which seat to trust. You cannot draw 900 weights per seat anymore. You begin drawing *aggregates* — averages of layers, not each line. First compromise. Still honest if labelled.

**v5 — 45,000 parameters, ~950 lines.**
Revolving presidency. Different seats chair different questions. Weights are sampled — a random subset each frame. The chart still shows real losses.

**v6 — 450,000 parameters, ~1,200 lines.**
Ensemble voting. Five networks on the same rule. Individual weights invisible now, but *behaviour* is still visible — accuracy, loss, votes. Pure Python training starts hurting.

**v7 — 4.5M parameters, ~1,500 lines.**
Deeper networks. Batching required. Training moves to a background thread. You watch it slowly rather than live.

**v8 — 45M parameters, ~1,900 lines.**
Near the LOC ceiling. Most of the network cannot be shown anymore. You show summaries. The visibility discipline is stretched but holds.

**v9 — 450M parameters.**
File splits. Multiple modules. Two thousand lines is no longer enough. It becomes a package.

**v10 — 4.5B parameters.**
GPT-2 scale. Real training infrastructure needed. Pydroid is long gone.

---

## Q4, Q5, Q6 — The mind question

There is no known parameter count for a mind.

Anyone who says *"X billion parameters produces consciousness"* is guessing. Neuroscience does not know what consciousness is. Philosophy does not know what causes it. Computer science has never built one. The honest answer is: **nobody knows the number, because nobody knows the mechanism.**

But here is what *is* true:

**Scaling Edencell will not produce a mind.** Not because it is too small, but because parameters are not the right unit. A mind needs things Edencell does not have:

- **Drives** — hunger, curiosity, fear, wanting. Something it is trying to do.
- **Memory** — not just weights, but episodes. Things it remembers happening.
- **A body or a self** — a sense of where it ends and the world begins.
- **Time** — a continuous experience, not just training iterations.
- **Architecture** — brains are not transformers. They are recurrent, spiking, embodied, chemical.

None of these appear by scaling. They appear by design.

**What scaling Edencell will produce:**

- A system that can solve harder problems.
- An ensemble that votes better than any single member.
- An arbiter that learns to trust the right seat at the right moment.
- Something that looks, from outside, like a small deliberative intelligence.

That is not a mind. But it is real. And it is more than most projects ever reach.

---

## The honest reframe

The question *"how many versions until a mind?"* has no answer, because Edencell is not a path to one.

It is a **lab for the mechanism** — a place to learn how small networks combine into decisions. That knowledge is what a future mind-shaped system will be built from.

Edencell does not *become* the mind. It teaches how to *build* one.

So the useful question is not *"when does it become a mind?"*

The useful question is *"what can be learned from it at each size?"*

The first has no answer. The second has one per version, ten times over.

---

## A note on the LOC ceiling

The 2000-line figure is not a law. It is a working constraint.

Past v8, Edencell stops being a single file. It becomes a package. That is fine — it is what any growing project does. The lines are not what matters. What matters is that the mechanism stays visible.

If a version grows past what can be shown in one file, the visibility is preserved across files. That is not the same problem. It is a bigger version of the same problem.

The discipline survives the split. It just has to be designed to.

---

*The size of the network is not the question.*

*The size of the window is.*

*Windows take a lot of code. Seeing takes almost none.*