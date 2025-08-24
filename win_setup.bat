@echo off


@REM Change working directory
cd %USERPROFILE%


@REM Download the repository
curl -L -o tmp.zip https://github.com/muysengly/repo_attendance_system/archive/refs/heads/main.zip


@REM Extract the downloaded zip file
tar -xf tmp.zip


@REM Delete the zip file after extraction
del tmp.zip


@REM Change directory to the extracted folder
cd repo_attendance_system-main


@REM install dependencies
pip install pyqt5 opencv-python insightface onnxruntime


@REM Copy shortcut to desktop
copy "%USERPROFILE%\repo_attendance_system-main\resource\utility\Attendance System.lnk" "%USERPROFILE%\Desktop\Attendance System.lnk"


pause