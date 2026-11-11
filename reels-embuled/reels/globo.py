# Reels 8: pendente Glass Globo cristal ou âmbar, de R$333,64 por R$199,00
# Antes de renderizar: python3 montar_cards.py globo
# (caixa-4k.jpg = ffmpeg -ss 1 -i fotos/globo/caixas.mov -frames:v 1 -q:v 2 fotos/globo/caixa-4k.jpg)
MARCA = 'EMBULED'
PRECO_DE = 333.64
PRECO_POR = 199.00
SAIDA = 'reels-esquenta-black-glass-globo.mp4'

P = 'fotos/globo/'
CENAS = [
    {'src': P + 'close.jpg', 'zoom': 1.1, 'dx': -30, 'dy': 20, 'dy0': -40,
     'linhas': [('PENDENTE', 'branco', 140), ('GLASS GLOBO', 'ambar', 140)]},
    # âmbar não está instalado na loja: close na arte da embalagem (quadro 4K do vídeo das caixas),
    # que mostra o globo cristal e o âmbar lado a lado
    {'src': P + 'caixa-4k.jpg', 'zoom': 3.6, 'dx': -40, 'dy': 0, 'dx0': 648, 'dy0': -28,
     'linhas': [('CRISTAL', 'branco', 170), ('OU ÂMBAR', 'ambar', 170)]},
    # close no globo dourado, sem as etiquetas de preço de outros produtos
    {'src': P + 'dourado.jpg', 'zoom': 1.6, 'dx': 30, 'dy': 30, 'dx0': -55, 'dy0': 640,
     'linhas': [('PREÇO DE BLACK', 'branco', 118)]},
]
FUNDO_PRECO = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
FUNDO_FINAL = {'src': P + 'card.jpg', 'zoom': 1.0, 'dx': 0, 'dy': 0}
SELO = (870, 860)
