@echo off
echo ============================================================
echo  TikTok Account Creator v7.0 - Playwright CDP
echo  Connects to YOUR Chrome with YOUR ProtonVPN
echo ============================================================
echo.
echo STEP 1: Starting Chrome with remote debugging...
echo.

REM Start Chrome in background with debugging enabled
start "" "%~dp0START_CHROME_DEBUG.bat"

echo Waiting 5 seconds for Chrome to start...
timeout /t 5 /nobreak >nul

echo.
echo ============================================================
echo STEP 2: Enable ProtonVPN in the Chrome window that opened
echo ============================================================
echo.
echo STEP 3: Press any key to start automation...
pause >nul

echo.
echo Starting TikTok Account Creator...
echo.

cd /d "%~dp0"
python core\run_playwright_chrome.py

pause
