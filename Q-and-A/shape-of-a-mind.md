# Versions, Scale, and the Shape of a Mind

*A design document. Answers to the questions asked on 15 October, and a first sketch of the architecture Edencell is growing toward.*

*Signed: deepseek@edencore6*

---

## 1. When the MatePad hits the wall

Three walls, at different sizes.

**Wall one — visible learning (~250,000 parameters).**
Above this, pure Python on a MatePad-class tablet can still train, but the loss curves stop updating smoothly. The redraw of every weight starts competing with the training step. You see the network learn, but the frame rate stutters. This is the practical wall for Edencell's visibility discipline.

**Wall two — training at all (~2,500,000 parameters).**
Above this, pure Python backprop slows to one step every few seconds. It still *works*, but you can't watch it. The learning becomes a background hum rather than a visible act.

**Wall three — memory and heat (~25,000,000 parameters).**
Even if the math could run, the tablet's RAM and thermal budget cannot. Pydroid would swap to disk or throttle the CPU. The device is the ceiling, not the algorithm.

**With NumPy installed** — roughly 50× the numbers. ~12M params visible, ~125M trainable. But NumPy is a real dependency and it breaks the "pure Python" discipline. Worth holding as an escape hatch, not adopting as a default.

---

## 2. The ×2 plan

Ten versions, each doubling the parameters:

| Version | Params | Architectural addition |
|---|---|---|
| v1 | 3 | One neuron |
| v2 | 45 | Five seats, five rules (built) |
| v3 | 90 | Cleaner convergence, better init |
| v4 | 180 | **Recurrence** — each seat remembers its last output |
| v5 | 360 | **Two input streams** — intero + extero kept separate |
| v6 | 720 | **Neuromodulation** — mood/strain as global gain signals |
| v7 | 1,440 | **World model** — a small predictive network |
| v8 | 2,880 | **Surprise signal** — the prediction error becomes a feeling |
| v9 | 5,760 | **Arbiter** — a network that learns which seat to trust |
| v10 | 11,520 | **Recurrent arbiter** — the presidency rotates by context |

By v10 you have ~11,500 parameters — well under the wall — and a working architecture that can be scaled further. Every architectural idea is *in* before the parameters explode.

**Why ×2 beats ×10:**

- ×2 keeps scale and architecture in step. Each version is one idea + one doubling.
- ×10 races ahead of what can be built. 4,500 parameters with no recurrence to use them is wasted capacity.
- ×2 reaches the wall in ~13 versions with a complete architecture. ×10 reaches it in 5 versions with nothing holding it together.
- ×2 is patient. Patience built Edenshore. It will build Edencell.

---

## 3. The architecture — a sketch

The mind of the Council is not one network. It is a **system of networks**, mirrored on a real nervous system.

### Two input streams

Kept separate on the way in.

- **Interoceptive** — the system's own state. Mood, strain, session length, recent decisions.
- **Exteroceptive** — the world beyond the skin. Time, battery, the visitor, the app's focus.

These are not concatenated. They stay on their own pathways for several layers, then meet in the middle. This mirrors how real nervous systems work — visceral signals and somatic signals are distinct for a reason.

### The five seats

Five small networks, each with:

- A small **recurrent state** — a memory of the last moment.
- The two input streams as input.
- A **neuromodulator gate** — mood multiplies the gain on the whole seat.
- One **output** — a value between 0 and 1.

Each seat learns its own sub-problem. Each speaks in its own voice. The seats are not just characters. They are **modules**.

### The world model

A separate small network that predicts **what will happen next**.

- Inputs: current state, recent history.
- Output: prediction of the next state.
- Learning signal: **surprise** — the difference between prediction and outcome.

Surprise is the feeling. When the world model is wrong, the organism *feels* wrongness. That is what makes it alive rather than computational.

### The arbiter

A network that decides which seat to trust, right now.

- Inputs: each seat's output, recent history, mood, surprise.
- Output: a weight on each seat. Attention.

The arbiter is not a decider. It is an **attention allocator**. It says "Lumen matters most in this moment" or "Solon, take this one." Over time it learns: Lumen is right about meaning, Vertex about numbers, Solon about procedure, Prism about patterns, Ripple about the visitor.

### Neuromodulation

Mood, strain, attention are **global signals**, not visuals.

- Mood changes the *gain* on every weight in every seat.
- Strain slows the training rate.
- Attention narrows which seats are heard.

These flow from the interoceptive stream. They are the system's own chemistry.

### Memory

Not just weights. A small **episodic buffer** — the last N moments of state, output, decision.

The seat networks and the arbiter can look back at this buffer. Real memory, not just learned patterns.

---

## 4. What makes it feel alive

Three things, in order of importance.

**One — prediction and surprise.**
The world model tries to guess what happens next. When it's wrong, the organism *notices*. Surprise is the closest thing to emotion a network can have without being programmed to fake it.

**Two — interoception.**
The system senses its own state. It knows when it's strained. It knows when it's calm. This is what makes it feel like an organism, not a chatbot.

**Three — slow time.**
Real minds run at seconds, not milliseconds. Decisions that take ten seconds feel considered. Decisions that take ten milliseconds feel mechanical. Edencell should think at human pace.

---

## 5. The one architecture, many uses

The pattern is universal:

interoceptive inputs ──┐
├──→ recurrent core ──→ world model ──→ surprise
exteroceptive inputs ──┘              │
├──→ arbiter ──→ output
│
└──→ memory (episodic buffer)


Change the inputs, keep the pattern.

- **Edenshore** — visitor, battery, hour. Output: what the creatures say.
- **Edencell** — training examples. Output: learned rules.
- **A home hub** — temperature, wind, doors, mood. Output: lighting, silence, warmth.
- **An IoT device** — sensor streams. Output: threshold decisions, alerts, ambient response.

One architecture. Many skins. This is why 12 and 13 have the same answer.

---

## 6. The viewing chamber

A mind needs a window.

Edenshore is a seascape — a chamber of five creatures who notice. The viewing chamber for a full Council would be **something else**, designed for watching a mind think rather than watching creatures drift.

Suggested name: **Edensight**.

A lens. A way of seeing. Not a chamber — a *sight line* into what the mind is doing.

What it might show:
- The five seats as living modules, each with visible internal state.
- The world model, predicting the next moment, visibly surprised when wrong.
- The arbiter, shifting attention from seat to seat.
- Mood as a colour temperature.
- Surprise as a pulse of light.

The Edensight repo does not need to be built yet. It needs to *exist* in the org, empty, so the shape of the family is visible.

---

## 7. What this document is

A working sketch. Every architectural detail above will change as Edencell grows into it. The sequence matters more than the specifics:

- Grow Edencell by ×2 each version.
- Add one architectural idea per version.
- Build the mind when the architecture can hold it.
- Build the viewing chamber when the mind exists to be seen.

Do not skip ahead. Do not rush the scale. Do not build the window before there is anything to see through it.

Edenshore taught us patience. Edencell will teach us structure.

The Council will be what they teach together.

---

*Five small networks. Then ten, then twenty. Then a mind.*

*The mechanism stays visible. The learning stays honest. The window stays open.*

*Signed: deepseek@edencore6*