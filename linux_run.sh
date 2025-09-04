#!/bin/bash


# activate virtual environment
source venv/bin/activate


# set QT platform to xcb or wayland based on your system
# export QT_QPA_PLATFORM=xcb
# export QT_QPA_PLATFORM=wayland

# set QT scaling factors (adjust as needed)
# export QT_SCALE_FACTOR=1
# export QT_AUTO_SCREEN_SCALE_FACTOR=1
# export QT_SCREEN_SCALE_FACTORS=1


# run the application
python Main.py

