@echo off
:: Admin launch check
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Not admin launch, restarting...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)
echo Admin launch ok

:: Associations set
reg add "HKCR\.worktime" /ve /d "WorkTimeFile" /f
reg add "HKCR\WorkTimeFile\shell\open\command" /ve /d "\"%SystemDrive%\Program Files\WorkTimeAnalyser\decryptor.exe\" \"%%1\"" /f

echo *.worktime files associated successfully