[Setup]
AppName=BLACKPINK Auto Clicker
AppVersion=6.1.5
DefaultDirName={pf}\BLACKPINKAutoClicker
DefaultGroupName=BLACKPINKAutoClicker
OutputBaseFilename=BLACKPINKAutoClickerSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=dist\auto_clicker\_internal\images\lemon.ico
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
AppPublisher=BLACKPINK Team
AppCopyright=Copyright © 2025 BLACKPINK Team

[Files]
Source: "dist\auto_clicker\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\BLACKPINK Auto Clicker"; Filename: "{app}\auto_clicker.exe"; WorkingDir: "{app}"; IconFilename: "{app}\_internal\images\lemon.ico"
Name: "{commondesktop}\BLACKPINK Auto Clicker"; Filename: "{app}\auto_clicker.exe"; WorkingDir: "{app}"; IconFilename: "{app}\_internal\images\lemon.ico"; Tasks: desktopicon
Name: "{group}\Gỡ cài đặt BLACKPINK Auto Clicker"; Filename: "{uninstallexe}"

[Tasks]
Name: "desktopicon"; Description: "Tạo shortcut trên Desktop"; GroupDescription: "Tùy chọn shortcut:"; Flags: checkedonce

[Run]
Filename: "{app}\auto_clicker.exe"; Description: "Chạy BLACKPINK Auto Clicker"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\_internal"
Type: filesandordirs; Name: "{app}"