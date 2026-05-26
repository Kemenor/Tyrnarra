$port = 8008
$inUse = $false
try {
    Invoke-WebRequest "http://127.0.0.1:$port/" -UseBasicParsing -TimeoutSec 1 | Out-Null
    $inUse = $true
} catch {}

if ($inUse) {
    Write-Host "[serve] Port $port already serving; reusing existing server."
    while ($true) { Start-Sleep -Seconds 3600 }
} else {
    Write-Host "[serve] Starting live-server on port $port."
    & npx --yes live-server "--port=$port" "--ignore=lore/**,.git/**,outputs/**"
}
