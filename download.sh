#!/bin/bash

# Change working directory to home directory
cd ~

# Download the repository
# -L option allows curl to follow redirects
# -o option specifies the output file name
curl -L -o tmp.zip https://github.com/muysengly/repo_attendance_system_gtr/archive/refs/heads/main.zip

# Extract the downloaded zip file
unzip tmp.zip

# Delete the zip file after extraction
rm tmp.zip

# Change directory to the extracted folder
cd repo_attendance_system-main

# Change execution permission for run.sh
chmod +x run.sh
