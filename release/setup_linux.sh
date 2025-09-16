#!/bin/bash

# update and upgrade system packages
sudo apt update
sudo apt upgrade -y


# install necessary packages for linux
sudo apt install python3-pip python3-venv python3-opencv python3-pyqt5 build-essential -y


# download the project from GitHub, then unzip and remove the zip file
curl -L -o tmp.zip https://github.com/muysengly/repo_attd_sys/archive/refs/heads/main.zip
unzip tmp.zip
rm tmp.zip


# rename the unzipped folder to attd_system_app
mv repo_attd_sys-main attd_system_app
cd attd_system_app


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



PROJECT_PATH="$(dirname "$(realpath "$0")")"

cat > "$PROJECT_PATH/run_linux.desktop" <<EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Run Main
Comment=Run Python Main.py inside venv
Path=$PROJECT_PATH
Exec=bash -c "cd '$PROJECT_PATH' && source venv/bin/activate && python Main.py"
Icon=$PROJECT_PATH/resource/asset/my_logo.ico
Terminal=true
EOL

chmod +x "$PROJECT_PATH/run_linux.desktop"




# show completion message
echo "Setup completed."
echo "You can now run the application using run_linux.sh"
echo
read -n 1 -s -r -p "Press any key to exit..."
echo