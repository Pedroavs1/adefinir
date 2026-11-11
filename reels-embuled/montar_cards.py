# Fundo da cena de preço: produtos em cards lado a lado na metade de cima (1080x1920).
# Uso: python3 montar_cards.py tocatoca | gadofofo | potatochips | sine | sway | globo | acrilux | torso
import sys
from PIL import Image, ImageDraw

W, H = 1080, 1920
# por fundo: saída, (largura, altura, espaço, y do topo) dos cards, e recortes
# (arquivo, centro x, centro y, altura do recorte) em pixels da foto original 1450x2576
FUNDOS = {
    'tocatoca': ('fotos/tocatoca/trio.jpg', (306, 540, 20, 350), [
        ('fotos/tocatoca/queijo.jpg', 390, 1560, 1350),
        ('fotos/tocatoca/capivara.jpg', 450, 1790, 1400),
        ('fotos/tocatoca/ursinho.jpg', 440, 1590, 1650),
    ]),
    'gadofofo': ('fotos/gadofofo/duo.jpg', (420, 600, 24, 340), [
        ('fotos/gadofofo/aceso.jpg', 520, 1450, 1400),
        ('fotos/gadofofo/apagado.jpg', 390, 1500, 1500),
    ]),
    'potatochips': ('fotos/potatochips/card.jpg', (540, 620, 0, 340), [
        ('fotos/potatochips/chips.jpg', 560, 1440, 1330),
    ]),
    'sine': ('fotos/sine/card.jpg', (1000, 600, 0, 330), [
        ('fotos/sine/bar.jpg', 730, 960, 780),
    ]),
    'sway': ('fotos/sway/card.jpg', (500, 600, 20, 330), [
        ('fotos/sway/preto.jpg', 830, 1150, 900),
        ('fotos/sway/gold.jpg', 800, 1000, 820),
    ]),
    'globo': ('fotos/globo/card.jpg', (620, 640, 0, 320), [
        ('fotos/globo/close.jpg', 750, 1010, 1080),
    ]),
    'acrilux': ('fotos/acrilux/card.jpg', (1000, 600, 0, 330), [
        ('fotos/acrilux/foto.jpg', 830, 1160, 760),
    ]),
    'torso': ('fotos/torso/card.jpg', (1000, 620, 0, 320), [
        ('fotos/torso/foto1.jpg', 760, 1210, 870),
    ]),
}

saida, (TW, TH, GAP, Y0), recortes = FUNDOS[sys.argv[1]]
fundo = Image.new('RGB', (W, H), (8, 8, 8))
n = len(recortes)
x = (W - n * TW - (n - 1) * GAP) // 2
for arq, cx, cy, ch in recortes:
    img = Image.open(arq).convert('RGB')
    cw = ch * TW / TH
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    box = (max(0, box[0]), max(0, box[1]), min(img.width, box[2]), min(img.height, box[3]))
    tile = img.resize((TW, TH), Image.LANCZOS, box=box)
    mask = Image.new('L', (TW, TH), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, TW - 1, TH - 1), radius=28, fill=255)
    fundo.paste(tile, (x, Y0), mask)
    x += TW + GAP
fundo.save(saida, quality=92)
print('ok', saida)
