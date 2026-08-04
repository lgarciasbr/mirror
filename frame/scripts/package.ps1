# Empacota o Mirror Frame portatil em out\MirrorFrame-win32-x64.
# Substitui o electron-packager (cuja extracao de zip falha nesta maquina) por
# uma montagem deterministica: dist do Electron + resources\app com o codigo e
# SOMENTE as dependencias de runtime - incluindo os pacotes binários de
# plataforma do node-pty (a ausencia deles quebrou a primeira rodada real).
[CmdletBinding()]
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$frame = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$out = Join-Path $frame 'out\MirrorFrame-win32-x64'
$dist = Join-Path $frame 'node_modules\electron\dist'
if (-not (Test-Path (Join-Path $dist 'electron.exe'))) {
    throw "Electron dist ausente em $dist - rode npm install e valide o binário."
}

Write-Host "Base Electron..." -ForegroundColor Cyan
robocopy $dist $out /E /PURGE /NFL /NDL /NJH /NJS | Out-Null
if (Test-Path (Join-Path $out 'electron.exe')) {
    Move-Item (Join-Path $out 'electron.exe') (Join-Path $out 'MirrorFrame.exe') -Force
}

$app = Join-Path $out 'resources\app'
New-Item -ItemType Directory -Force $app | Out-Null
Copy-Item (Join-Path $frame 'package.json') $app -Force
Copy-Item (Join-Path $frame 'preload.js') $app -Force
foreach ($dir in @('main', 'renderer', 'assets')) {
    robocopy (Join-Path $frame $dir) (Join-Path $app $dir) /E /NFL /NDL /NJH /NJS | Out-Null
}

Write-Host "Dependencias de runtime (todas as entradas de @lydell e @xterm)..." -ForegroundColor Cyan
foreach ($scope in @('@lydell', '@xterm')) {
    $src = Join-Path $frame "node_modules\$scope"
    Get-ChildItem $src -Directory | ForEach-Object {
        robocopy $_.FullName (Join-Path $app "node_modules\$scope\$($_.Name)") /E /NFL /NDL /NJH /NJS | Out-Null
    }
}

# Validacao NAO acontece aqui: a fonte unica dos asserts e
# scripts\verify-payload.ps1, executado UMA vez por cadeia de build
# (package -> verify -> ISCC) pelo installer\build.ps1 e pelo CI.
$mb = [math]::Round((Get-ChildItem $out -Recurse | Measure-Object Length -Sum).Sum / 1MB)
Write-Host "package OK: $out ($mb MB). Valide com scripts\verify-payload.ps1." -ForegroundColor Green
