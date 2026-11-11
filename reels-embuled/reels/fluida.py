# Reels 10: pendente Acrilux Fluida Gold, de R$1.158,38 por R$810,90
# Antes de renderizar:
#   ./preparar_clip.sh fotos/fluida/v1.mov build/clip-fluida1
#   ./preparar_clip.sh fotos/fluida/v2.mov build/clip-fluida2
MARCA = 'EMBULED'
PRECO_DE = 1158.38
PRECO_POR = 810.90
SAIDA = 'reels-esquenta-black-acrilux-fluida.mp4'

V1, V2 = 'build/clip-fluida1', 'build/clip-fluida2'
# enquadramentos puxados pra cima: as etiquetas de outros produtos ficam embaixo, fora do quadro
CENAS = [
    {'src': V1, 'ini': 0.0, 'zoom': 1.4, 'dx': 0, 'dy': 0, 'dy0': -384,
     'linhas': [('PENDENTE ACRILUX', 'branco', 96), ('FLUIDA GOLD', 'ambar', 150)]},
    {'src': 'fotos/fluida/foto.jpg', 'zoom': 1.8, 'dx': -40, 'dy': 0, 'dx0': 418, 'dy0': -600,
     'linhas': [('EMBULED', 'ambar', 170)]},
    {'src': V2, 'ini': 1.0, 'zoom': 1.5, 'dx': 0, 'dy': 0, 'dy0': -480,
     'linhas': [('PREÇO DE BLACK', 'branco', 118)]},
]
FUNDO_PRECO = {'src': V2, 'ini': 0.0, 'zoom': 1.3, 'dx': 0, 'dy': -288}
FUNDO_FINAL = {'src': V1, 'ini': 2.5, 'zoom': 1.4, 'dx': 0, 'dy': -384}
