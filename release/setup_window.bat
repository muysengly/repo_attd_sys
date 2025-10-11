@echo off

@REM CPU intel


@REM download the repository
curl -L -o tmp.zip https://github.com/muysengly/repo_attd_sys/archive/refs/heads/main.zip


@REM unzip tmp.zip
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath 'tmp.zip' -DestinationPath '.' -Force"


set new_name=attendance_system


@REM rename the unzipped folder
IF EXIST "repo_attd_sys-main" (
    RENAME "repo_attd_sys-main" "%new_name%"
)


@REM delete tmp.zip
IF EXIST "tmp.zip" DEL /F /Q "tmp.zip"


@REM change directory to the application folder
cd %new_name%

@REM delete folder release
IF EXIST "release" rmdir /S /Q "release"

@REM delete .gitignore file
IF EXIST ".gitignore" DEL /F /Q ".gitignore"

@REM delete readme.md
IF EXIST "README.md" DEL /F /Q "README.md"

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
@REM if not exist venv python -m venv venv
@REM call venv\Scripts\activate.bat


@REM upgrade pip
@REM python.exe -m pip install --upgrade pip
pip install --upgrade pip


@REM install dependencies
pip install PyQt5==5.15.11 
pip install opencv-python==4.12.0.88
pip install insightface==0.7.3
pip install onnxruntime==1.19.2


@REM create run.vbs script to run the application in a hidden window
echo @echo off >> run.bat
@REM echo call venv\Scripts\activate >> run.bat
echo start /min cmd /c python Main.py >> run.bat

@REM show completion message
echo Setup completed. 


pause