# Reels 3: abajur Tocatoca (queijo, capivara e ursinho), de R$149,75 por R$98,00
# Antes de renderizar: python3 montar_cards.py tocatoca  (gera o fundo da cena de preço)
MARCA = 'EMBULED'
PRECO_DE = 149.75
PRECO_POR = 98.00
SAIDA = 'reels-esquenta-black-tocatoca.mp4'

P = 'fotos/tocatoca/'
CENAS = [
    {'src': P + 'queijo.jpg', 'zoom': 1.15, 'dx': -30, 'dy': 20, 'dy0': 120,
     'linhas': [('ABAJUR', 'branco', 140), ('TOCATOCA', 'ambar', 150)]},
    {'src': P + 'capivara.jpg', 'zoom': 1.15, 'dx': 30, 'dy': -30, 'dy0': 180,
     'linhas': [('QUEIJO, CAPIVARA', 'branco', 108), ('OU URSINHO', 'ambar', 140)]},
    {'src': P + 'ursinho.jpg', 'zoom': 1.15, 'dx': 0, 'dy': 30, 'dy0': 60,
     'linhas': [('PREÇO DE BLACK', 'branco', 118)]},
]
FUNDO_PRECO = {'src': P + 'trio.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': P + 'trio.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (895, 905)  # canto do card do ursinho, sem cobrir o rosto
