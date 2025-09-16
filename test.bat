@echo off
REM Get current date and time as yyyymmddhhmmss format

REM Get date parts
set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%

REM Get time parts
set hour=%time:~0,2%
set minute=%time:~3,2%
set second=%time:~6,2%

REM Remove leading spaces from hour (for 0-9h)
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%

REM Combine into one variable
set datetime=%year%%month%%day%%hour%%minute%%second%

REM Example usage
echo %datetime%