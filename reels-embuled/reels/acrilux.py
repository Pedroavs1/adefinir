# Reels 9: pendente Acrilux Eterna, de R$1.469,52 por R$1.028,65
# Antes de renderizar:
#   ./preparar_clip.sh fotos/acrilux/v1.mov build/clip-acrilux1
#   ./preparar_clip.sh fotos/acrilux/v2.mov build/clip-acrilux2
#   python3 montar_cards.py acrilux
MARCA = 'EMBULED'
PRECO_DE = 1469.52
PRECO_POR = 1028.65
SAIDA = 'reels-esquenta-black-acrilux-eterna.mp4'

P = 'fotos/acrilux/'
CENAS = [
    {'src': 'build/clip-acrilux1', 'ini': 0.3, 'zoom': 1.3, 'dx': 0, 'dy': 0, 'dy0': 288,
     'linhas': [('PENDENTE', 'branco', 140), ('ACRILUX ETERNA', 'ambar', 118)]},
    {'src': P + 'foto.jpg', 'zoom': 1.2, 'dx': -40, 'dy': 0, 'dx0': 57, 'dy0': 192,
     'linhas': [('EMBULED', 'ambar', 170)]},
    # zoom maior pra tirar do quadro os clientes andando embaixo
    {'src': 'build/clip-acrilux2', 'ini': 0.5, 'zoom': 1.6, 'dx': 0, 'dy': 0, 'dy0': 56,
     'linhas': [('PREÇO DE BLACK', 'branco', 118)]},
]
FUNDO_PRECO = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (880, 880)
