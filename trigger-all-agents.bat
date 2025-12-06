@echo off
echo ========================================
echo Triggering All AI Agents
echo ========================================
echo.

set agents=ProductAgent CompetitionMinderAgent CustomerMinderAgent EfficiencyAgent SupplierMinderAgent OrderProcessingAgent

for %%a in (%agents%) do (
    echo Triggering %%a...
    curl -s -X POST "http://localhost:7071/admin/functions/%%a" -H "Content-Type: application/json" -d "{}" > nul
    if %errorlevel% == 0 (
        echo   %%a: Triggered successfully!
    ) else (
        echo   %%a: Failed to trigger
    )
)

echo.
echo All agents triggered! Check the func console for execution logs.
pause
