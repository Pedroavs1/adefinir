# Mixagem do reels com a trilha e os efeitos da Black Friday (ElevenLabs, pasta audio-bf/).
# A trilha entra com o build e o drop cai em T_BLACK. Efeitos alinhados com timeline.py.
# Uso: python3 audio.py saida.wav
import sys
import wave
import subprocess
import numpy as np
from timeline import *

SR = 44100
N = int(SR * DUR)


def carregar(nome):
    b = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', nome, '-ac', '2', '-ar', str(SR),
                        '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.int16).reshape(-1, 2) / 32768


def sfx(nome):
    return carregar(f'audio-bf/{nome}.mp3')


mix = np.zeros((N, 2))


def add(sig, t, gain=1.0):
    i = int(round(t * SR))
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i]
    mix[i:i + len(sig)] += sig * gain


# ---------- trilha ----------
musica = carregar(MUSICA)
ini = int((DROP_MUSICA - T_BLACK) * SR)
trilha = musica[ini:ini + N].copy()
env = np.ones(N)
t = np.arange(N) / SR
# abre suave, abaixa um pouco no contador pra dar espaço aos efeitos, e sai na cartela final
env *= np.clip(t / 0.15, 0, 1)
duck = (t > T_RISCO - 0.05) & (t < T_POR)
env[duck] *= 0.6
fim = t > T_FINAL + 0.4
env[fim] *= np.clip(1 - (t[fim] - T_FINAL - 0.4) / (DUR - T_FINAL - 0.4), 0, 1)
add(trilha * env[:len(trilha), None], 0, 0.85)

# ---------- efeitos (offsets = onset/pico medidos em cada arquivo) ----------
add(sfx('neon'), 0.10, 0.9)
add(sfx('boom'), T_BLACK - 0.02, 1.0)
for tc in (T_FOTO1, T_FOTO2, T_FOTO3, T_PRECO):
    add(sfx('whoosh'), tc - 0.43, 0.8)          # pico do whoosh no corte
add(sfx('carimbo'), T_RISCO, 0.9)
led = sfx('led-display')
for k in range(3):                               # beeps do contador descendo
    add(led, T_CONT0 + k * BEAT, 0.6)
add(sfx('boom'), T_POR - 0.02, 0.9)
add(sfx('caixa'), T_POR, 0.8)
add(sfx('carimbo'), T_SELO, 0.6)
add(sfx('whoosh'), T_FINAL - 0.43, 0.8)
add(sfx('boom'), T_FINAL - 0.02, 1.0)
add(sfx('brilho'), T_FINAL, 0.7)

# ---------- master ----------
mix = np.tanh(mix * 1.5) / np.tanh(1.5)  # compressão suave pra encorpar no celular
mix *= np.minimum(1, (N - np.arange(N)) / (SR * 0.3))[:, None]
mix /= np.max(np.abs(mix)) / 0.89
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('audio ok')
