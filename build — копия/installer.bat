@echo off
setlocal enabledelayedexpansion

:: Сохраняем текущий путь
set "ROOT_DIR=%~dp0"

:: Проверка прав администратора
fltmc >nul 2>&1 || (
    echo Not admin launch, restarting...
    powershell -Command "Start-Process -FilePath '%0' -Verb RunAs -WorkingDirectory '%ROOT_DIR:\=\\%'"
    exit /b
)
echo Admin launch ok

:: 1. Удаление содержимого папки WorkTimeAnalyser
cls
echo "|                    |  0 %%"
if exist "%SystemDrive%\Program Files\WorkTimeAnalyser\" (
    rd /s /q "%SystemDrive%\Program Files\WorkTimeAnalyser\"
    timeout /t 1 >nul
)

:: 2.1. Создание папки и копирование файлов
cls
echo "|----                |  20 %%"
md "%SystemDrive%\Program Files\WorkTimeAnalyser\" 2>nul

for %%f in (
    "alpha_games_logo_v3.ico"
    "decryptor.exe"
    "decryptor_associations_creator.bat"
    "main_menu.exe"
    "work_time_analyser.exe"
) do (
    if exist "%ROOT_DIR%%%~f" (
        copy /y "%ROOT_DIR%%%~f" "%SystemDrive%\Program Files\WorkTimeAnalyser\" >nul
    ) else (
        echo Error: file %%~f not found in %ROOT_DIR%!
        pause
        exit /b
    )
)

:: 2.2. Делаем все файлы в папке доступными для изменения
cls
echo "|--------            |  40 %%"
icacls "C:\Program Files\WorkTimeAnalyser" /grant "%USERNAME%":F /T /C /Q

:: 3. Запуск ассоциаций
cls
echo "|----------          |  50 %%"
cd /d "%SystemDrive%\Program Files\WorkTimeAnalyser\"
call decryptor_associations_creator.bat
cd /d %~dp0

:: 4. Создание ярлыков
cls
echo "|------------        |  60 %%"
set "SHORTCUT_NAME=Time Analyser Menu"
set "TARGET_PATH=%SystemDrive%\Program Files\WorkTimeAnalyser\main_menu.exe"

:: Для рабочего стола
powershell "$ws = New-Object -ComObject WScript.Shell; $lnk = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\%SHORTCUT_NAME%.lnk'); $lnk.TargetPath = '%TARGET_PATH%'; $lnk.Save()"

cls
echo "|--------------      |  70 %%"

:: Для меню Пуск
powershell "$ws = New-Object -ComObject WScript.Shell; $lnk = $ws.CreateShortcut([Environment]::GetFolderPath('StartMenu') + '\Programs\%SHORTCUT_NAME%.lnk'); $lnk.TargetPath = '%TARGET_PATH%'; $lnk.Save()"

:: 5. Настройка автозагрузки
cls
echo "|----------------    |  80 %%"
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WorkTimeAnalyser" /t REG_SZ /d "\"%SystemDrive%\Program Files\WorkTimeAnalyser\work_time_analyser.exe\"" /f

timeout /t 1 >nul

cls
echo "|--------------------|  100 %%  Success"

timeout /t 2 >nul

cls
echo "Restart your PC to run program"
pause

:: Удаление файлов и самого батника
for %%f in (
    "alpha_games_logo_v3.ico"
    "decryptor.exe"
    "decryptor_associations_creator.bat"
    "main_menu.exe"
    "work_time_analyser.exe"
) do (
    if exist "%ROOT_DIR%%%~f" del /f /q "%ROOT_DIR%%%~f"
)

del /f /q "%~f0"
