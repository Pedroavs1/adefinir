# Reels 8: pendente Glass Globo cristal ou âmbar, de R$333,64 por R$199,00
# Antes de renderizar:
#   ./preparar_clip.sh fotos/globo/caixas.mov build/clip-globo
#   python3 montar_cards.py globo
MARCA = 'EMBULED'
PRECO_DE = 333.64
PRECO_POR = 199.00
SAIDA = 'reels-esquenta-black-glass-globo.mp4'

P = 'fotos/globo/'
CLIP = 'build/clip-globo'
CENAS = [
    {'src': P + 'close.jpg', 'zoom': 1.1, 'dx': -30, 'dy': 20, 'dy0': -40,
     'linhas': [('PENDENTE', 'branco', 140), ('GLASS GLOBO', 'ambar', 140)]},
    # caixas na loja: a arte da embalagem mostra as versões cristal e âmbar
    {'src': CLIP, 'ini': 0.5, 'zoom': 1.6, 'dx': -40, 'dy': 0, 'dx0': 211, 'dy0': 100,
     'linhas': [('CRISTAL', 'branco', 170), ('OU ÂMBAR', 'ambar', 170)]},
    # close no globo dourado, sem as etiquetas de preço de outros produtos
    {'src': P + 'dourado.jpg', 'zoom': 1.6, 'dx': 30, 'dy': 30, 'dx0': -55, 'dy0': 640,
     'linhas': [('PREÇO DE BLACK', 'branco', 118)]},
]
FUNDO_PRECO = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (870, 860)
