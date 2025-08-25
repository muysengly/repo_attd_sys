#!/bin/bash

# export QT_QPA_PLATFORM=eglfs
export QT_QPA_PLATFORM=wayland

source ~/venv/bin/activate

cd ~

chmod +x Main.py

python Main.py

