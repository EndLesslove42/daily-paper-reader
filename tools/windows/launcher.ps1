param([ValidateSet('menu','admin','sync','sync-run','workflow','actions','status','update')][string]$Action = 'menu')
$ErrorActionPreference = 'Stop'
$Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
Set-Location -LiteralPath $Root
$env:PYTHONUTF8 = '1'
$Report = 'https://endlesslove42.github.io/daily-paper-reader/'
$Actions = 'https://github.com/EndLesslove42/daily-paper-reader/actions/workflows/daily-paper-reader.yml'
function Open-Link([string]$Url) { Start-Process $Url }
function Invoke-Git([string[]]$Arguments) {
    $result = & git @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Git $($Arguments[0]) 失败，请检查网络、登录和本地状态。" }
    return $result
}
function Get-Python {
    $python = Join-Path $Root '.venv\Scripts\python.exe'
    if (!(Test-Path -LiteralPath $python)) {
        Write-Host '正在创建 Python 虚拟环境...'
        if (Get-Command py -ErrorAction SilentlyContinue) { & py -3.12 -m venv .venv }
        if (!(Test-Path -LiteralPath $python)) {
            if (!(Get-Command python -ErrorAction SilentlyContinue)) { throw '未找到 Python，请安装 Python 3.12。' }
            & python -m venv .venv
        }
        if (!(Test-Path -LiteralPath $python)) { throw '创建虚拟环境失败。' }
    }
    $env:VIRTUAL_ENV = Join-Path $Root '.venv'
    $env:PATH = (Join-Path $Root '.venv\Scripts') + ';' + $env:PATH
    return $python
}
function File-Hash([string]$Path) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($Path))) } finally { $sha.Dispose() }
}
function Ensure-Dependencies([string]$Python) {
    # Management server uses only stdlib + PyYAML. Retrieval remains in existing Actions.
    $req = Join-Path $PSScriptRoot 'requirements-admin.txt'
    $hash = (File-Hash $req) + (File-Hash (Join-Path $Root 'requirements.txt')) + (File-Hash (Join-Path $Root 'src\local_debug_server.py'))
    $marker = Join-Path $Root '.venv\.deps_installed'
    if (!(Test-Path $marker) -or (Get-Content $marker -Raw).Trim() -ne $hash) {
        & $Python -m pip install -r $req
        if ($LASTEXITCODE -ne 0) { throw '后台依赖安装失败，请检查网络。' }
        [IO.File]::WriteAllText($marker, $hash)
    }
}
function Get-AdminState {
    try {
        $health = Invoke-RestMethod 'http://127.0.0.1:8567/api/local/health' -TimeoutSec 2
        if ($health.ok -and $health.mode -eq 'local-debug') {
            $config = Invoke-RestMethod 'http://127.0.0.1:8567/api/local/config' -TimeoutSec 2
            if ([IO.Path]::GetFullPath($config.path) -eq (Join-Path $Root 'config.yaml')) { return 'ours' }
        }
    } catch {}
    $listener = @([Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() | Where-Object { $_.Port -eq 8567 })
    if ($listener) { return 'other' }
    return 'stopped'
}
function Start-Admin {
    try {
        Invoke-Git @('fetch','origin') | Out-Null
        $behind = Invoke-Git @('rev-list','--count','HEAD..origin/main')
        if ([int]($behind | Select-Object -Last 1) -gt 0) {
            Write-Host 'GitHub 上有新的自动运行结果或项目更新。'
            $answer = [string](Read-Host '是否仍然继续启动后台？ [Y/N]')
            if ($answer -notmatch '^[yY]$') { return }
        }
    } catch { Write-Host '远端状态检查失败，将继续检查本地后台。' }
    $state = Get-AdminState
    if ($state -eq 'ours') { Open-Link 'http://127.0.0.1:8567'; Write-Host '后台已运行，直接打开。'; return }
    if ($state -eq 'other') { throw '8567 被其它服务或另一份仓库占用，未启动第二个后台。' }
    $python = Get-Python
    Ensure-Dependencies $python
    if (!(Test-Path '.env')) {
        Copy-Item -LiteralPath '.env.example' -Destination '.env'
        Write-Host '已创建 .env，请用编辑器填写 API Key；不会打印文件内容。'
    }
    New-Item -ItemType Directory -Path 'logs' -Force | Out-Null
    # Launch under a hidden PowerShell host so both streams share one append-only log.
    $hostScript = Join-Path $PSScriptRoot 'admin_host.ps1'
    Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',('"' + $hostScript + '"')) -WorkingDirectory $Root -WindowStyle Hidden
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Milliseconds 500
        if ((Get-AdminState) -eq 'ours') {
            Open-Link 'http://127.0.0.1:8567'
            Write-Host '后台已启动。日志: logs\local_admin.log'
            return
        }
    }
    throw '后台启动失败或超时，请检查 logs\local_admin.log。'
}
function Sync-Config {
    $python = Get-Python
    Ensure-Dependencies $python
    & $python (Join-Path $PSScriptRoot 'workflow.py') sync
    if ($LASTEXITCODE -ne 0) { throw '配置同步未完成；未触发工作流。请查看上方原因及备份目录。' }
}
function Run-Workflow {
    $available = $false
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        & gh auth status *> $null
        $available = $LASTEXITCODE -eq 0
    }
    if (!$available) {
        Open-Link $Actions
        Write-Host 'GitHub CLI 未安装或未登录，请在打开的页面手动点击 Run workflow。'
        return
    }
    $settings = Get-Content -LiteralPath (Join-Path $Root 'user_settings.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    # Read actual dispatch keys from the workflow's indentation, no unsupported input forwarding.
    $schema = Get-Content -LiteralPath (Join-Path $Root '.github\workflows\daily-paper-reader.yml') -Raw
    $allowed = @([regex]::Matches($schema, '(?m)^      ([a-z_]+):\s*$') | ForEach-Object { $_.Groups[1].Value })
    $arguments = @('workflow','run','daily-paper-reader.yml','--repo','EndLesslove42/daily-paper-reader','--ref','main')
    foreach ($property in $settings.PSObject.Properties) {
        if ($allowed -notcontains $property.Name) { throw "工作流不支持参数: $($property.Name)" }
        $value = [string]$property.Value
        if ($property.Name -eq 'fetch_days' -and $value -notmatch '^[1-9][0-9]*$') { throw 'fetch_days 必须为正整数。' }
        if ($property.Name -eq 'fetch_mode' -and $value -notin @('auto','standard','skims')) { throw 'fetch_mode 必须为 auto / standard / skims。' }
        if ($property.Name -eq 'run_enrich' -and $value -notin @('true','false')) { throw 'run_enrich 必须为 true 或 false。' }
        if ($value -match '[\r\n]' -or $value.Length -gt 256) { throw '运行参数格式不正确。' }
        if ($value) { $arguments += @('-f', ($property.Name + '=' + $value)) }
    }
    & gh @arguments
    if ($LASTEXITCODE -ne 0) { Write-Host '自动触发失败，请在 Actions 页面手动运行。' }
    else { Write-Host '已请求运行 daily-paper-reader 工作流，请查看 Actions 中的状态。' }
    Open-Link $Actions
}
function Show-Status {
    Write-Host "仓库: $Root"
    Write-Host ('分支: ' + (Invoke-Git @('branch','--show-current')))
    Write-Host ('提交: ' + (Invoke-Git @('rev-parse','--short','HEAD')))
    try {
        Invoke-Git @('fetch','origin') | Out-Null
        Write-Host ('origin/main 新增提交: ' + (Invoke-Git @('rev-list','--count','HEAD..origin/main')))
    } catch { Write-Host '远端状态未知（fetch 失败）。' }
    Write-Host ('config.yaml 状态: ' + ((Invoke-Git @('status','--short','--','config.yaml')) -join ' '))
    Write-Host ('secret.private 存在: ' + (Test-Path 'secret.private'))
    Write-Host ('.env 存在: ' + (Test-Path '.env'))
    Write-Host ('后台 / 8567: ' + (Get-AdminState))
    $installed = [bool](Get-Command gh -ErrorAction SilentlyContinue)
    Write-Host "GitHub CLI 已安装: $installed"
    if ($installed) { & gh auth status *> $null; Write-Host ('GitHub CLI 已登录: ' + ($LASTEXITCODE -eq 0)) }
}
function Execute([string]$Name) {
    switch ($Name) {
        'admin' { Start-Admin }
        'sync' { Sync-Config }
        'sync-run' { Sync-Config; Run-Workflow }
        'workflow' { Run-Workflow }
        'actions' { Open-Link $Actions }
        'status' { Show-Status }
        'update' {
            $python = Get-Python
            & $python (Join-Path $PSScriptRoot 'workflow.py') update
            if ($LASTEXITCODE -ne 0) { throw '更新未完成，请查看上方说明。' }
        }
    }
}
try {
    if ($Action -ne 'menu') { Execute $Action; exit 0 }
    while ($true) {
        Write-Host "`n========================================"
        Write-Host '        Daily Paper Reader'
        Write-Host '========================================'
        Write-Host '[1] 查看今日论文日报'
        Write-Host '[2] 打开后台管理'
        Write-Host '[3] 保存配置并运行论文检索'
        Write-Host '[4] 查看 GitHub Actions'
        Write-Host '[5] 更新 Daily Paper Reader'
        Write-Host '[6] 查看本地状态'
        Write-Host '[0] 退出'
        $choice = Read-Host '请选择'
        if ($choice -eq '0') { break }
        try {
            switch ($choice) {
                '1' { Open-Link $Report }
                '2' { Execute 'admin' }
                '3' { Execute 'sync-run' }
                '4' { Execute 'actions' }
                '5' { Execute 'update' }
                '6' { Execute 'status' }
                default { Write-Host '请输入 0 到 6。' }
            }
        } catch { Write-Host ('错误: ' + $_.Exception.Message) -ForegroundColor Red }
        Read-Host '按 Enter 返回菜单' | Out-Null
    }
} catch {
    Write-Host ('错误: ' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
