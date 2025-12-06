@echo off
echo ========================================
echo Touch Window AI Agents - Local Runner
echo ========================================
echo.

REM Start Azurite in background
echo Starting Azurite (Azure Storage Emulator)...
start /B npx azurite --silent --location "%~dp0.azurite" --blobPort 10000 --queuePort 10001 --tablePort 10002

REM Wait for Azurite to start
timeout /t 3 /nobreak > nul

echo Starting Azure Functions...
echo.
cd /d "%~dp0"
func start

pause
