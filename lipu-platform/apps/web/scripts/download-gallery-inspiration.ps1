# Download Pinterest-style home inspiration photos for the gallery
# Source: config/gallery-inspiration-map.json
$ErrorActionPreference = 'Stop'
$root = Join-Path (Join-Path (Split-Path $PSScriptRoot -Parent) 'public') 'images\inspiration'
$configPath = Join-Path (Join-Path (Split-Path $PSScriptRoot -Parent) 'config') 'gallery-inspiration-map.json'
$config = Get-Content $configPath -Raw | ConvertFrom-Json

$count = 0
foreach ($category in $config.categories) {
  $catDir = Join-Path $root $category.slug
  if (-not (Test-Path $catDir)) { New-Item -ItemType Directory -Path $catDir -Force | Out-Null }

  foreach ($photo in $category.photos) {
    $dest = Join-Path $catDir $photo.file
    $url = "https://images.pexels.com/photos/$($photo.pexelsId)/pexels-photo-$($photo.pexelsId).jpeg?auto=compress&cs=tinysrgb&w=1920"
    Write-Host "Downloading $($category.slug)/$($photo.file)..."
    Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
    Start-Sleep -Milliseconds 250
    $count++
  }
}

Write-Host "Done. $count inspiration photos saved to $root"
