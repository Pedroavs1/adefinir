#!/bin/bash
# Renderiza todos os reels (precisa de build/audio.wav e dos clipes/cards preparados).
cd "$(dirname "$0")"
for r in ventiladores elo_gold tocatoca gadofofo potatochips sine sway globo acrilux fluida torso; do
  saida=$(python3 -c "import reels.$r as c; print(c.SAIDA)")
  echo "$r -> $saida"
  REELS=$r python3 video.py build/audio.wav "$saida" > /dev/null &
  while [ "$(jobs -r | wc -l)" -ge 3 ]; do sleep 1; done
done
wait
echo fim
