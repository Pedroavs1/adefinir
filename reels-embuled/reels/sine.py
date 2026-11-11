# Reels 6: pendente Infini Sine Gold, de R$787,25 por R$499,00
# Antes de renderizar: python3 montar_cards.py sine  (gera o fundo da cena de preço)
MARCA = 'EMBULED'
PRECO_DE = 787.25
PRECO_POR = 499.00
SAIDA = 'reels-esquenta-black-sine-gold.mp4'

P = 'fotos/sine/'
CENAS = [
    {'src': P + 'bar.jpg', 'zoom': 1.05, 'dx': -40, 'dy': 0, 'dy0': -40,
     'linhas': [('PENDENTE INFINI', 'branco', 108), ('SINE GOLD', 'ambar', 150)]},
    {'src': P + 'natal.jpg', 'zoom': 1.1, 'dx': 40, 'dy': -30, 'dy0': -60,
     'linhas': [('EMBULED', 'ambar', 170)]},
    {'src': P + 'loja.jpg', 'zoom': 1.9, 'dx': -40, 'dy': 0, 'dx0': 60, 'dy0': -330,
     'linhas': [('PREÇO DE BLACK', 'branco', 118)]},
]
FUNDO_PRECO = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (880, 880)
