@echo off
:: Admin launch check
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Not admin launch, restarting...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: Main
echo Admin launch ok

set DECRYPTOR_PATH="C:\PythonProjects\WorkTimeCalculator\WorkTimeDecoder\dist\decryptor.exe"

:: Associations set
reg add "HKCR\.worktime" /ve /d "WorkTimeFile" /f
reg add "HKCR\WorkTimeFile\shell\open\command" /ve /d "\"%DECRYPTOR_PATH%\" \"%%1\"" /f

echo *.worktime files associated successfully
pause
