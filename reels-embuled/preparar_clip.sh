#!/bin/bash
# Extrai os quadros de um vídeo do celular (já girado) em 1080x1920, 30 fps, para a pasta indicada.
# Uso: ./preparar_clip.sh <video.mov> <pasta>
set -e
mkdir -p "$2"
ffmpeg -loglevel error -y -i "$1" -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -q:v 2 "$2/%04d.jpg"
ls "$2" | wc -l
