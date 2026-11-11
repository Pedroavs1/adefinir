# Reels 4: abajur Tocatoca Gadofofo, de R$168,51 por R$109,00
# Antes de renderizar: python3 montar_cards.py gadofofo  (gera o fundo da cena de preço)
MARCA = 'CASA DO LED'
PRECO_DE = 168.51
PRECO_POR = 109.00
SAIDA = 'reels-esquenta-led-friday-gadofofo.mp4'

P = 'fotos/gadofofo/'
CENAS = [
    {'src': P + 'aceso.jpg', 'zoom': 1.1, 'dx': -30, 'dy': 20, 'dx0': -160, 'dy0': 60,
     'linhas': [('ABAJUR', 'branco', 140), ('TOCATOCA', 'ambar', 150)]},
    {'src': P + 'apagado.jpg', 'zoom': 1.1, 'dx': 30, 'dy': -30, 'dx0': -120, 'dy0': 60,
     'linhas': [('GADOFOFO', 'ambar', 170)]},
    {'src': P + 'aceso.jpg', 'zoom': 1.45, 'dx': 0, 'dy': 30, 'dx0': -200, 'dy0': -150,
     'linhas': [('PREÇO DE', 'branco', 140), ('LED FRIDAY', 'ambar', 150)]},
]
FUNDO_PRECO = {'src': P + 'duo.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': P + 'duo.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (895, 905)
