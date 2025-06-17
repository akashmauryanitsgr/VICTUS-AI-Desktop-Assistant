@echo off
setlocal enabledelayedexpansion

echo Disconnecting old connections...
adb disconnect

echo Restarting device in TCP mode on port 5555...
adb tcpip 5555

echo Waiting for device to initialize...
timeout /t 7 >nul

echo Detecting device IP...
FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^| find "inet "') DO set ipfull=%%G
FOR /F "tokens=1 delims=/" %%G in ("!ipfull!") DO set ip=%%G

echo Connecting to device with IP !ip!...
adb connect !ip!

echo Done.
pause
