# Setup

## Setup Dependencies

###### Update and Upgrade System

sudo apt-get update

sudo apt-get upgrade

###### Install Python3 and Pip3

sudo apt-get install -y python3-pip python3-dev python3-venv

###### Install Required Packages

pip install -y pyqt5 opencv-python insightface onnxruntime --break-system-packages

## Setup Auto Run for Raspberry Pi 4

crontab -e

@reboot sleep 10 && DISPLAY=:0 QT_QPA_PLATFORM=eglfs /usr/bin/lxterminal -e "bash -c 'cd /home/pi/repo_attendance_system_gtr-main && sudo /usr/bin/python /home/pi/repo_attendance_system_gtr-main/Main.py; exec bash'"

## Setup Auto Run for Ubuntu

create bash file

run.sh

run autostart

and add run.sh

## Install PyQt5 Designer

To install PyQt5 Designer, run:

```bash
sudo apt-get install -y qttools5-dev-tools
```

You can then launch Designer with:

```bash
designer
```
