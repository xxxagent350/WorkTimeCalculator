[Setup]
AppName=Work Time Analyser
AppVersion=1.3
DefaultDirName=C:\GOSoftwareCache
DisableDirPage=yes
DisableProgramGroupPage=yes
DisableWelcomePage=no
SetupIconFile=alpha_games_logo_v3.ico
PrivilegesRequired=lowest
OutputBaseFilename=WorkTimeAnalyser v1.3
Compression=lzma2
SolidCompression=yes
Uninstallable=no
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
UsePreviousAppDir=no

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
Source: "alpha_games_logo_v3.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "decryptor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "decryptor_associations_creator.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "main_menu.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "projects.pkl"; DestDir: "{app}"; Flags: ignoreversion
Source: "work_time_analyser.exe"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "{app}\installer.bat"; Flags: nowait; Description: "Завершение установки"; StatusMsg: "Запуск установщика..."

[Code]
var
  PasswordPage: TInputQueryWizardPage;
  LicensePage: TOutputMsgMemoWizardPage;

procedure InitializeWizard;
begin
  // Создаём страницу лицензии
  LicensePage := CreateOutputMsgMemoPage(wpWelcome,
    'Лицензионное соглашение', 'Пожалуйста, прочтите и примите условия',
    'Вы должны согласиться с условиями, чтобы продолжить установку.',
    '1) Поддерживаемые среды разработки: PyCharm, Unity, Microsoft Visual Studio 2022' + #13#10 +
    '2) Поблагодарите великодушного Lomi за безвозмездную разработку и распространение этого ПО' + #13#10 +
    '3) Альфа велика!' + #13#10 +
    '4) Кто попытается накрутить себе пару часиков тот лох');

  // Создаём страницу ввода пароля после лицензии
  PasswordPage := CreateInputQueryPage(LicensePage.ID,
    'Проверка лицензии', 'Введите пароль установки',
    'Установка защищена надёжным паролем. Не пытайтесь его угадать. Введите "alpha_velika" для продолжения');
  PasswordPage.Add('Пароль:', True);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;

  // Проверяем, что пользователь принял лицензию
  if CurPageID = LicensePage.ID then
  begin
    // Если пользователь нажал "Далее" без согласия, ничего не проверяем,
    // так как соглашение автоматически требует нажатия "Согласен"
  end;

  // Проверяем пароль
  if CurPageID = PasswordPage.ID then
  begin
    if PasswordPage.Values[0] <> 'alpha_velika' then
    begin
      MsgBox('Неверный пароль установки. Попробуйте снова.', mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  // Пропускаем все страницы, кроме приветствия, лицензии и пароля
  Result := (PageID <> wpWelcome) and (PageID <> LicensePage.ID) and (PageID <> PasswordPage.ID);
end;