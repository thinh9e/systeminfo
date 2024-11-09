@echo off

set WORKPLACE=%cd%
set SOURCE=%WORKPLACE%\src
set BUILD_DIR=%WORKPLACE%\build
set DIST_DIR=%WORKPLACE%\dist
set CLIENT=client
set SERVER=server

if "%~1"=="clean" goto CLEAN

if exist %DIST_DIR% rmdir /s/q %DIST_DIR%
echo Build SERVER ...
call pyinstaller --onefile %SOURCE%\%SERVER%.py
if %ERRORLEVEL% neq 0 goto ERROR

echo Build CLIENT ...
call pyinstaller --onefile %SOURCE%\%CLIENT%.py
if %ERRORLEVEL% neq 0 goto ERROR

if not exist %DIST_DIR% goto ERROR
xcopy /i hosts_exp.txt %DIST_DIR%

if %ERRORLEVEL% neq 0 goto ERROR
goto SUCCESS

:CLEAN
if exist %BUILD_DIR% rmdir /s/q %BUILD_DIR%
if exist %DIST_DIR% rmdir /s/q %DIST_DIR%
if exist %SERVER%.spec del %SERVER%.spec
if exist %CLIENT%.spec del %CLIENT%.spec
goto EXIT

:SUCCESS
echo Successfully!
goto EXIT

:ERROR
echo Error!
goto EXIT

:EXIT
