# resize.ps1 - Resize the Talan maps for web display.
#
# Generates two reduced variants of each map in /assets/maps/:
#   display/  (2400px max width, quality 85) - for inline page display
#   thumbs/   (800px max width, quality 80)  - for previews / index thumbnails
#
# The originals stay untouched. Use whichever variant suits the page;
# the originals are kept for click-through to full-size.
#
# Requires ImageMagick: https://imagemagick.org/script/download.php
# (Choose the 'Windows Binary Release' installer; tick
#  'Add application directory to your system path' during install.)
#
# Run: powershell -ExecutionPolicy Bypass -File .\resize.ps1
# Or, from this directory:  .\resize.ps1

$ErrorActionPreference = 'Stop'

# Resolve paths relative to this script's location
$mapsDir = $PSScriptRoot
$displayDir = Join-Path $mapsDir 'display'
$thumbsDir = Join-Path $mapsDir 'thumbs'

# Check for ImageMagick
$magick = Get-Command magick -ErrorAction SilentlyContinue
if (-not $magick) {
    Write-Host "ERROR: ImageMagick is required but not found on PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "Install from: https://imagemagick.org/script/download.php"
    Write-Host "(Choose the 'Windows Binary Release' installer; make sure to tick"
    Write-Host " 'Add application directory to your system path' during install.)"
    exit 1
}

# Ensure output directories exist
New-Item -ItemType Directory -Force -Path $displayDir | Out-Null
New-Item -ItemType Directory -Force -Path $thumbsDir | Out-Null

# Maps to process
$maps = @('terrain.webp', 'kingdoms.webp', 'domains.webp')

Write-Host "Resizing Talan maps..." -ForegroundColor Cyan
Write-Host ""

$totalOrig = 0
$totalDisplay = 0
$totalThumb = 0

foreach ($map in $maps) {
    $inputPath = Join-Path $mapsDir $map
    if (-not (Test-Path $inputPath)) {
        Write-Host "  SKIP $map (not found)" -ForegroundColor Yellow
        continue
    }

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($map)
    $displayOut = Join-Path $displayDir "$baseName.webp"
    $thumbOut = Join-Path $thumbsDir "$baseName.webp"

    $origSize = (Get-Item $inputPath).Length
    $totalOrig += $origSize
    Write-Host ("  {0} ({1} MB)" -f $map, [math]::Round($origSize/1MB, 1))

    # Display version: 2400px max width, quality 85
    & magick $inputPath -resize '2400x>' -quality 85 -define webp:method=6 $displayOut
    if ($LASTEXITCODE -ne 0) { throw "magick failed on $map (display variant)" }
    $displaySize = (Get-Item $displayOut).Length
    $totalDisplay += $displaySize
    Write-Host ("    -> display/{0}.webp ({1} MB)" -f $baseName, [math]::Round($displaySize/1MB, 2))

    # Thumb version: 800px max width, quality 80
    & magick $inputPath -resize '800x>' -quality 80 -define webp:method=6 $thumbOut
    if ($LASTEXITCODE -ne 0) { throw "magick failed on $map (thumb variant)" }
    $thumbSize = (Get-Item $thumbOut).Length
    $totalThumb += $thumbSize
    Write-Host ("    -> thumbs/{0}.webp ({1} KB)" -f $baseName, [math]::Round($thumbSize/1KB, 0))
}

Write-Host ""
Write-Host "Done. Totals:" -ForegroundColor Green
Write-Host ("  Originals: {0} MB" -f [math]::Round($totalOrig/1MB, 1))
Write-Host ("  Display:   {0} MB" -f [math]::Round($totalDisplay/1MB, 1))
Write-Host ("  Thumbs:    {0} MB" -f [math]::Round($totalThumb/1MB, 2))
