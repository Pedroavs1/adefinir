# Reels 1: ventiladores de teto Embuled, de R$1.068,01 por R$249,90
MARCA = 'CASA DO LED'
PRECO_DE = 1068.01
PRECO_POR = 249.90
SAIDA = 'reels-esquenta-led-friday-ventiladores.mp4'

# 'src' é uma foto ou uma pasta de quadros (vídeo extraído); 'ini' = segundo inicial do vídeo
CENAS = [
    {'src': 'fotos/foto1.jpg', 'zoom': 1.04, 'dx': -40, 'dy': 0,
     'linhas': [('VENTILADORES', 'branco', 130), ('DE TETO', 'ambar', 130)]},
    {'src': 'fotos/foto2.jpg', 'zoom': 1.04, 'dx': 40, 'dy': -30,
     'linhas': [('EMBULED', 'ambar', 170)]},
    {'src': 'fotos/foto3.jpg', 'zoom': 1.04, 'dx': 0, 'dy': 30,
     'linhas': [('PREÇO DE', 'branco', 140), ('LED FRIDAY', 'ambar', 150)]},
]
FUNDO_PRECO = {'src': 'fotos/foto1.jpg', 'zoom': 1.12, 'dx': 0, 'dy': 300}
FUNDO_FINAL = {'src': 'fotos/foto1.jpg', 'zoom': 1.3, 'dx': 0, 'dy': 0}
