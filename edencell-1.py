# ============ EDENCELL — V1 ============
# A small neural network that learns in front of you.
# Three inputs, four hidden, one output. Trained live.
# The council watches.
# =======================================

import tkinter as tk, math, random, time

root = tk.Tk()
root.title("Edencell — v1")
try:
    root.attributes("-fullscreen", True)
except tk.TclError:
    pass
root.update_idletasks()
W, H = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (W, H))
root.configure(bg="#0a0208")

canvas = tk.Canvas(root, bg="#0a0208", width=W, height=H,
                   highlightthickness=0)
canvas.pack(fill="both", expand=True)

def font_px(px, bold=False):
    return ("Helvetica", -max(9, int(px)),
            "bold" if bold else "normal")

def clamp(v, lo, hi): return max(lo, min(hi, v))

# ---------- colours ----------
BG          = "#0a0208"
GRID        = "#1a1024"
TEXT_DIM    = "#7a6878"
TEXT_LIT    = "#e0d0e0"
LINE_POS    = "#80ffe0"
LINE_NEG    = "#ff80b8"
NODE_BASE   = "#1a2848"
NODE_LIT    = "#ffb060"
NODE_OUT    = "#5a1080"
LOSS_COL    = "#ffb060"
LOSS_GOOD   = "#80ffe0"

# ---------- the network ----------
# 3 inputs, 4 hidden, 1 output. All sigmoid. MSE loss.
N_IN   = 3
N_HID  = 4
N_OUT  = 1

W1 = [[random.uniform(-0.5, 0.5) for _ in range(N_HID)] for _ in range(N_IN)]
B1 = [0.0] * N_HID
W2 = [random.uniform(-0.5, 0.5) for _ in range(N_HID)]
B2 = 0.0

LR = 0.6

def sigmoid(x):
    if x < -60: return 0.0
    if x >  60: return 1.0
    return 1.0 / (1.0 + math.exp(-x))

# ---------- the problem ----------
# Three inputs. The network learns whether the visitor is present.
#   x0: screen is on (0 or 1)
#   x1: recent touch (0 or 1)
#   x2: hour is evening (0 or 1)
#   y:  visitor is present (roughly: x0 or x1, less likely at night)

def make_example():
    x0 = random.randint(0, 1)
    x1 = random.randint(0, 1)
    x2 = random.randint(0, 1)
    # target rule — the network does not know this
    if x0 == 1 and x1 == 1:
        y = 1
    elif x0 == 1 and x2 == 0:
        y = 1
    elif x1 == 1 and x2 == 0:
        y = 1
    else:
        y = 0
    return [x0, x1, x2], y

# ---------- training state ----------
STATE = {
    "epoch": 0,
    "loss": 1.0,
    "loss_hist": [],
    "last_loss": 1.0,
    "epochs_since_report": 0,
    "visitor_present": 0.0,
    "correct": 0,
    "total": 0,
    "paused": False,
}
COUNCIL = {"messages": [], "next_speak_at": 0.0}

# ---------- forward / backward ----------

def forward(x):
    h = []
    for j in range(N_HID):
        z = B1[j]
        for i in range(N_IN):
            z += x[i] * W1[i][j]
        h.append(sigmoid(z))
    z_out = B2
    for j in range(N_HID):
        z_out += h[j] * W2[j]
    o = sigmoid(z_out)
    return h, o

def train_step():
    x, y = make_example()
    h, o = forward(x)

    # loss (MSE with sigmoid derivative folded in)
    d_out = (o - y) * o * (1 - o)

    # hidden errors
    d_hid = []
    for j in range(N_HID):
        d_hid.append(d_out * W2[j] * h[j] * (1 - h[j]))

    # update W2, B2
    global B2
    for j in range(N_HID):
        W2[j] -= LR * d_out * h[j]
    B2 -= LR * d_out

    # update W1, B1
    for i in range(N_IN):
        for j in range(N_HID):
            W1[i][j] -= LR * d_hid[j] * x[i]
    for j in range(N_HID):
        B1[j] -= LR * d_hid[j]

    # track accuracy on this example
    pred = 1 if o > 0.5 else 0
    STATE["correct"] += 1 if pred == y else 0
    STATE["total"] += 1
    STATE["visitor_present"] = o
    return (o - y) ** 2

# ---------- council reactions ----------

COUNCIL_VOICES = {
    "Solon":  ["Loss noted.", "Epoch logged.", "Continuing.", "Weights updated."],
    "Lumen":  ["Is it learning?", "Does it know?", "How does it choose?"],
    "Vertex": ["Gradient stepped.", "Still descending.", "Numbers changing."],
    "Prism":  ["Every cycle, a small change.", "Converging.", "Pattern forming."],
    "Ripple": ["It's trying.", "Give it time.", "Almost."],
}
COUNCIL_SEATS = ["Solon", "Lumen", "Vertex", "Prism", "Ripple"]

def maybe_council_speak(now):
    if now < COUNCIL["next_speak_at"]: return
    # react to loss trend
    hist = STATE["loss_hist"]
    if len(hist) < 5:
        COUNCIL["next_speak_at"] = now + 3.0
        return
    trend = hist[-1] - hist[-5]
    if trend < -0.05:
        seat = random.choice(["Vertex", "Prism", "Solon"])
    elif trend > 0.05:
        seat = random.choice(["Lumen", "Ripple"])
    else:
        seat = random.choice(COUNCIL_SEATS)
    line = random.choice(COUNCIL_VOICES[seat])
    COUNCIL["messages"].append({
        "seat": seat,
        "text": line,
        "birth": now,
    })
    if len(COUNCIL["messages"]) > 3:
        COUNCIL["messages"].pop(0)
    COUNCIL["next_speak_at"] = now + random.uniform(3.5, 6.0)

# ---------- layout ----------

# Network diagram zone (top ~70% of screen)
NET_TOP    = int(H * 0.10)
NET_BOTTOM = int(H * 0.62)
NET_LEFT   = int(W * 0.08)
NET_RIGHT  = int(W * 0.92)

# Council zone (bottom ~30%)
COUNCIL_Y  = int(H * 0.80)

# Loss chart zone (right side of network area)
CHART_LEFT = int(W * 0.62)
CHART_TOP  = int(H * 0.66)
CHART_RIGHT= int(W * 0.94)
CHART_BOT  = int(H * 0.76)

def layer_x(count, which):
    """Evenly space `count` nodes across the network area."""
    x0 = NET_LEFT
    x1 = NET_RIGHT
    if which == 0:  # input layer
        return x0
    if which == 1:  # hidden layer
        return x0 + (x1 - x0) * 0.45
    return x1 - W * 0.02

def layer_y(index, count):
    span = NET_BOTTOM - NET_TOP
    if count == 1:
        return NET_TOP + span * 0.5
    return NET_TOP + span * (index + 0.5) / count

# ---------- rendering ----------

def draw_connections():
    # W1 — input to hidden
    for i in range(N_IN):
        x0 = layer_x(N_IN, 0) + W * 0.016
        y0 = layer_y(i, N_IN)
        for j in range(N_HID):
            x1 = layer_x(N_HID, 1) - W * 0.016
            y1 = layer_y(j, N_HID)
            w = W1[i][j]
            a = clamp(abs(w), 0.0, 1.0)
            if a < 0.05: continue
            col = LINE_POS if w > 0 else LINE_NEG
            width = max(1, int(a * 3))
            canvas.create_line(x0, y0, x1, y1,
                               fill=col, width=width, tags="net")
    # W2 — hidden to output
    for j in range(N_HID):
        x0 = layer_x(N_HID, 1) + W * 0.016
        y0 = layer_y(j, N_HID)
        x1 = layer_x(N_OUT, 2) - W * 0.016
        y1 = layer_y(0, N_OUT)
        w = W2[j]
        a = clamp(abs(w), 0.0, 1.0)
        if a < 0.05: continue
        col = LINE_POS if w > 0 else LINE_NEG
        width = max(1, int(a * 4))
        canvas.create_line(x0, y0, x1, y1,
                           fill=col, width=width, tags="net")

def draw_nodes():
    r_in = min(W, H) * 0.026
    # input layer
    for i in range(N_IN):
        cx = layer_x(N_IN, 0)
        cy = layer_y(i, N_IN)
        canvas.create_oval(cx - r_in, cy - r_in,
                           cx + r_in, cy + r_in,
                           fill=NODE_BASE, outline=TEXT_DIM,
                           width=1, tags="net")
        canvas.create_text(cx, cy - r_in*1.6,
                           text=["screen", "touch", "hour"][i],
                           fill=TEXT_DIM,
                           font=font_px(H * 0.014), tags="net")
    # hidden
    r_hid = min(W, H) * 0.024
    for j in range(N_HID):
        cx = layer_x(N_HID, 1)
        cy = layer_y(j, N_HID)
        canvas.create_oval(cx - r_hid, cy - r_hid,
                           cx + r_hid, cy + r_hid,
                           fill=NODE_BASE, outline=TEXT_DIM,
                           width=1, tags="net")
        canvas.create_text(cx, cy,
                           text="h%d" % (j + 1),
                           fill=TEXT_DIM,
                           font=font_px(H * 0.013), tags="net")
    # output
    r_out = min(W, H) * 0.034
    cx = layer_x(N_OUT, 2)
    cy = layer_y(0, N_OUT)
    v = STATE["visitor_present"]
    out_fill = NODE_OUT
    # colour the output by its current value
    if v > 0.5:
        out_fill = NODE_LIT
    canvas.create_oval(cx - r_out, cy - r_out,
                       cx + r_out, cy + r_out,
                       fill=out_fill, outline=TEXT_DIM,
                       width=1, tags="net")
    canvas.create_text(cx, cy,
                       text="%.2f" % v,
                       fill=TEXT_LIT,
                       font=font_px(H * 0.020, bold=True),
                       tags="net")
    canvas.create_text(cx, cy - r_out*1.6,
                       text="visitor present",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.014), tags="net")

def draw_labels():
    canvas.create_text(W * 0.5, H * 0.035,
                       text="Edencell — v1",
                       fill=TEXT_LIT,
                       font=font_px(H * 0.026, bold=True), tags="net")
    canvas.create_text(W * 0.5, H * 0.062,
                       text="a single neuron, learning in front of you",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.014), tags="net")

def draw_stats():
    # left block: epoch, loss, accuracy
    x = W * 0.06
    y = H * 0.66
    acc = 0.0
    if STATE["total"] > 0:
        acc = STATE["correct"] / STATE["total"] * 100.0
    canvas.create_text(x, y,
                       text="epoch", anchor="w",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.014), tags="net")
    canvas.create_text(x + W * 0.16, y,
                       text="%d" % STATE["epoch"], anchor="e",
                       fill=TEXT_LIT,
                       font=font_px(H * 0.018, bold=True), tags="net")
    canvas.create_text(x, y + H * 0.03,
                       text="loss", anchor="w",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.014), tags="net")
    canvas.create_text(x + W * 0.16, y + H * 0.03,
                       text="%.3f" % STATE["loss"], anchor="e",
                       fill=TEXT_LIT,
                       font=font_px(H * 0.018, bold=True), tags="net")
    canvas.create_text(x, y + H * 0.06,
                       text="accuracy", anchor="w",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.014), tags="net")
    canvas.create_text(x + W * 0.16, y + H * 0.06,
                       text="%.1f%%" % acc, anchor="e",
                       fill=TEXT_LIT,
                       font=font_px(H * 0.018, bold=True), tags="net")

def draw_chart():
    # frame
    canvas.create_rectangle(CHART_LEFT, CHART_TOP,
                            CHART_RIGHT, CHART_BOT,
                            outline=GRID, width=1, tags="net")
    canvas.create_text((CHART_LEFT + CHART_RIGHT) / 2,
                       CHART_TOP - H * 0.014,
                       text="loss over time",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.013), tags="net")
    hist = STATE["loss_hist"]
    if len(hist) < 2: return
    # keep last 120 points
    data = hist[-120:]
    n = len(data)
    span = CHART_BOT - CHART_TOP
    width = CHART_RIGHT - CHART_LEFT
    max_loss = 1.0
    pts = []
    for i, v in enumerate(data):
        x = CHART_LEFT + width * (i / max(1, n - 1))
        y = CHART_BOT - span * clamp(v / max_loss, 0.0, 1.0)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        canvas.create_line(pts[i][0], pts[i][1],
                           pts[i + 1][0], pts[i + 1][1],
                           fill=LOSS_COL, width=2, tags="net")

def draw_creature(cx, cy, scale, kind, lit):
    """Small flat silhouette. `lit` brightens the rim."""
    col = "#1a2848"
    rim = "#ffb060" if lit > 0.3 else "#5a3020"
    if kind == "turtle":
        pts = [(cx-1.0*scale, cy+0.1*scale),
               (cx-0.7*scale, cy-0.4*scale),
               (cx+0.3*scale, cy-0.5*scale),
               (cx+0.9*scale, cy-0.1*scale),
               (cx+0.8*scale, cy+0.28*scale),
               (cx-0.8*scale, cy+0.3*scale)]
        canvas.create_polygon(*[p for pt in pts for p in pt],
                              fill=col, outline=rim, width=1, tags="council")
    elif kind == "jelly":
        pts = [(cx-0.8*scale, cy+0.1*scale),
               (cx-0.6*scale, cy-0.5*scale),
               (cx+0.6*scale, cy-0.5*scale),
               (cx+0.8*scale, cy+0.1*scale)]
        canvas.create_polygon(*[p for pt in pts for p in pt],
                              fill=col, outline=rim, width=1, tags="council")
        for k in range(5):
            xx = cx + (k-2)*0.3*scale
            canvas.create_line(xx, cy+0.1*scale,
                               xx, cy+0.7*scale,
                               fill=rim, width=1, tags="council")
    elif kind == "crab":
        canvas.create_oval(cx-0.8*scale, cy-0.4*scale,
                           cx+0.8*scale, cy+0.35*scale,
                           fill=col, outline=rim, width=1, tags="council")
        for side in (-1, 1):
            for i in range(3):
                bx = cx + side*(0.4+i*0.14)*scale
                by = cy + 0.05*scale
                tx = bx + side*0.35*scale
                ty = by + 0.35*scale
                canvas.create_line(bx, by, tx, ty,
                                   fill=rim, width=1, tags="council")
    elif kind == "ray":
        pts = [(cx-1.1*scale, cy+0.1*scale),
               (cx-0.4*scale, cy-0.55*scale),
               (cx+0.4*scale, cy-0.55*scale),
               (cx+1.1*scale, cy+0.1*scale),
               (cx+0.4*scale, cy+0.5*scale),
               (cx-0.4*scale, cy+0.5*scale)]
        canvas.create_polygon(*[p for pt in pts for p in pt],
                              fill=col, outline=rim, width=1, tags="council")
        canvas.create_line(cx, cy+0.5*scale,
                           cx, cy+1.0*scale,
                           fill=rim, width=1, tags="council")
    else:  # seahorse
        pts = [(cx-0.25*scale, cy-0.7*scale),
               (cx+0.05*scale, cy-0.85*scale),
               (cx+0.3*scale, cy-0.5*scale),
               (cx+0.2*scale, cy-0.1*scale),
               (cx-0.05*scale, cy+0.35*scale),
               (cx-0.25*scale, cy+0.8*scale),
               (cx+0.05*scale, cy+0.85*scale),
               (cx+0.2*scale, cy+0.5*scale),
               (cx+0.1*scale, cy+0.1*scale)]
        canvas.create_polygon(*[p for pt in pts for p in pt],
                              fill=col, outline=rim, width=1, tags="council")

def draw_council():
    now = time.time()
    spacing = W / 5.5
    kind_map = {"Solon":"turtle", "Lumen":"jelly", "Vertex":"crab",
                "Prism":"ray", "Ripple":"seahorse"}
    for i, seat in enumerate(COUNCIL_SEATS):
        cx = spacing * (i + 0.75)
        cy = COUNCIL_Y
        # lit if the seat is currently speaking
        lit = 0.0
        for m in COUNCIL["messages"]:
            if m["seat"] == seat:
                age = now - m["birth"]
                lit = max(lit, clamp(1.0 - age / 3.5, 0.0, 1.0))
        scale = min(W, H) * 0.028
        draw_creature(cx, cy, scale, kind_map[seat], lit)
        canvas.create_text(cx, cy + scale * 2.0,
                           text=seat,
                           fill=TEXT_LIT if lit > 0.3 else TEXT_DIM,
                           font=font_px(H * 0.013), tags="council")
    # speech lines
    for i, m in enumerate(COUNCIL["messages"]):
        age = time.time() - m["birth"]
        if age > 4.5: continue
        alpha = clamp(1.0 - age / 4.5, 0.0, 1.0)
        # fade by lerping toward BG
        def fade(c1):
            h1 = c1.lstrip("#")
            r = int(h1[0:2], 16); g = int(h1[2:4], 16); b = int(h1[4:6], 16)
            hb = BG.lstrip("#")
            rb = int(hb[0:2], 16); gb = int(hb[2:4], 16); bb = int(hb[4:6], 16)
            return "#%02x%02x%02x" % (
                int(rb + (r - rb) * alpha),
                int(gb + (g - gb) * alpha),
                int(bb + (b - bb) * alpha))
        col = fade(TEXT_LIT)
        y = COUNCIL_Y - H * 0.10 - i * H * 0.030
        canvas.create_text(W * 0.5, y,
                           text="%s: %s" % (m["seat"], m["text"]),
                           fill=col,
                           font=font_px(H * 0.017, bold=True),
                           tags="council")

# ---------- main tick ----------

LAST = [time.time()]

def tick():
    now = time.time()
    dt = now - LAST[0]; LAST[0] = now

    # training — several steps per frame
    if not STATE["paused"]:
        for _ in range(6):
            l = train_step()
            STATE["epoch"] += 1
            STATE["loss"] = STATE["loss"] * 0.98 + l * 0.02
        STATE["loss_hist"].append(STATE["loss"])
        if len(STATE["loss_hist"]) > 500:
            STATE["loss_hist"] = STATE["loss_hist"][-500:]
        STATE["epochs_since_report"] += 1

    # council notices
    maybe_council_speak(now)

    # render
    canvas.delete("net")
    canvas.delete("council")
    draw_labels()
    draw_connections()
    draw_nodes()
    draw_stats()
    draw_chart()
    draw_council()

    # top strip — a quiet instruction
    canvas.create_text(W * 0.5, H * 0.985,
                       text="tap to pause / resume",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.013), tags="net")

    root.after(60, tick)

def on_tap(e):
    STATE["paused"] = not STATE["paused"]

canvas.bind("<Button-1>", on_tap)

tick()
root.mainloop()

# ============ END EDENCELL V1 ============