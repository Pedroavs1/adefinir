# Reels 11: pendente Acrilux Torso Gold, de R$1.953,12 por R$1.367,20
# (a etiqueta da loja vista na foto do Fluida dizia 1.369,20: confirmar antes de postar)
# Antes de renderizar:
#   ./preparar_clip.sh fotos/torso/video.mov build/clip-torso
#   python3 montar_cards.py torso
MARCA = 'CASA DO LED'
PRECO_DE = 1953.12
PRECO_POR = 1367.20
SAIDA = 'reels-esquenta-led-friday-acrilux-torso.mp4'

P = 'fotos/torso/'
CENAS = [
    {'src': 'build/clip-torso', 'ini': 0.0, 'zoom': 1.3, 'dx': 0, 'dy': 0, 'dy0': 288,
     'linhas': [('PENDENTE ACRILUX', 'branco', 96), ('TORSO GOLD', 'ambar', 150)]},
    {'src': P + 'foto2.jpg', 'zoom': 1.15, 'dx': 30, 'dy': 0, 'dy0': 144,
     'linhas': [('CASA DO LED', 'ambar', 150)]},
    # close na volta maior do acrílico
    {'src': P + 'foto1.jpg', 'zoom': 1.6, 'dx': -40, 'dy': 0, 'dx0': 612, 'dy0': 274,
     'linhas': [('PREÇO DE', 'branco', 140), ('LED FRIDAY', 'ambar', 150)]},
]
FUNDO_PRECO = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (880, 880)
