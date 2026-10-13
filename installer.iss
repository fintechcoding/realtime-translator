; Inno Setup script for RealTime Translator
; Build the PyInstaller bundle first (dist\RealTimeTranslator\), then compile:
;   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
; Output: installer_output\RealTimeTranslator-Setup-<version>.exe

#define MyAppName "RealTime Translator"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "RealTime Translator"
#define MyAppExeName "RealTimeTranslator.exe"

[Setup]
AppId={{B6E9F4C2-7A3D-4E1B-9C5A-2F8D1A6E0B34}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=RealTimeTranslator-Setup-{#MyAppVersion}
SetupIconFile=app\gui\assets\app.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\RealTimeTranslator\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
