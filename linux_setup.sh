#!/bin/bash


# update and upgrade system packages
sudo apt update
sudo apt upgrade -y


# install necessary packages
sudo apt install python3-pip python3-venv python3-opencv python3-pyqt5 build-essential -y


# install dependencies for insightface
# sudo apt install libopenblas-dev liblapack-dev libjpeg-dev libpng-dev -y


# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi


# Activate virtual environment
source venv/bin/activate


# upgrade pip
python -m pip install --upgrade pip


# install dependencies
pip install pyqt5 opencv-python-headless insightface onnxruntime


