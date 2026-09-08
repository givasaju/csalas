<#
.SYNOPSIS
    Script de Provisionamento de Nova Instituição para ClassSync AI (Windows PowerShell).
.EXAMPLE
    .\scripts\deploy-institution.ps1 -Tenant "faculdade_alpha" -Port 8001
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Tenant,

    [Parameter(Mandatory = $true, Position = 1)]
    [int]$Port,

    [Parameter(Mandatory = $false, Position = 2)]
    [string]$DatabaseUrl = "sqlite:////app/data/classsync.db",

    [Parameter(Mandatory = $false)]
    [string]$MasterChefEmail,

    [Parameter(Mandatory = $false)]
    [string]$MasterChefPassword
)

$ErrorActionPreference = "Stop"


Write-Host "==> Provisionando instituição: $Tenant na porta $Port..." -ForegroundColor Cyan

# 1. Criar diretório de dados persistentes
$DataDir = "./data/$Tenant"
if (-not (Test-Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir -Force | Out-Null
}
Write-Host "  [OK] Diretório criado: $DataDir" -ForegroundColor Green

# 2. Gerar SECRET_KEY aleatória de 64 caracteres hexadecimais
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$bytes = New-Object byte[] 32
$rng.GetBytes($bytes)
$SecretKey = -join ($bytes | ForEach-Object { "{0:x2}" -f $_ })

# 3. Escrever arquivo de ambiente da instituição
$EnvFile = ".env.$Tenant"
$EnvContent = @"
TENANT_NAME=$Tenant
PORT=$Port
HOST=0.0.0.0
DATA_DIR=$DataDir
DATABASE_URL=$DatabaseUrl
SECRET_KEY=$SecretKey
APP_ENV=production
"@

Set-Content -Path $EnvFile -Value $EnvContent -Encoding utf8
Write-Host "  [OK] Arquivo gerado: $EnvFile" -ForegroundColor Green

# 4. Semear o master-chef no banco da instituição caso informado
if ($MasterChefEmail -and $MasterChefPassword) {
    Write-Host "==> Semeando Master-Chef ($MasterChefEmail) na base do tenant..." -ForegroundColor Cyan
    $DbPath = "$PWD/data/$Tenant/project.db"
    $pyCmd = @"
import os, sys
db_path = r'$DbPath'
os.environ['DATABASE_URL'] = 'sqlite:///' + db_path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, User
from src.api.auth import hash_password

engine = create_engine('sqlite:///' + db_path, connect_args={'check_same_thread': False})
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
s = Session()
try:
    u = s.query(User).filter(User.email == '$MasterChefEmail').first()
    if not u:
        u = User(
            id='u-$Tenant-master',
            name='Gestor Geral Institucional',
            email='$MasterChefEmail',
            password_hash=hash_password('$MasterChefPassword'),
            role='gestor',
            department='Administração Geral',
            is_active=True,
            must_change_password=True
        )
        s.add(u)
        s.commit()
finally:
    s.close()
"@
    python -c "$pyCmd"
    Write-Host "  [OK] Master-Chef provisionado com sucesso (must_change_password=True)." -ForegroundColor Green
}

# 5. Executar subida do container via Docker Compose se docker estiver disponível

if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "==> Inicializando container classsync-$Tenant via docker compose..." -ForegroundColor Cyan
    docker compose --project-name "classsync-$Tenant" --env-file "$EnvFile" up -d --build
    Write-Host "==> Sucesso! Instituição $Tenant iniciada em http://localhost:$Port/" -ForegroundColor Green
} else {
    Write-Host "==> Aviso: Docker não detectado no PATH do sistema." -ForegroundColor Yellow
    Write-Host "    A configuração $EnvFile e a pasta $DataDir foram criadas com sucesso." -ForegroundColor Yellow
    Write-Host "    Para rodar localmente sem container:" -ForegroundColor Gray
    Write-Host "    `$env:TENANT_NAME='$Tenant'; `$env:PORT=$Port; `$env:SECRET_KEY='$SecretKey'; python -m src.main" -ForegroundColor Gray
}
