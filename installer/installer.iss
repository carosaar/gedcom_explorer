[Setup]
AppName=GEDCOM Explorer
AppVersion=1.3
DefaultDirName={pf}\GEDCOM Explorer
DefaultGroupName=GEDCOM Explorer
OutputDir=output
OutputBaseFilename=GEDCOM_Explorer_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=release\prg_logo.ico

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Files]
Source: "release\ged_explorer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "release\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "release\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\GEDCOM Explorer"; Filename: "{app}\ged_explorer.exe"
Name: "{commondesktop}\GEDCOM Explorer"; Filename: "{app}\ged_explorer.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Desktop-Verknüpfung erstellen"; GroupDescription: "Zusätzliche Aufgaben:"; Flags: unchecked

[Run]
Filename: "{app}\ged_explorer.exe"; Description: "GEDCOM Explorer starten"; Flags: nowait postinstall skipifsilent

