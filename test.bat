@echo off
REM === Set paths ===
set VENV_PATH=%~dp0venv\Scripts\activate.bat
set PROJECT_PATH=%~dp0
set MAIN_SCRIPT=Main.py
set SHORTCUT_NAME=run_window

REM === Shortcut target command ===
set TARGET=cmd /k "call %VENV_PATH% && python %PROJECT_PATH%\%MAIN_SCRIPT%"

REM === Shortcut location (Desktop) ===
set SHORTCUT_PATH=%~dp0%SHORTCUT_NAME%.lnk

REM === Create shortcut using PowerShell ===
powershell -command ^
  "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%'); ^
   $s.TargetPath='cmd.exe'; ^
   $s.Arguments='/k %TARGET%'; ^
   $s.WorkingDirectory='%PROJECT_PATH%'; ^
   $s.IconLocation='cmd.exe,0'; ^
   $s.Save()"

echo Shortcut created: %SHORTCUT_PATH%
pause
