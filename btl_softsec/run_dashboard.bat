@echo off
setlocal
cd /d "%~dp0"
echo =================================================================
echo   SOFTSEC TOOLKIT - DASHBOARD STREAMLIT (DuongUniversity BTL)
echo =================================================================

set PY=python
if exist "%USERPROFILE%\anaconda3\python.exe" set PY=%USERPROFILE%\anaconda3\python.exe

"%PY%" -c "import streamlit, plotly, pandas" 2>nul
if errorlevel 1 (
    echo [CAI DAT] Thieu thu vien - dang cai streamlit plotly pandas...
    "%PY%" -m pip install streamlit plotly pandas
)

echo Mo trinh duyet tai http://localhost:8501  (Ctrl+C de dung)
"%PY%" -m streamlit run dashboard_streamlit.py --server.headless true --browser.gatherUsageStats false
endlocal
