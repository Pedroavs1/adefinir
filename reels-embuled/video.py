# Renderiza o reels (1080x1920, 30 fps) e faz o mux com o áudio.
# Uso: python3 video.py build/audio.wav saida.mp4
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import glob
import importlib
from timeline import *

# qual reels renderizar: REELS=elo_gold python3 video.py ...
C = importlib.import_module('reels.' + os.environ.get('REELS', 'ventiladores'))
FONT_BLACK = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
FONT_BOLD = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FONT_MED = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'

AMBAR = (255, 176, 32)
LARANJA = (255, 92, 20)
VERMELHO = (255, 46, 46)
BRANCO = (255, 255, 255)
CINZA = (190, 190, 190)

rng = np.random.default_rng(3)


# ---------- utilidades ----------
def font(path, size):
    return ImageFont.truetype(path, size)


def clamp01(x):
    return max(0.0, min(1.0, x))


def ease_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_back(x, s=1.7):
    x = clamp01(x)
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


def texto(txt, fnt, cor, glow=None, glow_r=28, tracking=0, stroke=0, stroke_cor=None):
    """Sprite RGBA do texto, com brilho opcional."""
    # largura considerando espaçamento entre letras
    chars = list(txt)
    widths = [fnt.getbbox(c)[2] for c in chars]
    w = int(sum(widths) + tracking * (len(chars) - 1)) + 2 * stroke
    asc, desc = fnt.getmetrics()
    h = asc + desc + 2 * stroke
    pad = glow_r * 3 if glow else 10
    img = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad + stroke
    for c, cw in zip(chars, widths):
        d.text((x, pad + stroke), c, font=fnt, fill=cor,
               stroke_width=stroke, stroke_fill=stroke_cor or cor)
        x += cw + tracking
    if glow:
        a = img.split()[3].filter(ImageFilter.GaussianBlur(glow_r))
        g = Image.new('RGBA', img.size, glow + (0,))
        g.putalpha(a.point(lambda v: min(255, int(v * 1.6))))
        g.alpha_composite(img)
        img = g
    img.pad = pad
    return img


def colar(frame, spr, cx, cy, escala=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0.003 or escala <= 0.01:
        return
    s = spr
    if abs(escala - 1) > 0.002:
        s = s.resize((max(1, int(s.width * escala)), max(1, int(s.height * escala))), Image.BICUBIC)
    if rot:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = s.split()[3].point(lambda v: int(v * alpha))
        s = s.copy()
        s.putalpha(a)
    frame.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))


def cobrir(img, escala=1.0, dx=0.0, dy=0.0):
    """Preenche 1080x1920 com a foto (cover) com zoom e deslocamento."""
    base = max(W / img.width, H / img.height) * escala
    nw, nh = int(img.width * base), int(img.height * base)
    x0 = min(max(0, (nw - W) / 2 + dx), nw - W)
    y0 = min(max(0, (nh - H) / 2 + dy), nh - H)
    box = (x0 / base, y0 / base, (x0 + W) / base, (y0 + H) / base)
    return img.resize((W, H), Image.BICUBIC, box=box)


def gradiente_vertical(top_a, bot_a, y0=0, y1=H):
    g = np.zeros((H, W, 4), np.uint8)
    ys = np.clip((np.arange(H) - y0) / max(1, (y1 - y0)), 0, 1)
    a = (top_a + (bot_a - top_a) * ys) * 255
    g[..., 3] = a[:, None].astype(np.uint8)
    return Image.fromarray(g, 'RGBA')


def vinheta(forca=0.75):
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((r - 0.55) / 0.6, 0, 1) ** 1.6 * forca * 255
    v = np.zeros((H, W, 4), np.uint8)
    v[..., 3] = a.astype(np.uint8)
    return Image.fromarray(v, 'RGBA')


def brilho_radial(cor, raio, cx, cy, forca=1.0):
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / raio
    a = np.clip(1 - r, 0, 1) ** 2 * forca * 255
    v = np.zeros((H, W, 4), np.uint8)
    v[..., 0], v[..., 1], v[..., 2] = cor
    v[..., 3] = a.astype(np.uint8)
    return Image.fromarray(v, 'RGBA')


def brl(v):
    s = f'{v:,.2f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


# ---------- recursos pré-renderizados ----------
_fontes = {}


def fonte(src, t=0.0, ini=0.0):
    """Foto, ou quadro de uma pasta de quadros extraídos de vídeo (30 fps)."""
    if os.path.isdir(src):
        qs = _fontes.setdefault(src, sorted(glob.glob(os.path.join(src, '*.jpg'))))
        i = min(len(qs) - 1, max(0, int((ini + t) * 30)))
        return Image.open(qs[i]).convert('RGB')
    if src not in _fontes:
        _fontes[src] = Image.open(src).convert('RGB')
    return _fontes[src]


CORES = {'branco': (255, 255, 255), 'ambar': (255, 176, 32)}
VINHETA = vinheta()
SOMBRA_BAIXO = gradiente_vertical(0, 0.94, 600, 1250)
SOMBRA_TOPO = gradiente_vertical(0.65, 0, 0, 420)
BRILHO_INTRO = brilho_radial(LARANJA, 900, W / 2, 960, 0.55)
BRILHO_FINAL = brilho_radial(AMBAR, 1000, W / 2, 900, 0.5)

S_ESQUENTA = texto('ESQUENTA', font(FONT_BLACK, 150), BRANCO, glow=(255, 120, 40), glow_r=22, tracking=4)
S_ESQUENTA_OFF = texto('ESQUENTA', font(FONT_BLACK, 150), (45, 45, 45), tracking=4)
CAMPANHA = 'LED FRIDAY'  # nome da campanha depois do "ESQUENTA"


def fonte_que_cabe(txt, tam, larg_max, path=FONT_BLACK):
    while tam > 60 and font(path, tam).getlength(txt) > larg_max:
        tam -= 4
    return font(path, tam)


F_CAMPANHA = fonte_que_cabe(CAMPANHA, 300, 960)
S_BLACK = texto(CAMPANHA, F_CAMPANHA, AMBAR, glow=LARANJA, glow_r=40, tracking=-4)
S_EMBULED = texto(' '.join(C.MARCA), font(FONT_BOLD, 56), BRANCO, tracking=6)

_tag = f'ESQUENTA {CAMPANHA}  •  {C.MARCA}'
S_TAG = texto(_tag, fonte_que_cabe(_tag, 40, 880, FONT_BOLD), BRANCO, tracking=3)
TAG_BG = None

S_FOTO_TXT = [[texto(txt, font(FONT_BLACK, tam), CORES[cor], glow=(0, 0, 0), glow_r=24, tracking=2 if tam >= 160 else 0)
               for txt, cor, tam in cena['linhas']] for cena in C.CENAS]

S_DE = texto('DE', font(FONT_BOLD, 64), CINZA, tracking=4)
S_PRECO_VELHO = texto('R$' + brl(C.PRECO_DE), font(FONT_BLACK, 130), CINZA)
S_POR = texto('POR APENAS', font(FONT_BOLD, 64), BRANCO, tracking=4)
# preço grande: 220 px, reduzido se o maior valor do contador (R$ + número) não couber em 940 px
_tam = 220
while _tam > 120:
    _fp, _fr = font(FONT_BLACK, _tam), font(FONT_BLACK, int(_tam * 100 / 220))
    _larg = max(_fp.getlength(brl(v)) for v in (C.PRECO_DE, C.PRECO_POR)) + _fr.getlength('R$') + 16
    if _larg <= 940:
        break
    _tam -= 6
F_PRECO = font(FONT_BLACK, _tam)
F_RS = font(FONT_BLACK, int(_tam * 100 / 220))
S_RS = texto('R$', F_RS, AMBAR, glow=LARANJA, glow_r=26)
S_PRECO_FINAL = texto(brl(C.PRECO_POR), F_PRECO, AMBAR, glow=LARANJA, glow_r=36, tracking=-4)

pct = int((C.PRECO_DE - C.PRECO_POR) / C.PRECO_DE * 100)  # arredonda pra baixo


def selo():
    r = 150
    img = Image.new('RGBA', (2 * r + 40, 2 * r + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = []
    for i in range(48):
        a = i / 48 * 2 * math.pi
        rr = r if i % 2 == 0 else r - 16
        pts.append((r + 20 + rr * math.cos(a), r + 20 + rr * math.sin(a)))
    d.polygon(pts, fill=VERMELHO)
    t1 = texto(f'-{pct}%', font(FONT_BLACK, 104), BRANCO)
    t2 = texto('OFF', font(FONT_BLACK, 56), BRANCO, tracking=4)
    img.alpha_composite(t1, (int(img.width / 2 - t1.width / 2), int(img.height / 2 - t1.height / 2 - 26)))
    img.alpha_composite(t2, (int(img.width / 2 - t2.width / 2), int(img.height / 2 - t2.height / 2 + 58)))
    return img


S_SELO = selo()
S_FINAL_1 = texto('ESQUENTA', font(FONT_BLACK, 150), BRANCO, glow=(255, 120, 40), glow_r=22, tracking=4)
S_FINAL_2 = texto(CAMPANHA, F_CAMPANHA, AMBAR, glow=LARANJA, glow_r=40, tracking=-4)
S_FINAL_3 = texto(' '.join(C.MARCA), font(FONT_BOLD, 56), BRANCO, tracking=6)
S_FINAL_PRECO = texto('R$' + brl(C.PRECO_POR), font(FONT_BLACK, 120), (20, 20, 20))


def pilula(spr, cor, padx=60, pady=24):
    img = Image.new('RGBA', (spr.width + 2 * padx, spr.height + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=img.height // 2, fill=cor)
    img.alpha_composite(spr, (padx, pady))
    return img


P_FINAL_PRECO = pilula(S_FINAL_PRECO, AMBAR)
P_TAG = pilula(S_TAG, (0, 0, 0, 170), 40, 10)

# janelas do neon piscando (medidas no efeito neon.mp3, que entra em 0,1 s)
LED_ON = [(0.10, 0.31), (0.36, 0.41), (0.46, 0.57), (0.62, 0.67), (0.82, 0.93), (0.96, 99)]


def led_on(t):
    return any(a <= t < b for a, b in LED_ON)


# ---------- cenas ----------
def cena_intro(t):
    f = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    on = led_on(t)
    if t >= T_BLACK:
        k = ease_out((t - T_BLACK) / 0.6)
        f.alpha_composite(Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 0)), BRILHO_INTRO, k))
    cy_esq = 760 if t < T_BLACK else 760 - 30 * ease_out((t - T_BLACK) / 0.3)
    colar(f, S_ESQUENTA if on else S_ESQUENTA_OFF, W / 2, cy_esq, 1.0 + 0.02 * math.sin(t * 3))
    if t >= T_BLACK:
        p = (t - T_BLACK) / 0.18
        esc = 2.6 - 1.6 * ease_out(p) if p < 1 else 1.0 + 0.015 * math.sin((t - T_BLACK) * 4)
        colar(f, S_BLACK, W / 2, 980, esc, clamp01(p * 2))
    if t >= T_BLACK + 0.45:
        k = ease_out((t - T_BLACK - 0.45) / 0.4)
        colar(f, S_EMBULED, W / 2, 1200 + 30 * (1 - k), 1.0, k)
    return f


def cena_foto(t, idx, t_ini, t_fim):
    lt = t - t_ini
    dur = t_fim - t_ini
    punch = 1.0 + 0.22 * (1 - ease_out(lt / 0.35))
    cena = C.CENAS[idx]
    zoom = cena['zoom'] + 0.08 * lt / dur
    dx = cena.get('dx0', 0) + cena['dx'] * lt / dur
    dy = cena.get('dy0', 0) + cena['dy'] * lt / dur
    img = cobrir(fonte(cena['src'], lt, cena.get('ini', 0)), zoom * punch, dx, dy)
    if lt < 0.12:
        img = img.filter(ImageFilter.BoxBlur(int(14 * (1 - lt / 0.12)) + 1))
    f = img.convert('RGBA')
    f.alpha_composite(SOMBRA_TOPO)
    f.alpha_composite(gradiente_vertical(0, 0.75, 1150, 1700) if idx < 3 else SOMBRA_BAIXO)
    f.alpha_composite(VINHETA)
    colar(f, P_TAG, W / 2, 250, 1.0, 1.0)
    # texto grande entrando com "slam"
    k = ease_back((lt - 0.12) / 0.3)
    a = clamp01((lt - 0.12) / 0.12)
    linhas = S_FOTO_TXT[idx]
    ys = [1440] if len(linhas) == 1 else [1380, 1510]
    for j, (spr, y) in enumerate(zip(linhas, ys)):
        atraso = 0.12 + 0.28 * j
        kj = ease_back((lt - atraso) / 0.3)
        colar(f, spr, W / 2, y, 1.4 - 0.4 * kj, clamp01((lt - atraso) / 0.12))
    return f


def cena_preco(t):
    lt = t - T_PRECO
    fp = C.FUNDO_PRECO
    img = cobrir(fonte(fp['src'], lt, fp.get('ini', 0)), fp['zoom'] + 0.05 * lt / 6, fp['dx'], fp['dy'])
    if lt < 0.12:
        img = img.filter(ImageFilter.BoxBlur(int(14 * (1 - lt / 0.12)) + 1))
    f = img.convert('RGBA')
    f.alpha_composite(SOMBRA_TOPO)
    f.alpha_composite(SOMBRA_BAIXO)
    f.alpha_composite(VINHETA)
    colar(f, P_TAG, W / 2, 250, 1.0, 1.0)

    # "DE R$1.068,01"
    k = ease_out(lt / 0.35)
    colar(f, S_DE, W / 2, 1010 + 40 * (1 - k), 1.0, k)
    colar(f, S_PRECO_VELHO, W / 2, 1110 + 40 * (1 - k), 1.0, k)
    # risco vermelho
    if t >= T_RISCO:
        p = ease_out((t - T_RISCO) / 0.14)
        d = ImageDraw.Draw(f)
        x0 = W / 2 - S_PRECO_VELHO.width / 2 + 10
        x1 = x0 + (S_PRECO_VELHO.width - 20) * p
        d.line((x0, 1135, x1, 1095), fill=VERMELHO, width=16)

    # contador / preço novo
    if t >= T_CONT0:
        kp = ease_out((t - T_CONT0) / 0.3)
        colar(f, S_POR, W / 2, 1270 + 30 * (1 - kp), 1.0, kp)
        if t < T_POR:
            p = (t - T_CONT0) / (T_POR - T_CONT0)
            v = C.PRECO_DE - (C.PRECO_DE - C.PRECO_POR) * (1 - (1 - p) ** 2.2)
            num = texto(brl(v), F_PRECO, BRANCO, tracking=-4)
            rs = texto('R$', F_RS, BRANCO)
            esc = 1.0
            glow = False
        else:
            num, rs = S_PRECO_FINAL, S_RS
            pp = (t - T_POR) / 0.22
            esc = 1.0 + 0.25 * (1 - ease_out(pp)) + 0.02 * math.sin((t - T_POR) * 5)
            glow = True
        # posiciona R$ + número centralizados juntos
        nw = num.width - 2 * num.pad
        rw = rs.width - 2 * rs.pad
        larg = rw + 16 + nw
        cx_num = W / 2 + larg / 2 - nw / 2
        cx_rs = W / 2 - larg / 2 + rw / 2
        colar(f, num, cx_num, 1450, esc, kp)
        colar(f, rs, W / 2 + (cx_rs - W / 2) * esc, 1450 - 45 * esc, esc, kp)

    if t >= T_SELO:
        p = (t - T_SELO) / 0.3
        sx, sy = getattr(C, 'SELO', (810, 720))
        colar(f, S_SELO, sx, sy, ease_back(p, 2.2) * 0.95, clamp01(p * 3), rot=14 + 4 * math.sin((t - T_SELO) * 3))
    return f


def cena_final(t):
    lt = t - T_FINAL
    f = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    ff = C.FUNDO_FINAL
    bg = cobrir(fonte(ff['src'], lt, ff.get('ini', 0)), ff['zoom'] + 0.04 * lt, ff['dx'], ff['dy']).convert('RGBA')
    f = Image.blend(f, bg, 0.22)
    f.alpha_composite(BRILHO_FINAL)
    f.alpha_composite(VINHETA)
    k = ease_back(lt / 0.3)
    colar(f, S_FINAL_1, W / 2, 640, 1.3 - 0.3 * k, clamp01(lt / 0.1))
    k2 = ease_back((lt - 0.08) / 0.3)
    colar(f, S_FINAL_2, W / 2, 860, 1.5 - 0.5 * k2, clamp01((lt - 0.08) / 0.1))
    k3 = ease_out((lt - 0.3) / 0.35)
    colar(f, S_FINAL_3, W / 2, 1080 + 30 * (1 - k3), 1.0, k3)
    k4 = ease_back((lt - 0.45) / 0.35)
    colar(f, P_FINAL_PRECO, W / 2, 1290, max(0.01, k4), clamp01((lt - 0.45) / 0.1))
    return f


# ---------- efeitos globais ----------
TREMORES = [(T_BLACK, 26), (T_RISCO, 12), (T_POR, 30), (T_SELO, 10), (T_FINAL, 30)]
FLASHES = [(T_BLACK, 0.55), (T_FOTO1, 0.5), (T_FOTO2, 0.5), (T_FOTO3, 0.5),
           (T_PRECO, 0.45), (T_POR, 0.5), (T_FINAL, 0.7)]


def frame(t):
    if t < T_FOTO1:
        f = cena_intro(t)
    elif t < T_FOTO2:
        f = cena_foto(t, 0, T_FOTO1, T_FOTO2)
    elif t < T_FOTO3:
        f = cena_foto(t, 1, T_FOTO2, T_FOTO3)
    elif t < T_PRECO:
        f = cena_foto(t, 2, T_FOTO3, T_PRECO)
    elif t < T_FINAL:
        f = cena_preco(t)
    else:
        f = cena_final(t)

    dx = dy = 0.0
    for ts, amp in TREMORES:
        if ts <= t < ts + 0.3:
            a = amp * (1 - (t - ts) / 0.3)
            dx += rng.uniform(-a, a)
            dy += rng.uniform(-a, a)
    if dx or dy:
        g = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        g.alpha_composite(f.resize((int(W * 1.04), int(H * 1.04))),
                          (int(-W * 0.02 + dx), int(-H * 0.02 + dy)))
        f = g
    for ts, a in FLASHES:
        if ts <= t < ts + 0.12:
            k = a * (1 - (t - ts) / 0.12)
            f = Image.blend(f, Image.new('RGBA', (W, H), (255, 240, 220, 255)), k)
    if t > DUR - 0.4:
        f = Image.blend(f, Image.new('RGBA', (W, H), (0, 0, 0, 255)), (t - (DUR - 0.4)) / 0.4)
    return f.convert('RGB')


if __name__ == '__main__':
    audio, saida = sys.argv[1], sys.argv[2]
    so = [a for a in sys.argv if a.startswith('--frame=')]
    if so:
        t = float(so[0].split('=')[1])
        frame(t).save(saida)
        sys.exit()
    ff = subprocess.Popen([
        'ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-i', audio,
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', saida],
        stdin=subprocess.PIPE)
    total = int(DUR * FPS)
    for i in range(total):
        ff.stdin.write(frame(i / FPS).tobytes())
        if i % 60 == 0:
            print(f'{i}/{total}', flush=True)
    ff.stdin.close()
    ff.wait()
    print('ok', saida)
