#!/bin/bash


# 1. update and upgrade system packages
sudo apt update
sudo apt upgrade -y


# 2. install necessary packages
sudo apt install python3-pip python3-venv python3-opencv python3-pyqt5 build-essential curl -y





# change working directory to home directory
cd ~


# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi


# Activate virtual environment
source ~/venv/bin/activate

# install dependencies
pip install pyqt5 opencv-python insightface onnxruntime


# download the repository https://github.com/muysengly/repo_attendance_system_gtr/archive/refs/heads/main.zip
curl -L -o tmp.zip https://github.com/muysengly/repo_attendance_system_gtr/archive/refs/heads/main.zip


# @REM Extract the downloaded zip file
unzip tmp.zip


# delete the zip file after extraction
rm tmp.zip



###### run project

cd ~

# change working directory to the extracted folder
cd repo_attendance_system_gtr-main


export QT_QPA_PLATFORM=wayland

python Main.py
