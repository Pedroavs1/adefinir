# Linha do tempo compartilhada entre vídeo e áudio (segundos).
# 128 BPM; a batida entra junto com o "BLACK" em 1,2 s.
FPS = 30
DUR = 15.0
W, H = 1080, 1920

BPM = 128
BEAT = 60 / BPM
T0 = 1.2


def beat(n):
    return T0 + n * BEAT


T_BLACK = T0                # "BLACK" bate na tela
T_FOTO1 = beat(3)           # 2,61
T_FOTO2 = beat(7)           # 4,48
T_FOTO3 = beat(11)          # 6,36
T_PRECO = beat(15)          # 8,23  cena do preço
T_RISCO = beat(17)          # 9,17  risco no preço antigo
T_CONT0 = beat(18)          # 9,64  contador começa a cair
T_POR = beat(21)            # 11,04 R$249,90 crava
T_SELO = beat(23)           # 11,98 selo de desconto
T_FINAL = beat(27)          # 13,86 cartela final
