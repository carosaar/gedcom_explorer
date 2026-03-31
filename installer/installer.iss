[Code]
function GetLatestVersion: String;
var
  VersionURL: String;
begin
  VersionURL := 'https://github.com/carosaar/gedcom_explorer/version.txt';
  try
    Result := Trim(DownloadTemporaryFile(VersionURL));
  except
    Result := '';
  end;
end;

function CompareVersions(Current, Latest: String): Integer;
begin
  Result := CompareStr(Current, Latest);
end;

function InitializeSetup(): Boolean;
var
  Latest: String;
  Current: String;
begin
  Current := '1.3';  // Deine aktuelle Version
  Latest := GetLatestVersion;

  if Latest <> '' then begin
    if CompareVersions(Current, Latest) < 0 then begin
      MsgBox(
        'Es ist eine neuere Version verfügbar (' + Latest + ').' + #13#10 +
        'Du verwendest Version ' + Current + '.' + #13#10#13#10 +
        'Bitte lade die aktuelle Version herunter.',
        mbInformation, MB_OK
      );
    end;
  end;

  Result := True;
end;

[Setup]
AppName=GEDCOM Explorer
AppVersion=1.3
DefaultDirName={pf}\GEDCOM Explorer
DefaultGroupName=GEDCOM Explorer
OutputDir=output
OutputBaseFilename=GEDCOM_Explorer_Setup
Compression=lzma
SolidCompression=yes

; Optional
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