# Inicia el servidor local y abre el sitio. Ejecutar desde PowerShell.
$ErrorActionPreference = 'Stop'
$projectPath = $PSScriptRoot
$pythonPath = Join-Path $projectPath '.venv/Scripts/pythonw.exe'
$siteUrl = 'http://127.0.0.1:5000'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Falta el entorno .venv. Segui la instalacion del README.'
}
if (-not (Test-Path -LiteralPath (Join-Path $projectPath '.env'))) {
    throw 'Falta el archivo .env con la configuracion MySQL.'
}
$alreadyRunning = $false
try {
    $response = Invoke-WebRequest -Uri "$siteUrl/api/categorias" -TimeoutSec 2
    $alreadyRunning = $response.StatusCode -eq 200
} catch { }
if (-not $alreadyRunning) {
    $logPath = Join-Path $projectPath 'logs'
    New-Item -ItemType Directory -Force -Path $logPath | Out-Null
    Start-Process -FilePath $pythonPath -ArgumentList @('-m', 'flask', '--app', 'app', 'run', '--host', '127.0.0.1', '--port', '5000') -WorkingDirectory $projectPath -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logPath 'servidor.log') -RedirectStandardError (Join-Path $logPath 'errores.log') | Out-Null
    $ready = $false
    for ($attempt = 0; $attempt -lt 15; $attempt++) {
        try {
            $response = Invoke-WebRequest -Uri "$siteUrl/api/categorias" -TimeoutSec 2
            if ($response.StatusCode -eq 200) { $ready = $true; break }
        } catch { Start-Sleep -Milliseconds 500 }
    }
    if (-not $ready) { throw 'No se pudo iniciar el sitio. Revisa MySQL, .env y logs/errores.log.' }
}
Start-Process $siteUrl
Write-Output "Raiz Celeste disponible en $siteUrl"
