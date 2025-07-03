#!/bin/bash

# Change working directory to /
cd ~

# Download the repository
curl -L -o repo.zip https://github.com/muysengly/repo_attendance_system_gtr/archive/refs/heads/main.zip

# Extract the downloaded zip file
unzip repo.zip

# Delete the zip file after extraction
# rm repo.zip

# Change directory to the extracted folder
cd repo_attendance_system-main

# Run setup.sh
# bash setup.sh
