@echo off
echo ============================================================
echo  TikTok Account Creator - Cleanup Script
echo  Version 7.0 - Removing Deprecated Files
echo ============================================================
echo.

REM Create archive directories
echo Creating archive directories...
if not exist "archive\v6_deprecated" mkdir "archive\v6_deprecated"
if not exist "archive\debug_screenshots" mkdir "archive\debug_screenshots"
if not exist "archive\unused" mkdir "archive\unused"

echo.
echo Moving deprecated scripts...
if exist "core\run_chrome_modern.py" move "core\run_chrome_modern.py" "archive\v6_deprecated\" >nul
if exist "core\run_edge_modern.py" move "core\run_edge_modern.py" "archive\v6_deprecated\" >nul
if exist "RUN_FRESH_PROFILE.py" move "RUN_FRESH_PROFILE.py" "archive\v6_deprecated\" >nul
if exist "RUN_WITH_MANUAL_VPN.py" move "RUN_WITH_MANUAL_VPN.py" "archive\v6_deprecated\" >nul
if exist "OPEN_YOUR_EDGE.bat" move "OPEN_YOUR_EDGE.bat" "archive\v6_deprecated\" >nul

echo Moving debug screenshots...
if exist "Screenshot 2025-11-13 195218.png" move "Screenshot 2025-11-13 195218.png" "archive\debug_screenshots\" >nul
if exist "Screenshot 2025-11-13 203921.png" move "Screenshot 2025-11-13 203921.png" "archive\debug_screenshots\" >nul
if exist "core\before_send_code.png" move "core\before_send_code.png" "archive\debug_screenshots\" >nul

echo Moving unused files...
if exist "proxy_config.json" move "proxy_config.json" "archive\unused\" >nul
if exist "proxy.gif" move "proxy.gif" "archive\unused\" >nul

echo Removing artifacts...
if exist "nul" del "nul" >nul 2>&1

echo Cleaning Python cache...
if exist "__pycache__" rmdir /S /Q "__pycache__" >nul 2>&1
if exist "core\__pycache__" rmdir /S /Q "core\__pycache__" >nul 2>&1

echo.
echo ============================================================
echo  Cleanup Complete!
echo ============================================================
echo.
echo Files moved to archive:
echo   - archive\v6_deprecated\     (old scripts)
echo   - archive\debug_screenshots\ (screenshots)
echo   - archive\unused\            (unused files)
echo.
echo Active v7.0 files remain in:
echo   - core\run_playwright_chrome.py
echo   - START_CHROME_DEBUG.bat
echo   - RUN_WITH_YOUR_CHROME.bat
echo   - test_chrome_connection.py
echo.
echo ============================================================
pause
