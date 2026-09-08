<#
.SYNOPSIS
    Inicia todas as instâncias de instituições (tenants) configuradas no ClassSync AI.
.DESCRIPTION
    Varre os arquivos .env.<tenant> e inicializa instâncias locais caso não estejam respondendo.
.EXAMPLE
    .\scripts\start-all-tenants.ps1
#>

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   ClassSync AI - Gerenciador de Instâncias de Tenants" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# 1. Verificar porta 8001 (Instância Master / Global)
$MainOnline = $false
try {
    $tcp = New-Object System.Net.Sockets.TcpClient
    $tcp.Connect("127.0.0.1", 8001)
    $MainOnline = $true
    $tcp.Close()
} catch {
    $MainOnline = $false
}

if ($MainOnline) {
    Write-Host "[OK] Instância Principal (doctor-chef) ativa em: http://localhost:8001/" -ForegroundColor Green
} else {
    Write-Host "[AVISO] Instância Principal (8001) está OFFLINE." -ForegroundColor Yellow
    Write-Host "        Para iniciar: python -m src.main" -ForegroundColor Gray
}

# 2. Varrer arquivos .env.<tenant>
$EnvFiles = Get-ChildItem -Path $RootDir -Filter ".env.*" | Where-Object { 
    $_.Name -notlike "*.example" -and $_.Name -notlike "*.bak" 
}

if (-not $EnvFiles) {
    Write-Host "Nenhum arquivo de tenant (.env.<tenant>) encontrado." -ForegroundColor Gray
    exit 0
}

Write-Host "`nVerificando tenants configurados..." -ForegroundColor Cyan

foreach ($file in $EnvFiles) {
    $tenantSlug = $file.Name.Substring(5)
    $port = 8001
    $dataDir = "./data/$tenantSlug"
    $dbUrl = "sqlite:///./data/$tenantSlug/project.db"
    $secretKey = ""
    $appEnv = "production"

    Get-Content $file.FullName | ForEach-Object {
        $line = $_.Trim()
        if ($line -match "^PORT=(\d+)") { $port = [int]$matches[1] }
        if ($line -match "^DATA_DIR=(.+)") { $dataDir = $matches[1].Trim() }
        if ($line -match "^DATABASE_URL=(.+)") { $dbUrl = $matches[1].Trim() }
        if ($line -match "^SECRET_KEY=(.+)") { $secretKey = $matches[1].Trim() }
        if ($line -match "^APP_ENV=(.+)") { $appEnv = $matches[1].Trim() }
    }

    # Testar se a porta está online
    $isOnline = $false
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $client.Connect("127.0.0.1", $port)
        $isOnline = $true
        $client.Close()
    } catch {
        $isOnline = $false
    }

    if ($isOnline) {
        Write-Host "  -> Tenant '$tenantSlug' (porta $port): [ONLINE] em http://localhost:$port/" -ForegroundColor Green
    } else {
        Write-Host "  -> Tenant '$tenantSlug' (porta $port): [OFFLINE]. Iniciando processo em background..." -ForegroundColor Yellow
        
        $startInfo = New-Object System.Diagnostics.ProcessStartInfo
        $startInfo.FileName = "python"
        $startInfo.Arguments = "-m src.main"
        $startInfo.WorkingDirectory = $RootDir
        $startInfo.UseShellExecute = $false
        $startInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden

        # Variáveis de ambiente da instância
        $startInfo.EnvironmentVariables["TENANT_NAME"] = $tenantSlug
        $startInfo.EnvironmentVariables["PORT"] = "$port"
        $startInfo.EnvironmentVariables["DATABASE_URL"] = $dbUrl
        $startInfo.EnvironmentVariables["DATA_DIR"] = $dataDir
        $startInfo.EnvironmentVariables["SECRET_KEY"] = $secretKey
        $startInfo.EnvironmentVariables["APP_ENV"] = $appEnv

        [System.Diagnostics.Process]::Start($startInfo) | Out-Null
        Start-Sleep -Seconds 1

        # Re-testar
        try {
            $client2 = New-Object System.Net.Sockets.TcpClient
            $client2.Connect("127.0.0.1", $port)
            Write-Host "     [SUCESSO] Instância '$tenantSlug' agora está ONLINE em http://localhost:$port/" -ForegroundColor Green
            $client2.Close()
        } catch {
            Write-Host "     [AVISO] Instância iniciada em background, aguardando término de boot." -ForegroundColor Yellow
        }
    }
}

Write-Host "`nConcluído!" -ForegroundColor Cyan
