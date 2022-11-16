:: ccleaner-scripts
:: Whatever...
@echo off

:: UTF-8 Encoding
chcp 65001

cls

title CCleaner Script

:: Check file exists
if not exist "%~dp0CCleaner.exe" (
    echo CCleaner.exe not found!
    echo Please put this script in the same directory as CCleaner.exe
    pause
    exit
)

:: Check first run
if not exist "%~dp0Setup/config.def" (
    echo First run, please run CCleaner.exe first.
    echo Please modify the settings you want to use in Custom Clean.
    pause
    exit
)

:: Check CCleaner is running
tasklist /fi "imagename eq CCleaner.exe" | find /i "ccleaner.exe" >nul
if %errorlevel% equ 0 (
    echo CCleaner is running, please close it first.
    pause
    exit
)

:: Check CCleaner64 is running
tasklist /fi "imagename eq CCleaner64.exe" | find /i "ccleaner64.exe" >nul
if %errorlevel% equ 0 (
    echo CCleaner is running, please close it first.
    pause
    exit
)

:: Run CCleaner with AUTO mode
echo Running CCleaner...
start "" /wait "%~dp0CCleaner.exe" /AUTO
echo The Cleaning has been started.

pause
exit
