@echo off


@REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)


@REM Check if pip is installed
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


echo Setup completed. You can now run the application using win_run.vbs


pause
