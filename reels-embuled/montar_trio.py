# Fundo da cena de preço do Tocatoca: os três abajures lado a lado na metade de cima (1080x1920).
# Uso: python3 montar_trio.py
from PIL import Image, ImageDraw

W, H = 1080, 1920
TW, TH, GAP, Y0 = 306, 540, 20, 350
# (arquivo, centro x, centro y, altura do recorte) em pixels da foto original 1450x2576
RECORTES = [
    ('fotos/tocatoca/queijo.jpg', 390, 1560, 1350),
    ('fotos/tocatoca/capivara.jpg', 450, 1790, 1400),
    ('fotos/tocatoca/ursinho.jpg', 440, 1590, 1650),
]

fundo = Image.new('RGB', (W, H), (8, 8, 8))
x = (W - 3 * TW - 2 * GAP) // 2
for arq, cx, cy, ch in RECORTES:
    img = Image.open(arq).convert('RGB')
    cw = ch * TW / TH
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    box = (max(0, box[0]), max(0, box[1]), min(img.width, box[2]), min(img.height, box[3]))
    tile = img.resize((TW, TH), Image.LANCZOS, box=box)
    mask = Image.new('L', (TW, TH), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, TW - 1, TH - 1), radius=28, fill=255)
    fundo.paste(tile, (x, Y0), mask)
    x += TW + GAP
fundo.save('fotos/tocatoca/trio.jpg', quality=92)
print('ok')
