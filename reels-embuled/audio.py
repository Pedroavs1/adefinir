# Trilha + efeitos sintetizados (WAV 44.1 kHz estéreo), sincronizados com timeline.py.
# Uso: python3 audio.py saida.wav
import sys
import numpy as np
from scipy.signal import butter, sosfilt
from timeline import *

SR = 44100
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(7)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * np.sqrt((1 - pan) / 2)
    R[i:i + len(sig)] += sig * gain * np.sqrt((1 + pan) / 2)


def tt(d):
    return np.arange(int(d * SR)) / SR


def lp(x, f, o=2):
    return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)


# ---------- instrumentos ----------
def kick():
    t = tt(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2.2 * np.sin(ph) * np.exp(-t * 7)) * 0.9 + hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300) * 0.25


def clap():
    t = tt(0.3)
    env = np.zeros(len(t))
    for k, d in enumerate([0, 0.011, 0.022]):
        i = int(d * SR)
        env[i:] += np.exp(-(t[: len(t) - i]) * (90 if k < 2 else 22))
    return bp(rng.standard_normal(len(t)), 900, 4000) * env * 0.55


def hat(open_=False):
    t = tt(0.25 if open_ else 0.06)
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * (14 if open_ else 70)) * 0.22


def saw(f, d):
    t = tt(d)
    return 2 * ((t * f) % 1) - 1


def stab(freqs, d=0.32):
    t = tt(d)
    s = sum(saw(f, d) + saw(f * 1.006, d) for f in freqs) / (2 * len(freqs))
    s = lp(s, 2600)
    return s * np.exp(-t * 6) * 0.45


def sub(f, d):
    t = tt(d)
    env = np.minimum(1, t / 0.005) * np.minimum(1, (d - t) / 0.03)
    return np.tanh(1.6 * np.sin(2 * np.pi * f * t)) * env * 0.5


# ---------- efeitos ----------
def impacto(d=1.8, big=1.0):
    t = tt(d)
    f = 30 + 140 * np.exp(-t * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    boom = np.tanh(3 * np.sin(ph)) * np.exp(-t * 2.6)
    crack = lp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 18)
    tail = lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 3) * 0.4
    return (boom * 0.9 + crack * 0.45 + tail) * big


def led(d=1.15):
    t = tt(d)
    buzz = np.sign(np.sin(2 * np.pi * 120 * t)) * 0.3 + np.sin(2 * np.pi * 240 * t) * 0.2
    buzz = lp(buzz, 3000)
    gate = np.zeros(len(t))
    # liga-desliga irregular e depois fica aceso
    for a, b in [(0.0, 0.06), (0.14, 0.18), (0.3, 0.42), (0.5, 0.53), (0.62, d)]:
        gate[int(a * SR):int(b * SR)] = 1
    click = np.zeros(len(t))
    for a in [0.0, 0.14, 0.3, 0.5, 0.62]:
        i = int(a * SR)
        click[i:i + 300] += hp(rng.standard_normal(300), 2000) * np.exp(-np.arange(300) / 40)
    return buzz * lp(gate, 200) * 0.5 + click * 0.6


def swoosh(d=0.5):
    t = tt(d)
    x = rng.standard_normal(len(t))
    out = np.zeros(len(t))
    seg = 512
    for i in range(0, len(t), seg):
        p = i / len(t)
        fc = 400 + 5000 * np.sin(np.pi * p) ** 2
        out[i:i + seg] = bp(x[i:i + seg + 0], max(100, fc * 0.6), min(18000, fc * 1.6), 1)[: len(out[i:i + seg])]
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return lp(out, 9000) * env * 0.9


def riser(d=1.2):
    t = tt(d)
    noise = hp(rng.standard_normal(len(t)), 1500) * (t / d) ** 2
    f = 200 * (8 ** (t / d))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) * 0.3 * (t / d) ** 1.5
    return (noise * 0.35 + tone)


def carimbo():
    t = tt(0.35)
    thump = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 18)
    slap = bp(rng.standard_normal(len(t)), 300, 3000) * np.exp(-t * 45)
    return thump * 0.9 + slap * 0.6


def blip(f):
    t = tt(0.035)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 90) * 0.35


def chime():
    t = tt(1.4)
    s = np.zeros(len(t))
    for i, (f, dt) in enumerate([(1318.5, 0), (1975.5, 0.09)]):
        k = int(dt * SR)
        tk = t[: len(t) - k]
        tone = np.sin(2 * np.pi * f * tk) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tk) * np.exp(-tk * 6)
        s[k:] += tone * np.exp(-tk * 3.5)
    return s * 0.35


# ---------- trilha (lá menor: Am F C G) ----------
prog = [(55.0, [220, 261.6, 329.6]), (43.65, [174.6, 220, 261.6]),
        (65.41, [261.6, 329.6, 392.0]), (49.0, [196.0, 246.9, 293.7])]
n_beats = int((T_FINAL - T0) / BEAT + 0.5)
for b in range(n_beats):
    tb = beat(b)
    breakdown = beat(19) <= tb < T_POR   # respiro antes do preço cravar
    bar = (b // 4) % 4
    root, chord = prog[bar]
    if not breakdown:
        add(kick(), tb, 0.9)
        add(sub(root, BEAT * 0.9), tb + BEAT * 0.5, 0.8)
    if b % 2 == 1 and not breakdown:
        add(clap(), tb, 0.7)
    add(hat(), tb + BEAT * 0.5, 0.8, pan=0.3)
    add(hat(), tb + BEAT * 0.75, 0.4, pan=-0.3)
    if b % 4 in (0, 1) or breakdown:
        add(stab(chord), tb + (BEAT * 0.75 if b % 4 == 1 else 0), 0.6 if not breakdown else 0.4, pan=-0.2)

# riser do respiro até o preço
add(riser(T_POR - beat(19)), beat(19), 0.6)

# ---------- efeitos na linha do tempo ----------
add(led(), 0.05, 0.9)
add(riser(T_BLACK - 0.1), 0.1, 0.35)
add(impacto(2.2, 1.0), T_BLACK, 1.0)
for tc in (T_FOTO1, T_FOTO2, T_FOTO3, T_PRECO):
    add(swoosh(0.5), tc - 0.3, 0.8, pan=0.0)
add(carimbo(), T_RISCO, 1.0)
# contador descendo: blips acelerando
tcur, k = T_CONT0, 0
while tcur < T_POR - 0.03:
    add(blip(1800 + 400 * (k % 3)), tcur, 0.7, pan=(-0.3 if k % 2 else 0.3))
    k += 1
    tcur += 0.075 - 0.04 * (tcur - T_CONT0) / (T_POR - T_CONT0)
add(impacto(1.6, 0.85), T_POR, 1.0)
add(chime(), T_POR + 0.02, 1.0)
add(carimbo(), T_SELO, 0.6)
add(chime(), T_SELO, 0.4)
add(riser(T_FINAL - beat(25)), beat(25), 0.5)
add(swoosh(0.5), T_FINAL - 0.3, 0.8)
add(impacto(2.4, 1.1), T_FINAL, 1.0)
add(chime(), T_FINAL + 0.05, 0.5)

# ---------- master ----------
mix = np.stack([L, R], 1)
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
fade = np.minimum(1, (N - np.arange(N)) / (SR * 0.5))[:, None]
mix *= fade
mix /= np.max(np.abs(mix)) / 0.89
import wave
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('audio ok')
