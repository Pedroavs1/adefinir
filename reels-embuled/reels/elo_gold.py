# Reels 2: pendente Elo Gold, de R$787,25 por R$499,00
# Antes de renderizar: ./preparar_clip.sh fotos/elo/elo.mov build/clip-elo
MARCA = 'CASA DO LED'
PRECO_DE = 787.25
PRECO_POR = 499.00
SAIDA = 'reels-esquenta-led-friday-elo-gold.mp4'

CLIP = 'build/clip-elo'
FOTO = 'fotos/elo/elo-loja.jpg'

CENAS = [
    {'src': CLIP, 'ini': 0.0, 'zoom': 1.0, 'dx': 0, 'dy': 0,
     'linhas': [('PENDENTE', 'branco', 140), ('ELO GOLD', 'ambar', 150)]},
    {'src': FOTO, 'zoom': 1.25, 'dx': 30, 'dy': -40, 'dy0': -200,
     'linhas': [('CASA DO LED', 'ambar', 150)]},
    {'src': CLIP, 'ini': 3.4, 'zoom': 1.35, 'dx': -40, 'dy': 0,
     'linhas': [('PREÇO DE', 'branco', 140), ('LED FRIDAY', 'ambar', 150)]},
]
# fundo do preço: vídeo andando, aproximado e com os anéis na metade de cima
FUNDO_PRECO = {'src': CLIP, 'ini': 0.3, 'zoom': 1.4, 'dx': 0, 'dy': 380}
FUNDO_FINAL = {'src': FOTO, 'zoom': 1.3, 'dx': 0, 'dy': -200}
