# Linha do tempo compartilhada entre vídeo e áudio (segundos).
# 130 BPM (trilha da Black Friday); o drop da música cai junto com o "BLACK" em 1,5 s.
FPS = 30
DUR = 15.0
W, H = 1080, 1920

BPM = 130
BEAT = 60 / BPM
T0 = 1.5


def beat(n):
    return T0 + n * BEAT


T_BLACK = T0                # "BLACK" bate na tela
T_FOTO1 = beat(3)           # 2,88
T_FOTO2 = beat(7)           # 4,73
T_FOTO3 = beat(11)          # 6,58
T_PRECO = beat(15)          # 8,42  cena do preço
T_RISCO = beat(17)          # 9,35  risco no preço antigo
T_CONT0 = beat(18)          # 9,81  contador começa a cair
T_POR = beat(21)            # 11,19 R$249,90 crava
T_SELO = beat(23)           # 12,12 selo de desconto
T_FINAL = beat(27)          # 13,96 cartela final

MUSICA = 'audio-bf/musica-drop130-a.mp3'
DROP_MUSICA = 7.149         # segundo do drop dentro do arquivo da trilha
