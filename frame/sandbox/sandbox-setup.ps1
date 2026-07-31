# Prepara o Windows Sandbox para testar o Mirror Frame.
# O repo do host entra SOMENTE-LEITURA; tudo é copiado para dentro do sandbox,
# então nenhuma escrita (venv, .env, banco) toca a máquina real.
$ErrorActionPreference = 'Continue'
$src  = "$env:USERPROFILE\Desktop\mirror-exe"
$repo = "C:\MirrorTest"
$app  = "C:\MirrorFrame"

Write-Host "== Mirror Frame — preparação do sandbox ==" -ForegroundColor Cyan
Write-Host "Copiando o repositório (sem pesados)..."
robocopy $src $repo /E /XD "$src\.venv" "$src\frame\node_modules" "$src\frame\out" /NFL /NDL /NJH /NJS | Out-Null

Write-Host "Copiando o app empacotado..."
robocopy "$src\frame\out\MirrorFrame-win32-x64" $app /E /NFL /NDL /NJH /NJS | Out-Null

# Relançador que relê o PATH do registro — necessário depois do bootstrap
# instalar git/node/uv/pi (o processo antigo não enxerga PATH novo).
$cmd = @'
@echo off
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USERPATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "SYSPATH=%%b"
set "PATH=%SYSPATH%;%USERPATH%"
set "MIRROR_FRAME_ROOT=C:\MirrorTest"
start "" "C:\MirrorFrame\MirrorFrame.exe"
'@
Set-Content -Path "$env:USERPROFILE\Desktop\Mirror Frame.cmd" -Value $cmd -Encoding Ascii

[Environment]::SetEnvironmentVariable("MIRROR_FRAME_ROOT", $repo, "User")
$env:MIRROR_FRAME_ROOT = $repo

Write-Host "Abrindo o Mirror Frame..." -ForegroundColor Green
Start-Process "$app\MirrorFrame.exe"
Write-Host ""
Write-Host "Roteiro: Setup (luzes vermelhas) -> Instalar pré-requisitos (bootstrap)"
Write-Host "-> fechar o app -> reabrir pelo atalho 'Mirror Frame' na área de trabalho."
