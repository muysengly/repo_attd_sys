#!/bin/bash

# show admin dialog to get sudo access
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi


# update and upgrade system packages
sudo apt update && sudo apt upgrade -y


# install necessary packages for linux
sudo apt install python3-pip python3-venv python3-opencv python3-pyqt5 build-essential -y


# download the project from GitHub, then unzip and remove the zip file
curl -L -o tmp.zip https://github.com/muysengly/repo_attd_sys/archive/refs/heads/main.zip && unzip tmp.zip && rm tmp.zip


# rename the unzipped folder to attd_system_app
mv repo_attd_sys-main attd_system_app && cd attd_system_app


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


# change permission to execute the run_linux.sh script
chmod +x run_linux.sh


# show completion message
echo "Setup completed"
read -n 1 -s -r -p "Press any key to exit..."