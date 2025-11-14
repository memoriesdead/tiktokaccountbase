@echo off
echo ============================================================
echo  Starting Chrome with Remote Debugging
echo ============================================================
echo.
echo Chrome will start on port 9222 for automation
echo Keep this window open while running the script
echo.
echo ============================================================

REM Create custom profile directory if it doesn't exist
set CHROME_PROFILE=%USERPROFILE%\ChromeDebugProfile
if not exist "%CHROME_PROFILE%" mkdir "%CHROME_PROFILE%"

REM Start Chrome with remote debugging (REQUIRED for Chrome 136+)
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%CHROME_PROFILE%" --no-first-run --no-default-browser-check

echo.
echo Chrome closed. You can close this window.
pause
