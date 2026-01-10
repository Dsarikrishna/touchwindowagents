@echo off
echo ========================================
echo Triggering All AI Agents
echo ========================================
echo.

set agents=ProductAgent CompetitionMinderAgent CustomerMinderAgent EfficiencyAgent SupplierMinderAgent OrderProcessingAgent

setlocal enabledelayedexpansion
for %%a in (%agents%) do (
    echo Triggering %%a...
    set "code="
    for /f "delims=" %%c in ('curl -s -w "%%{http_code}" -X POST "http://localhost:7071/api/Trigger%%a" -H "Content-Type: application/json" -d "{}" -o nul') do set "code=%%c"
    if "!code!"=="200" (
        echo   %%a: Triggered successfully!
    ) else (
        echo   %%a: Failed to trigger (status !code!)
    )
)
endlocal

echo.
echo All agents triggered! Check the func console for execution logs.
pause
