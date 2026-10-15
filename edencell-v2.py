# ============ EDENCELL — V2 ============
# A council of five small networks.
# Each seat learns something different. Trained live.
# =======================================

import tkinter as tk, math, random, time

root = tk.Tk()
root.title("Edencell — v2")
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
    return ("Helvetica", -max(9, int(px)), "bold" if bold else "normal")

def clamp(v, lo, hi): return max(lo, min(hi, v))

# ---------- colours ----------
BG       = "#0a0208"
TEXT_DIM = "#7a6878"
TEXT_LIT = "#e0d0e0"
LINE_POS = "#80ffe0"
LINE_NEG = "#ff80b8"
NODE_IN  = "#1a2848"
NODE_OUT = "#3a1858"

# per-seat accent
SEAT_COL = {
    "Solon":  "#ffb060",
    "Lumen":  "#c0a0ff",
    "Vertex": "#5fd08a",
    "Prism":  "#ffc857",
    "Ripple": "#ff7ea8",
}

SEATS = ["Solon", "Lumen", "Vertex", "Prism", "Ripple"]

# ---------- small network ----------
# 2 inputs → 2 hidden → 1 output. All sigmoid.
N_IN, N_HID, N_OUT = 2, 2, 1

def sigmoid(x):
    if x < -60: return 0.0
    if x >  60: return 1.0
    return 1.0 / (1.0 + math.exp(-x))

class SmallNet:
    def __init__(self, seed):
        rng = random.Random(seed)
        self.W1 = [[rng.uniform(-0.8, 0.8) for _ in range(N_HID)]
                   for _ in range(N_IN)]
        self.B1 = [0.0] * N_HID
        self.W2 = [rng.uniform(-0.8, 0.8) for _ in range(N_HID)]
        self.B2 = 0.0
        self.lr = 0.6
        self.loss = 1.0
        self.loss_hist = []
        self.epoch = 0
        self.correct = 0
        self.total = 0
        self.last_out = 0.0

    def forward(self, x):
        h = []
        for j in range(N_HID):
            z = self.B1[j]
            for i in range(N_IN):
                z += x[i] * self.W1[i][j]
            h.append(sigmoid(z))
        z2 = self.B2
        for j in range(N_HID):
            z2 += h[j] * self.W2[j]
        return h, sigmoid(z2)

    def step(self, x, y):
        h, o = self.forward(x)
        d_out = (o - y) * o * (1 - o)
        d_hid = [d_out * self.W2[j] * h[j] * (1 - h[j])
                 for j in range(N_HID)]
        for j in range(N_HID):
            self.W2[j] -= self.lr * d_out * h[j]
        self.B2 -= self.lr * d_out
        for i in range(N_IN):
            for j in range(N_HID):
                self.W1[i][j] -= self.lr * d_hid[j] * x[i]
        for j in range(N_HID):
            self.B1[j] -= self.lr * d_hid[j]
        # score
        pred = 1 if o > 0.5 else 0
        self.correct += 1 if pred == y else 0
        self.total += 1
        self.last_out = o
        return (o - y) ** 2

# ---------- the five problems ----------
# Each creature learns a rule it can never be told. Only examples.
# Rules chosen to reflect each register.

def rule_solon(x):
    # is the chamber open?  screen on OR recent session
    screen, recent = x
    return 1 if (screen or recent) else 0

def rule_lumen(x):
    # is something odd?  exactly one of the two signals
    touch, focus = x
    return 1 if (touch != focus) else 0

def rule_vertex(x):
    # good to continue?  battery high AND not late
    battery_hi, hour_ok = x
    return 1 if (battery_hi and hour_ok) else 0

def rule_prism(x):
    # pattern holds?  same hour AND visitor present
    same_hour, present = x
    return 1 if (same_hour and present) else 0

def rule_ripple(x):
    # all well?  visitor present AND quiet
    present, quiet = x
    return 1 if (present and quiet) else 0

RULE = {
    "Solon":  rule_solon,
    "Lumen":  rule_lumen,
    "Vertex": rule_vertex,
    "Prism":  rule_prism,
    "Ripple": rule_ripple,
}

NETS = {s: SmallNet(seed=hash(s) & 0xffff) for s in SEATS}

# ---------- voices ----------
VOICES = {
    "Solon":  {"rising": ["Something is wrong.", "Noted."],
               "falling": ["Chamber is open.", "Continuing."],
               "flat": ["Still working."]},
    "Lumen":  {"rising": ["Is that right?", "I don't know."],
               "falling": ["Oh. I see.", "Closer."],
               "flat": ["Hm."]},
    "Vertex": {"rising": ["Numbers off.", "Rechecking."],
               "falling": ["Readings good.", "Holding."],
               "flat": ["Watching."]},
    "Prism":  {"rising": ["Not the shape.", "Almost."],
               "falling": ["Pattern forming.", "There it is."],
               "flat": ["Every cycle."]},
    "Ripple": {"rising": ["It's alright.", "Take your time."],
               "falling": ["That's better.", "There."],
               "flat": ["I'm here."]},
}

VOICE = {s: {"text": "", "until": 0.0} for s in SEATS}
NEXT_SPEAK = {s: time.time() + random.uniform(2.0, 5.0) for s in SEATS}

def maybe_speak(seat, now):
    if now < NEXT_SPEAK[seat]: return
    hist = NETS[seat].loss_hist
    if len(hist) < 6:
        trend = "flat"
    else:
        d = hist[-1] - hist[-6]
        if d < -0.02: trend = "falling"
        elif d > 0.02: trend = "rising"
        else: trend = "flat"
    line = random.choice(VOICES[seat][trend])
    VOICE[seat]["text"] = line
    VOICE[seat]["until"] = now + random.uniform(3.0, 5.0)
    NEXT_SPEAK[seat] = now + random.uniform(4.0, 8.0)

# ---------- layout ----------
TITLE_Y   = H * 0.035
SUBTITLE_Y= H * 0.062

COUNCIL_Y = H * 0.12      # creature row
NET_TOP   = H * 0.22
NET_BOT   = H * 0.62
NAMES_Y   = H * 0.68
STATS_Y   = H * 0.72
VOICE_Y   = H * 0.78

CHART_LEFT = W * 0.08
CHART_RIGHT= W * 0.92
CHART_TOP  = H * 0.84
CHART_BOT  = H * 0.95

def col_center(i):
    return W * (i + 0.5) / len(SEATS)

# ---------- draw creatures (small, from Edenshore) ----------

def draw_creature(cx, cy, scale, seat, lit):
    col = "#1a2848"
    base_rim = SEAT_COL[seat]
    # lit 0..1 brightens the rim
    rim = base_rim
    if lit < 0.05:
        # dim the rim
        rim = "#3a2a3a"
    if seat == "Solon":
        pts = [(cx-1.0*scale, cy+0.1*scale),
               (cx-0.7*scale, cy-0.4*scale),
               (cx+0.3*scale, cy-0.5*scale),
               (cx+0.9*scale, cy-0.1*scale),
               (cx+0.8*scale, cy+0.28*scale),
               (cx-0.8*scale, cy+0.30*scale)]
        canvas.create_polygon(*[p for pt in pts for p in pt],
                              fill=col, outline=rim, width=1, tags="c")
    elif seat == "Lumen":
        pts = [(cx-0.8*scale, cy+0.1*scale),
               (cx-0.6*scale, cy-0.5*scale),
               (cx+0.6*scale, cy-0.5*scale),
               (cx+0.8*scale, cy+0.1*scale)]
        canvas.create_polygon(*[p for pt in pts for p in pt],
                              fill=col, outline=rim, width=1, tags="c")
        for k in range(4):
            xx = cx + (k-1.5)*0.3*scale
            canvas.create_line(xx, cy+0.1*scale,
                               xx, cy+0.7*scale,
                               fill=rim, width=1, tags="c")
    elif seat == "Vertex":
        canvas.create_oval(cx-0.8*scale, cy-0.4*scale,
                           cx+0.8*scale, cy+0.35*scale,
                           fill=col, outline=rim, width=1, tags="c")
        for side in (-1, 1):
            for i in range(3):
                bx = cx + side*(0.4+i*0.14)*scale
                by = cy + 0.05*scale
                tx = bx + side*0.35*scale
                ty = by + 0.35*scale
                canvas.create_line(bx, by, tx, ty,
                                   fill=rim, width=1, tags="c")
    elif seat == "Prism":
        pts = [(cx-1.1*scale, cy+0.1*scale),
               (cx-0.4*scale, cy-0.55*scale),
               (cx+0.4*scale, cy-0.55*scale),
               (cx+1.1*scale, cy+0.1*scale),
               (cx+0.4*scale, cy+0.5*scale),
               (cx-0.4*scale, cy+0.5*scale)]
        canvas.create_polygon(*[p for pt in pts for p in pt],
                              fill=col, outline=rim, width=1, tags="c")
        canvas.create_line(cx, cy+0.5*scale, cx, cy+1.0*scale,
                           fill=rim, width=1, tags="c")
    else:  # Ripple
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
                              fill=col, outline=rim, width=1, tags="c")

# ---------- draw each small network ----------

def draw_net(cx, seat):
    net = NETS[seat]
    col_x0 = cx - W * 0.085
    col_x1 = cx + W * 0.085
    x_in   = col_x0 + W * 0.014
    x_hid  = (col_x0 + col_x1) / 2
    x_out  = col_x1 - W * 0.014
    y_in_1 = NET_TOP + (NET_BOT - NET_TOP) * 0.25
    y_in_2 = NET_TOP + (NET_BOT - NET_TOP) * 0.75
    y_h_1  = NET_TOP + (NET_BOT - NET_TOP) * 0.30
    y_h_2  = NET_TOP + (NET_BOT - NET_TOP) * 0.70
    y_out  = (NET_TOP + NET_BOT) / 2

    r_node = min(W, H) * 0.014

    # W1 lines
    for i, (y_i) in enumerate([y_in_1, y_in_2]):
        for j, (y_j) in enumerate([y_h_1, y_h_2]):
            w = net.W1[i][j]
            a = clamp(abs(w), 0.0, 1.0)
            if a < 0.06: continue
            col_line = LINE_POS if w > 0 else LINE_NEG
            canvas.create_line(x_in, y_i, x_hid, y_j,
                               fill=col_line,
                               width=max(1, int(a * 2.4)), tags="c")
    # W2 lines
    for j, (y_j) in enumerate([y_h_1, y_h_2]):
        w = net.W2[j]
        a = clamp(abs(w), 0.0, 1.0)
        if a < 0.06: continue
        col_line = LINE_POS if w > 0 else LINE_NEG
        canvas.create_line(x_hid, y_j, x_out, y_out,
                           fill=col_line,
                           width=max(1, int(a * 3.0)), tags="c")

    # nodes
    for y in [y_in_1, y_in_2]:
        canvas.create_oval(x_in - r_node, y - r_node,
                           x_in + r_node, y + r_node,
                           fill=NODE_IN, outline=TEXT_DIM, width=1,
                           tags="c")
    for y in [y_h_1, y_h_2]:
        canvas.create_oval(x_hid - r_node, y - r_node,
                           x_hid + r_node, y + r_node,
                           fill=NODE_IN, outline=TEXT_DIM, width=1,
                           tags="c")
    # output node — lights up
    lit = net.last_out
    out_fill = NODE_OUT if lit < 0.5 else SEAT_COL[seat]
    r_out = r_node * 1.35
    canvas.create_oval(x_out - r_out, y_out - r_out,
                       x_out + r_out, y_out + r_out,
                       fill=out_fill, outline=TEXT_DIM, width=1,
                       tags="c")
    canvas.create_text(x_out, y_out,
                       text="%.2f" % lit,
                       fill=TEXT_LIT,
                       font=font_px(H * 0.013, bold=True),
                       tags="c")

# ---------- draw whole council column ----------

def draw_column(i, seat, now):
    cx = col_center(i)

    # creature above network
    # lit if it just spoke
    lit = 0.0
    if VOICE[seat]["until"] > now and VOICE[seat]["text"]:
        # fading brightness by remaining time
        remain = VOICE[seat]["until"] - now
        lit = clamp(remain / 5.0, 0.0, 1.0)
    draw_creature(cx, COUNCIL_Y, min(W, H) * 0.020, seat, lit)

    # network diagram
    draw_net(cx, seat)

    # name
    canvas.create_text(cx, NAMES_Y,
                       text=seat,
                       fill=SEAT_COL[seat],
                       font=font_px(H * 0.016, bold=True),
                       tags="c")

    # stats
    net = NETS[seat]
    acc = 0.0
    if net.total > 0:
        acc = net.correct / net.total * 100.0
    canvas.create_text(cx, STATS_Y,
                       text="loss %.3f" % net.loss,
                       fill=TEXT_DIM,
                       font=font_px(H * 0.012),
                       tags="c")
    canvas.create_text(cx, STATS_Y + H * 0.020,
                       text="%d epochs · %.0f%%" % (net.epoch, acc),
                       fill=TEXT_DIM,
                       font=font_px(H * 0.012),
                       tags="c")

def draw_title():
    canvas.create_text(W * 0.5, TITLE_Y,
                       text="Edencell — v2",
                       fill=TEXT_LIT,
                       font=font_px(H * 0.026, bold=True),
                       tags="c")
    canvas.create_text(W * 0.5, SUBTITLE_Y,
                       text="a council of five small networks, learning in front of you",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.013),
                       tags="c")

def draw_voice_lines(now):
    for i, seat in enumerate(SEATS):
        cx = col_center(i)
        if VOICE[seat]["until"] <= now: continue
        if not VOICE[seat]["text"]: continue
        age = (VOICE[seat]["until"] - now)
        # simple alpha by colour fade
        # (alpha in Tk is not supported; use lerp toward BG)
        def fade(hexc, a):
            h1 = hexc.lstrip("#")
            r = int(h1[0:2], 16); g = int(h1[2:4], 16); b = int(h1[4:6], 16)
            hb = BG.lstrip("#")
            rb = int(hb[0:2], 16); gb = int(hb[2:4], 16); bb = int(hb[4:6], 16)
            return "#%02x%02x%02x" % (
                int(rb + (r - rb) * a),
                int(gb + (g - gb) * a),
                int(bb + (b - bb) * a))
        a = clamp(age / 5.0, 0.0, 1.0)
        col = fade(SEAT_COL[seat], a)
        canvas.create_text(cx, VOICE_Y,
                           text='"%s"' % VOICE[seat]["text"],
                           fill=col,
                           font=font_px(H * 0.014, bold=True),
                           tags="c")

def draw_chart():
    canvas.create_rectangle(CHART_LEFT, CHART_TOP,
                            CHART_RIGHT, CHART_BOT,
                            outline="#1a1024", width=1, tags="c")
    canvas.create_text((CHART_LEFT + CHART_RIGHT) / 2,
                       CHART_TOP - H * 0.014,
                       text="loss over time — one line per seat",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.013),
                       tags="c")
    span = CHART_BOT - CHART_TOP
    width = CHART_RIGHT - CHART_LEFT
    for seat in SEATS:
        hist = NETS[seat].loss_hist
        if len(hist) < 2: continue
        data = hist[-200:]
        n = len(data)
        pts = []
        for i, v in enumerate(data):
            x = CHART_LEFT + width * (i / max(1, n - 1))
            y = CHART_BOT - span * clamp(v, 0.0, 1.0)
            pts.append((x, y))
        for i in range(len(pts) - 1):
            canvas.create_line(pts[i][0], pts[i][1],
                               pts[i+1][0], pts[i+1][1],
                               fill=SEAT_COL[seat], width=2, tags="c")

# ---------- training ----------

PAUSED = [False]

def train_all():
    for seat in SEATS:
        net = NETS[seat]
        for _ in range(3):
            x0 = random.randint(0, 1)
            x1 = random.randint(0, 1)
            y  = RULE[seat]([x0, x1])
            l  = net.step([x0, x1], y)
            net.epoch += 1
            net.loss = net.loss * 0.98 + l * 0.02
        net.loss_hist.append(net.loss)
        if len(net.loss_hist) > 400:
            net.loss_hist = net.loss_hist[-400:]

# ---------- main tick ----------

LAST = [time.time()]

def tick():
    now = time.time()
    if not PAUSED[0]:
        train_all()
    for seat in SEATS:
        maybe_speak(seat, now)

    canvas.delete("c")
    draw_title()
    for i, seat in enumerate(SEATS):
        draw_column(i, seat, now)
    draw_voice_lines(now)
    draw_chart()

    canvas.create_text(W * 0.5, H * 0.985,
                       text="tap to pause / resume",
                       fill=TEXT_DIM,
                       font=font_px(H * 0.012),
                       tags="c")

    root.after(80, tick)

def on_tap(e):
    PAUSED[0] = not PAUSED[0]

canvas.bind("<Button-1>", on_tap)

tick()
root.mainloop()

# ============ END EDENCELL V2 ============