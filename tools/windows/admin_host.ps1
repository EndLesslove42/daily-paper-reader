$ErrorActionPreference = 'Stop'
$Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
Set-Location -LiteralPath $Root
$env:PYTHONUTF8 = '1'
# One host per Windows session/port. The mutex remains held throughout server lifetime.
$mutex = New-Object Threading.Mutex($false, 'Local\DailyPaperReaderAdmin8567')
$owned = $false
try {
    try { $owned = $mutex.WaitOne(0) } catch [Threading.AbandonedMutexException] { $owned = $true }
    if (!$owned) { exit 0 }
    $ErrorActionPreference = 'Continue'
    & (Join-Path $Root '.venv\Scripts\python.exe') -u (Join-Path $Root 'src\local_debug_server.py') --host 127.0.0.1 --port 8567 >> (Join-Path $Root 'logs\local_admin.log') 2>&1
} finally {
    if ($owned) { $mutex.ReleaseMutex() }
    $mutex.Dispose()
}
