"""Sound design for AuraGap. Every time comes from src/aura/timeline.json.

    python3 -m sfx sfx/cues/aura_gap.py

Key: A minor. The bed darkens to Fmaj7 when the gap is marked and resolves
to A major on the logo ring. One impact only: the crack in "مكسور".
"""

from sfx.synth import blip, chime, click, envelope, impact, pad, pop, riser, scratch, whoosh

TIMELINE = "src/aura/timeline.json"
OUT = "public/aura-sfx.wav"
TARGET_LUFS = -14.0

BED_MIN = [110.0, 164.81, 220.0, 261.63, 493.88]  # Am(add9)
BED_GAP = [87.31, 130.81, 220.0, 329.63]  # Fmaj7: the tension under the gap
BED_RES = [110.0, 164.81, 277.18, 329.63, 493.88]  # A(add9): resolution on the logo
NODE_NOTES = [880.0, 1046.5, 1318.5, 1174.66, 987.77]  # rises to trust, falls after the break
BAR_NOTES = [1318.5, 1046.5, 880.0, 659.25, 523.25]  # the funnel narrows, the pitch drops


def bezier(x1, y1, x2, y2):
    """Same cubic-bezier easing the picture uses (Remotion Easing.bezier)."""
    def at(a1, a2, s):
        return 3 * a1 * s * (1 - s) ** 2 + 3 * a2 * s * s * (1 - s) + s ** 3

    def ease(x):
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if at(x1, x2, mid) < x:
                lo = mid
            else:
                hi = mid
        return at(y1, y2, (lo + hi) / 2)

    return ease


EXPO_OUT = bezier(0.16, 1, 0.3, 1)
EXPO_IN_OUT = bezier(0.87, 0, 0.13, 1)


def crossing(t0, t1, ease, level):
    """First time in [t0, t1] where ease((t - t0) / (t1 - t0)) reaches level."""
    steps = 600
    for k in range(steps + 1):
        if ease(k / steps) >= level:
            return t0 + (t1 - t0) * k / steps
    return t1


def score(mix, tl):
    s1, s2, s3, s4, s5 = tl["s1"], tl["s2"], tl["s3"], tl["s4"], tl["s5"]
    dur = tl["duration"]
    put = mix.put

    # bed: in after the first line, ducked under the crack, out with the fade to black
    crack = s1["crack"]
    volume = envelope([
        (0, 0), (1.2, 0.8), (crack, 0.8), (crack + 0.15, 0.25), (s2["draw"], 0.25),
        (s2["drawEnd"], 1), (s4["exit"], 1), (s5["ring"], 0.6), (s5["ring"] + 0.8, 1.2),
        (s5["fadeOut"], 1.2), (dur, 0),
    ])
    chords = [(0, BED_MIN), (s3["gap"], BED_GAP), (s4["sweepEnd"], BED_MIN), (s5["ring"] + 0.8, BED_RES)]
    mix.put_stereo(0, *pad(dur, chords, volume=volume), gain=0.03)

    # scene 1: words snap in, gold flash, the crack
    for i, w in enumerate(s1["words1"]):
        put(w, whoosh(0.18, 700, 3000, peak=0.2), 0.08, 0.3 - i * 0.3)
        put(w, click(1500 + i * 150, dur=0.04), 0.16, 0.3 - i * 0.3)
        put(w + 0.01, blip(110 * (1, 1.2, 1.5)[i], dur=0.35, tau=0.1), 0.2)
    put(s1["flash"] - 0.12, whoosh(0.14, 600, 6000, peak=0.9, q=0.6), 0.18)
    put(s1["flash"], click(3200, dur=0.03), 0.26)
    put(s1["flash"], blip(220, dur=0.25, tau=0.06), 0.16)
    for i, w in enumerate(s1["words2"]):
        put(w, click(1700 - i * 200, dur=0.04), 0.16, 0.3 - i * 0.3)
        put(w + 0.01, blip((146.83, 130.81, 110.0)[i], dur=0.4, tau=0.12), 0.22)
    put(crack - 0.01, impact(), 0.32)
    put(crack, scratch(0.25), 0.2, -0.1)
    put(crack + 0.005, blip(116.54, dur=0.6, tau=0.2), 0.1)  # Bb against the A: it hurts a little
    put(s1["exit"], whoosh(0.3, 400, 3800, peak=0.7), 0.14, 0.7)
    put(s1["exit"], whoosh(0.3, 400, 3800, peak=0.7), 0.14, -0.7)

    # scene 2: the path draws right to left, nodes pop, the line breaks at trust
    put(s2["draw"], whoosh(s2["drawEnd"] - s2["draw"], 300, 1600, peak=0.5, q=0.6), 0.1, 0.2)
    put(s2["draw"] + 0.05, scratch(s2["drawEnd"] - s2["draw"] - 0.1), 0.05)
    for i in range(5):
        t = crossing(s2["draw"], s2["drawEnd"], EXPO_IN_OUT, i / 4)
        pan = 0.6 - i * 0.3  # right to left, like the reading order
        put(t, pop(NODE_NOTES[i] * 1.1, NODE_NOTES[i] * 0.55), 0.2, pan)
        put(t + 0.005, blip(NODE_NOTES[i] / 2, dur=0.35, tau=0.1), 0.08, pan)
    brk = s2["break"]
    put(brk, scratch(0.2), 0.18)
    put(brk, blip(110.0, dur=0.8, tau=0.3), 0.22)
    put(brk, blip(116.54, dur=0.8, tau=0.3), 0.16)
    for k in range(3):  # one tick per shake cycle
        put(brk + k * 0.167, click(900 - k * 120, dur=0.03), 0.1, (-0.2, 0.2, -0.1)[k])
    put(s2["toBars"], whoosh(0.6, 2400, 600, peak=0.5), 0.14, 0.4)

    # scene 3: bars grow from the right, numbers count, the gap gets marked
    put(s3["label"], whoosh(0.4, 500, 2600, peak=0.35), 0.08)
    put(s3["label"] + 0.15, blip(220.0, dur=0.4, tau=0.12), 0.12)
    for i in range(5):
        t = s3["bars"] + i * 0.15
        put(t, pop(BAR_NOTES[i], BAR_NOTES[i] * 0.5), 0.16, 0.5)
    for k in range(1, 13):  # counter ticks, fast then settling, like the count-up
        t = crossing(s3["count"], s3["count"] + 1.4, EXPO_OUT, k / 13)
        put(t, click(2600 - k * 60, dur=0.02), 0.06, 0.1)
    gap = s3["gap"]
    put(gap, scratch(0.4), 0.16, -0.3)
    put(gap, blip(87.31, dur=1.0, tau=0.4), 0.22)
    put(gap + 0.25, pop(700, 300), 0.18, -0.4)
    put(gap + 0.25, blip(311.13, dur=0.5, tau=0.15), 0.08, -0.4)  # Eb: the tritone of the key
    for i in range(5):
        put(s3["exit"] + i * 0.04, whoosh(0.3, 2800, 700, peak=0.4), 0.05, 0.5)

    # scene 4: the bracket becomes the glass, the glass reveals the truth
    put(s4["morph"], whoosh(s4["morphEnd"] - s4["morph"], 300, 2200, peak=0.6, q=0.7), 0.16, 0.4)
    put(s4["morphEnd"], click(2200, dur=0.04), 0.14, 0.6)
    put(s4["morphEnd"], blip(440.0, dur=0.5, tau=0.15), 0.1, 0.6)
    sweep = s4["sweepEnd"] - s4["sweep"]
    for k, pan in enumerate((0.6, 0.2, -0.2, -0.6)):  # the glass travels right to left
        put(s4["sweep"] + k * sweep / 4, whoosh(sweep / 4 + 0.1, 900, 1500, peak=0.5, q=1.2), 0.07, pan)
    put(s4["sweepEnd"] - 0.05, chime([440.0, 523.25, 659.25, 987.77], dur=2.0, tau=0.7), 0.16)
    put(s4["sweepEnd"] + 0.1, whoosh(0.65, 1600, 500, peak=0.4), 0.06)
    put(s4["exit"], whoosh(0.3, 2200, 600, peak=0.3), 0.1)

    # scene 5: glass to dot, the ring draws, the name lands, the CTA
    put(s4["exit"] + 0.25, riser(s5["ring"] - s4["exit"] - 0.25, 400, 4200), 0.16)
    put(s5["shrink"], whoosh(s5["dot"] - s5["shrink"], 2400, 300, peak=0.8), 0.12)
    put(s5["dot"], pop(1600, 900), 0.18)
    put(s5["ring"], click(2400, dur=0.04), 0.2)
    for k, pan in enumerate((0.4, 0.6, -0.2, -0.6)):  # pen travels clockwise around the ring
        put(s5["ring"] + k * 0.2, whoosh(0.25, 800, 2200, peak=0.5), 0.07, pan)
    put(s5["ring"] + 0.8, chime([440.0, 554.37, 659.25, 830.61, 987.77], dur=2.4, tau=0.9), 0.2)
    put(s5["type"], whoosh(s5["typeEnd"] - s5["type"], 4000, 900, peak=0.2, q=0.5), 0.06)
    for i in range(7):  # one soft tick per letter as the spacing tightens
        put(s5["type"] + 0.05 + i * 0.06, click(2800 - i * 80, dur=0.02), 0.05, -0.45 + i * 0.15)
    put(s5["cta"], pop(1046.5, 520), 0.16)
    put(s5["cta"] + 0.01, blip(440.0, dur=0.6, tau=0.2), 0.12)
