# Download Odisha/India-compliant architecture photos into public/images/
# Selection rules: image-guidelines.md
$ErrorActionPreference = 'Stop'
$root = Join-Path (Join-Path (Split-Path $PSScriptRoot -Parent) 'public') 'images'

$detail = 'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?auto=format&fit=crop&w=1920&q=85'

# path => download URL (Pexels India-tagged + product detail macro)
$map = [ordered]@{
  'hero/main.jpg'                    = 'https://images.pexels.com/photos/9285535/pexels-photo-9285535.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'hero/transformation.jpg'          = 'https://images.pexels.com/photos/14002095/pexels-photo-14002095.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'hero/editorial-strip.jpg'         = 'https://images.pexels.com/photos/33034471/pexels-photo-33034471.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'projects/coastal-residence.jpg'   = 'https://images.pexels.com/photos/38179316/pexels-photo-38179316.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'projects/skyline-penthouse.jpg'   = 'https://images.pexels.com/photos/37334792/pexels-photo-37334792.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'projects/heritage-revival.jpg'    = 'https://images.pexels.com/photos/35114454/pexels-photo-35114454.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'projects/lonavala-retreat.jpg'    = 'https://images.pexels.com/photos/35361412/pexels-photo-35361412.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'projects/goa-villa.jpg'           = 'https://images.pexels.com/photos/35361412/pexels-photo-35361412.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'projects/corporate-lobby.jpg'     = 'https://images.pexels.com/photos/34725805/pexels-photo-34725805.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'before-after/bandra-before.jpg'   = 'https://images.pexels.com/photos/35114454/pexels-photo-35114454.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'before-after/bandra-after.jpg'    = 'https://images.pexels.com/photos/9285535/pexels-photo-9285535.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'before-after/lonavala-before.jpg' = 'https://images.pexels.com/photos/2806377/pexels-photo-2806377.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'before-after/lonavala-after.jpg'  = 'https://images.pexels.com/photos/14002095/pexels-photo-14002095.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'before-after/pune-before.jpg'     = 'https://images.pexels.com/photos/33034471/pexels-photo-33034471.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'before-after/pune-after.jpg'      = 'https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'design/modern-minimal.jpg'        = 'https://images.pexels.com/photos/14002095/pexels-photo-14002095.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'design/european-classic.jpg'      = 'https://images.pexels.com/photos/33034471/pexels-photo-33034471.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'design/coastal-resilient.jpg'     = 'https://images.pexels.com/photos/38179316/pexels-photo-38179316.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'design/tropical-open.jpg'         = 'https://images.pexels.com/photos/35361412/pexels-photo-35361412.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/horizon-sliding.jpg'     = 'https://images.pexels.com/photos/9285535/pexels-photo-9285535.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/horizon-detail.jpg'      = $detail
  'products/atelier-casement.jpg'    = 'https://images.pexels.com/photos/35114454/pexels-photo-35114454.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/atelier-detail.jpg'      = $detail
  'products/grand-entrance.jpg'      = 'https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/grand-detail.jpg'        = $detail
  'products/garden-portal.jpg'       = 'https://images.pexels.com/photos/35361412/pexels-photo-35361412.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/garden-detail.jpg'       = 'https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/facade-system.jpg'       = 'https://images.pexels.com/photos/34725823/pexels-photo-34725823.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/facade-detail.jpg'       = 'https://images.pexels.com/photos/34725805/pexels-photo-34725805.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/skyline-fixed.jpg'       = 'https://images.pexels.com/photos/37334792/pexels-photo-37334792.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'products/skyline-detail.jpg'      = $detail
  'gallery/morning-light.jpg'        = 'https://images.pexels.com/photos/14002095/pexels-photo-14002095.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/garden-portal.jpg'        = 'https://images.pexels.com/photos/35361412/pexels-photo-35361412.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/urban-edge.jpg'           = 'https://images.pexels.com/photos/36245020/pexels-photo-36245020.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/monsoon-calm.jpg'         = 'https://images.pexels.com/photos/9285535/pexels-photo-9285535.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/courtyard-frame.jpg'      = 'https://images.pexels.com/photos/33034471/pexels-photo-33034471.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/dusk-silhouette.jpg'      = 'https://images.pexels.com/photos/33034471/pexels-photo-33034471.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/profile-detail.jpg'       = $detail
  'gallery/stairwell-light.jpg'      = 'https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/sea-horizon.jpg'          = 'https://images.pexels.com/photos/38179316/pexels-photo-38179316.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/minimal-bedroom.jpg'      = 'https://images.pexels.com/photos/14002095/pexels-photo-14002095.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/villa-pool.jpg'           = 'https://images.pexels.com/photos/35361412/pexels-photo-35361412.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'gallery/city-penthouse.jpg'       = 'https://images.pexels.com/photos/37834156/pexels-photo-37834156.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'about/craft.jpg'                  = $detail
  'about/studio.jpg'                 = 'https://images.pexels.com/photos/1115800/pexels-photo-1115800.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'about/manifesto.jpg'              = 'https://images.pexels.com/photos/9285535/pexels-photo-9285535.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'team/aditya.jpg'                  = 'https://images.pexels.com/photos/33261955/pexels-photo-33261955.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'team/meera.jpg'                   = 'https://images.pexels.com/photos/1181690/pexels-photo-1181690.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'team/rohan.jpg'                   = 'https://images.pexels.com/photos/1181692/pexels-photo-1181692.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'contact/exterior.jpg'             = 'https://images.pexels.com/photos/35114454/pexels-photo-35114454.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'contact/visualizer.jpg'           = 'https://images.pexels.com/photos/35361412/pexels-photo-35361412.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'page-heroes/projects.jpg'         = 'https://images.pexels.com/photos/35361412/pexels-photo-35361412.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'page-heroes/products.jpg'         = 'https://images.pexels.com/photos/1029599/pexels-photo-1029599.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'page-heroes/gallery.jpg'          = 'https://images.pexels.com/photos/14002095/pexels-photo-14002095.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'page-heroes/about.jpg'            = 'https://images.pexels.com/photos/1115800/pexels-photo-1115800.jpeg?auto=compress&cs=tinysrgb&w=1920'
  'page-heroes/contact.jpg'          = 'https://images.pexels.com/photos/35114454/pexels-photo-35114454.jpeg?auto=compress&cs=tinysrgb&w=1920'
}

foreach ($entry in $map.GetEnumerator()) {
  $dest = Join-Path $root $entry.Key
  $dir = Split-Path $dest -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
  Write-Host "Downloading $($entry.Key)..."
  Invoke-WebRequest -Uri $entry.Value -OutFile $dest -UseBasicParsing
  Start-Sleep -Milliseconds 300
}

Write-Host "Done. $(($map.Count)) files saved to $root"
