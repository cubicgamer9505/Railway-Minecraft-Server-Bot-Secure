@echo off
title Minecraft Server Bot - 24/7 Mode
echo ========================================
echo Minecraft Server Bot - 24/7 Mode
echo ========================================
echo.

:start
echo [%date% %time%] Starting Minecraft Server Bot...
py simple_bot.py

echo.
echo [%date% %time%] Bot crashed or stopped. Restarting in 10 seconds...
echo Press Ctrl+C to stop completely
timeout /t 10 /nobreak > nul

goto start
