@echo off
setlocal
set "PATH=C:\Users\keert\AppData\Local\GitHubDesktop\app-3.6.7\resources\app\git\cmd;C:\Users\keert\AppData\Local\GitHubDesktop\app-3.6.7\resources\app\git\mingw64\bin;%PATH%"

echo ======================================================================
echo   RescueVision AI - Push to GitHub
echo   Target: https://github.com/chandanabh44/RescueVision-AI.git
echo   Branch: main
echo ======================================================================
echo.

git remote set-url origin https://github.com/chandanabh44/RescueVision-AI.git
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ======================================================================
    echo   [SUCCESS] Your project was successfully pushed to GitHub!
    echo   Repository URL: https://github.com/chandanabh44/RescueVision-AI
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo   [NOTICE] If a browser window opened, click 'Authorize' to complete
    echo   your GitHub login, then re-run this script.
    echo ======================================================================
)

echo.
pause
