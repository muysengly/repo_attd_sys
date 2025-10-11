#!/bin/bash


# check if Homebrew is installed
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


# install python3 if not installed
# brew install python3


# download the project from GitHub, then unzip and remove the zip file
curl -L -o tmp.zip https://github.com/muysengly/repo_attd_sys/archive/refs/heads/main.zip
unzip tmp.zip
rm tmp.zip

# set new folder name
new_name=attendance_system


# rename the unzipped folder
mv repo_attd_sys-main $new_name
cd $new_name


# delete folder release
if [ -d "release" ]; then
    rm -rf release
fi
# delete .gitignore file
if [ -f ".gitignore" ]; then
    rm .gitignore
fi
# delete readme.md
if [ -f "README.md" ]; then
    rm README.md
fi



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


# create run.command script to run the application
cat << EOF > run.command
#!/bin/bash

# Navigate to the script directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run the application
python Main.py
EOF


# change permission to execute the run_linux.sh script
chmod +x run.command


# show completion message
echo "Setup completed."
echo "You can now run the application using run.command"
echo
read -n 1 -s -r -p "Press any key to exit..."
echo