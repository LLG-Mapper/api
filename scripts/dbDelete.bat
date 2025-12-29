@echo off
REM Get the folder where this script is located
SET SCRIPT_DIR=%~dp0

REM Delete migrations and instance folders relative to the script
rmdir /s /q "%SCRIPT_DIR%\..\migrations"
rmdir /s /q "%SCRIPT_DIR%\..\instance"

echo Deleted migrations and instance folders.