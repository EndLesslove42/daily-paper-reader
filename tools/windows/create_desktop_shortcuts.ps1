$ErrorActionPreference = 'Stop'
$Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$Desktop = [Environment]::GetFolderPath('Desktop')
$Shell = New-Object -ComObject WScript.Shell
foreach ($entry in @(
    @{ Name = 'Daily Paper Reader'; Target = 'DailyPaperReader.cmd'; Style = 1 },
    @{ Name = 'Daily Paper Reader - 今日论文'; Target = 'tools\windows\open_report.cmd'; Style = 7 }
)) {
    $Shortcut = $Shell.CreateShortcut((Join-Path $Desktop ($entry.Name + '.lnk')))
    $Shortcut.TargetPath = Join-Path $Root $entry.Target
    $Shortcut.WorkingDirectory = $Root
    $Shortcut.WindowStyle = $entry.Style
    $Shortcut.Save()
    Write-Host ('已创建: ' + $entry.Name)
}
