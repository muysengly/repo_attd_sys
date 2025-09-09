@echo off


@REM download the repository
curl -L -o tmp.zip https://github.com/muysengly/repo_attd_sys/archive/refs/heads/main.zip


@REM unzip tmp.zip
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath 'tmp.zip' -DestinationPath '.' -Force"


@REM rename the unzipped folder to attd_system_app
IF EXIST "repo_attd_sys-main" (
    RENAME "repo_attd_sys-main" "attd_system_app"
)


@REM delete tmp.zip
IF EXIST "tmp.zip" DEL /F /Q "tmp.zip"


@REM change directory to the application folder
cd attd_system_app


@REM check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)


@REM check if pip is installed
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Please install pip and try again.
    pause
    exit /b 1
)


@REM create and activate virtual environment
if not exist venv python -m venv venv
call venv\Scripts\activate.bat


@REM upgrade pip
python.exe -m pip install --upgrade pip


@REM install dependencies
pip install pyqt5 opencv-python insightface onnxruntime


@REM create a shortcut to run the application from run_window.vbs as ink file
@REM echo Set oWS = WScript.CreateObject("WScript.Shell") > run_window.vbs
@REM echo sLinkFile = "%USERPROFILE%\Desktop\Attendance System.lnk" >> run_window.vbs
@REM echo Set oLink = oWS.CreateShortcut(sLinkFile) >> run_window.vbs
@REM echo oLink.TargetPath = "%CD%\venv\Scripts\python.exe" >> run_window.vbs
@REM echo oLink.Arguments = "%CD%\main.py" >> run_window.vbs 
@REM echo oLink.WorkingDirectory = "%CD%" >> run_window.vbs
@REM echo oLink.WindowStyle = 1 >> run_window.vbs
@REM echo oLink.IconLocation = "%CD%\icon.ico" >> run_window.vbs
@REM echo oLink.Description = "Attendance System Application" >> run_window.vbs
@REM echo oLink.Save >> run_window.vbs
@REM echo A shortcut to the application has been created on your Desktop.


@REM show completion message
echo Setup completed. You can now run the application using win_run.vbs
pause