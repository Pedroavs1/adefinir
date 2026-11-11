# Reels 7: pendente Infini Sway (preto ou gold), de R$787,25 por R$499,00
# Antes de renderizar: python3 montar_cards.py sway  (gera o fundo da cena de preço)
MARCA = 'CASA DO LED'
PRECO_DE = 787.25
PRECO_POR = 499.00
SAIDA = 'reels-esquenta-led-friday-sway.mp4'

P = 'fotos/sway/'
CENAS = [
    {'src': P + 'duas-cores.jpg', 'zoom': 1.2, 'dx': -40, 'dy': 0, 'dy0': 150,
     'linhas': [('PENDENTE INFINI', 'branco', 108), ('SWAY', 'ambar', 170)]},
    {'src': P + 'preto.jpg', 'zoom': 1.15, 'dx': 40, 'dy': -30, 'dy0': 100,
     'linhas': [('PRETO', 'branco', 200)]},
    {'src': P + 'gold.jpg', 'zoom': 1.2, 'dx': -40, 'dy': 20, 'dy0': 0,
     'linhas': [('OU GOLD', 'ambar', 200)]},
]
# cena do preço: as duas cores lado a lado
FUNDO_PRECO = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (900, 880)
