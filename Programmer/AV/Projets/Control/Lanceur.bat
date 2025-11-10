set "scriptPath=%~dp0"
Cd /d %scriptPath%
del a.txt
Nircmd win hide process "cmd.exe"
start /min QrCodepy.py
Timeout /2
Nircmd win hide process "python.exe"
:a
nircmd.exe savescreenshot "%scriptPath%a.jpg"
Timeout /t 1
Goto :a
