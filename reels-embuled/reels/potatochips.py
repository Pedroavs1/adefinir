# Reels 5: abajur Tocatoca Potato Chips, de R$187,25 por R$121,00
# Antes de renderizar: python3 montar_cards.py potatochips  (gera o fundo da cena de preço)
MARCA = 'EMBULED'
PRECO_DE = 187.25
PRECO_POR = 121.00
SAIDA = 'reels-esquenta-black-potatochips.mp4'

F = 'fotos/potatochips/chips.jpg'
# uma foto só: cada cena é um enquadramento diferente (inteiro, close no logo, caixa)
CENAS = [
    {'src': F, 'zoom': 1.1, 'dx': 30, 'dy': 20, 'dx0': -150, 'dy0': 100,
     'linhas': [('ABAJUR', 'branco', 140), ('TOCATOCA', 'ambar', 150)]},
    {'src': F, 'zoom': 1.5, 'dx': -30, 'dy': -20, 'dx0': -270, 'dy0': 270,
     'linhas': [('POTATO CHIPS', 'ambar', 122)]},
    {'src': F, 'zoom': 1.6, 'dx': 0, 'dy': 30, 'dx0': 300, 'dy0': 0,
     'linhas': [('PREÇO DE BLACK', 'branco', 118)]},
]
FUNDO_PRECO = {'src': 'fotos/potatochips/card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': 'fotos/potatochips/card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (880, 880)
