[Setup]
AppName=MedVoice
AppVersion=1.0
DefaultDirName={autopf}\MedVoice
DefaultGroupName=MedVoice
OutputDir=output
OutputBaseFilename=MedVoiceInstaller
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Файли бекенду
Source: "backend\dist\MedVoice-Server-CLI\*"; DestDir: "{app}\backend"; Flags: ignoreversion recursesubdirs createallsubdirs

; Файли GUI (Tauri)
Source: "gui\src-tauri\target\release\*"; DestDir: "{app}\gui"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Ярлик на GUI
Name: "{group}\MedVoice GUI"; Filename: "{app}\gui\med-voice.exe"

; Ярлик на бекенд (опціонально, якщо має бути CLI)
Name: "{group}\MedVoice CLI"; Filename: "{app}\backend\MedVoice-Server-CLI.exe"

; Uninstall
Name: "{group}\Uninstall MedVoice"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\gui\med-voice.exe"; Description: "Запустити MedVoice"; Flags: nowait postinstall skipifsilent
