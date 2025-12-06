@echo off
echo ========================================
echo Touch Window AI Agents - Dashboard
echo ========================================
echo.
echo Starting the Dashboard UI...
echo.
echo Dashboard will open at: http://localhost:8501
echo.
echo Make sure your agents are running first!
echo (Run start-local.bat in another terminal)
echo.
cd /d "%~dp0"
streamlit run dashboard.py --server.port 8501
pause
