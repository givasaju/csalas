<#
.SYNOPSIS
    Script de Backup Centralizado dos Volumes Multi-Tenant (Windows PowerShell).
.EXAMPLE
    .\scripts\backup-institutions.ps1 -BackupDir "./backups"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, Position = 0)]
    [string]$BackupDir = "./backups"
)

$ErrorActionPreference = "Stop"
$DataRoot = "./data"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

Write-Host "==> Iniciando backup centralizado de instituições em $BackupDir..." -ForegroundColor Cyan

if (-not (Test-Path $DataRoot)) {
    Write-Host "Diretório $DataRoot não encontrado. Nenhum dado a ser copiado." -ForegroundColor Yellow
    exit 0
}

$Tenants = Get-ChildItem -Path $DataRoot -Directory
if ($Tenants.Count -eq 0) {
    Write-Host "Nenhum diretório de tenant encontrado em $DataRoot." -ForegroundColor Yellow
    exit 0
}

foreach ($Tenant in $Tenants) {
    $TenantName = $Tenant.Name
    $ZipPath = Join-Path $BackupDir "backup_${TenantName}_${Timestamp}.zip"
    Write-Host "  -> Compactando dados da instituição: $TenantName..." -ForegroundColor Gray
    
    Compress-Archive -Path $Tenant.FullName -DestinationPath $ZipPath -Force
    $FileSize = (Get-Item $ZipPath).Length / 1KB
    Write-Host ("     [OK] Criado: {0} ({1:N2} KB)" -f $ZipPath, $FileSize) -ForegroundColor Green
}

Write-Host "==> Rotina de backup concluída com sucesso!" -ForegroundColor Cyan
