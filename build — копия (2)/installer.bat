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

cls
echo Installing, please WAIT, DONT CLOSE, IT CLOSES AUTOMATICLY

:: -1. Добавляем в исключения защитника windows папку распаковки и установки
powershell -Command "Add-MpPreference -ExclusionPath '%CD%'"
powershell -Command "Add-MpPreference -ExclusionPath 'C:\Program Files\WorkTimeAnalyser'"

:: 0. Пытаемся закрыть приложение, чтобы оно не мешало установке/обновлению
taskkill /F /IM work_time_analyser.exe 2>nul

cls
echo Installing, please WAIT, DONT CLOSE, IT CLOSES AUTOMATICLY

:: Определяем, установка это или обновление
set "IS_UPDATE=0"
if exist "%SystemDrive%\Program Files\WorkTimeAnalyser\" set "IS_UPDATE=1"

:: 1. Удаление содержимого папки WorkTimeAnalyser, но сохраняем нужные файлы при обновлении
if %IS_UPDATE%==0 (
    rd /s /q "%SystemDrive%\Program Files\WorkTimeAnalyser\" 2>nul
) else (
    echo Skipping deletion of existing user data...
    move /y "%SystemDrive%\Program Files\WorkTimeAnalyser\user_data.pkl" "%TEMP%\user_data.pkl" 2>nul
    move /y "%SystemDrive%\Program Files\WorkTimeAnalyser\projects.pkl" "%TEMP%\projects.pkl" 2>nul
    rd /s /q "%SystemDrive%\Program Files\WorkTimeAnalyser\" 2>nul
)

cls
echo Installing, please WAIT, DONT CLOSE, IT CLOSES AUTOMATICLY

timeout /t 1 >nul

:: 2.1. Создание папки и копирование файлов
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

:: Если это НЕ обновление, то копируем projects.pkl
if %IS_UPDATE%==0 (
    if exist "%ROOT_DIR%projects.pkl" copy /y "%ROOT_DIR%projects.pkl" "%SystemDrive%\Program Files\WorkTimeAnalyser\" >nul
)

:: Восстанавливаем файлы, если обновление
if %IS_UPDATE%==1 (
    move /y "%TEMP%\user_data.pkl" "%SystemDrive%\Program Files\WorkTimeAnalyser\" 2>nul
    move /y "%TEMP%\projects.pkl" "%SystemDrive%\Program Files\WorkTimeAnalyser\" 2>nul
)

cls
echo Installing, please WAIT, DONT CLOSE, IT CLOSES AUTOMATICLY

:: 2.2. Делаем все файлы в папке доступными для изменения
icacls "C:\Program Files\WorkTimeAnalyser" /grant "%USERNAME%":F /T /C /Q

cls
echo Installing, please WAIT, DONT CLOSE, IT CLOSES AUTOMATICLY

:: 3. Запуск ассоциаций
cd /d "%SystemDrive%\Program Files\WorkTimeAnalyser\"
call decryptor_associations_creator.bat
cd /d %~dp0

cls
echo Installing, please WAIT, DONT CLOSE, IT CLOSES AUTOMATICLY

:: 4. Создание ярлыков
set "SHORTCUT_NAME=Time Analyser Menu"
set "TARGET_PATH=%SystemDrive%\Program Files\WorkTimeAnalyser\main_menu.exe"

:: Для рабочего стола
powershell "$ws = New-Object -ComObject WScript.Shell; $lnk = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\%SHORTCUT_NAME%.lnk'); $lnk.TargetPath = '%TARGET_PATH%'; $lnk.Save()"

:: Для меню Пуск
powershell "$ws = New-Object -ComObject WScript.Shell; $lnk = $ws.CreateShortcut([Environment]::GetFolderPath('StartMenu') + '\Programs\%SHORTCUT_NAME%.lnk'); $lnk.TargetPath = '%TARGET_PATH%'; $lnk.Save()"

cls
echo Installing, please WAIT, DONT CLOSE, IT CLOSES AUTOMATICLY

:: 5. Настройка автозагрузки
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WorkTimeAnalyser" /t REG_SZ /d "\"%SystemDrive%\Program Files\WorkTimeAnalyser\work_time_analyser.exe\"" /f

cls

cd /d %SystemDrive%\

start "" "%SystemDrive%\Program Files\WorkTimeAnalyser\work_time_analyser.exe"

:: 6. Удаление кеша
set "TARGET=C:\GOSoftwareCache"

if exist "%TARGET%" (
    rmdir /s /q "%TARGET%"
)

echo Success
timeout /t 2 >nul
pause
