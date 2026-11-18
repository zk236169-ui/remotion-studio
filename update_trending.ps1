$env:U2NET_HOME = "D:\remotion-temp\u2net"
New-Item -ItemType Directory -Path "public\assets", "public\audio", "D:\remotion-temp\u2net" -Force | Out-Null

$headers = @{ "User-Agent" = "RemotionFootballStudio/1.0 (contact@local.dev)" }

function Get-WikiImage($wikiSlug, $outFile) {
    Write-Host "Fetching real photo for $wikiSlug..." -ForegroundColor Cyan
    $meta = Invoke-RestMethod -Uri "https://en.wikipedia.org/api/rest_v1/page/summary/$wikiSlug" -Headers $headers
    $imgUrl = if ($meta.originalimage.source) { $meta.originalimage.source } else { $meta.thumbnail.source }
    Invoke-WebRequest -Uri $imgUrl -Headers $headers -OutFile $outFile
    Write-Host "Saved $outFile" -ForegroundColor Green
}

function Get-CommonsPhoto($searchQuery, $outFile) {
    Write-Host "Searching Wikimedia Commons for '$searchQuery'..." -ForegroundColor Cyan
    $encoded = [uri]::EscapeDataString($searchQuery)
    $api = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=filetype:bitmap+$encoded&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json"
    $res = Invoke-RestMethod -Uri $api -Headers $headers
    $pages = $res.query.pages.PSObject.Properties.Value
    $first = $pages | Where-Object { $_.imageinfo[0].thumburl -match '\.(jpg|jpeg|png)$' } | Select-Object -First 1
    if (-not $first) { $first = $pages | Select-Object -First 1 }
    $url = if ($first.imageinfo[0].thumburl) { $first.imageinfo[0].thumburl } else { $first.imageinfo[0].url }
    Invoke-WebRequest -Uri $url -Headers $headers -OutFile $outFile
    Write-Host "Saved $outFile" -ForegroundColor Green
}

# 1. Fetch Real Player & Manager Portraits + Cutouts
Get-WikiImage "Jorge_Jesus" "public\assets\jesus.jpg"
rembg i -m u2netp "public\assets\jesus.jpg" "public\assets\jesus_cutout.png"

Get-WikiImage "Rasmus_H%C3%B8jlund" "public\assets\hojlund.jpg"
rembg i -m u2netp "public\assets\hojlund.jpg" "public\assets\hojlund_cutout.png"

Get-WikiImage "Cristiano_Ronaldo" "public\assets\ronaldo.jpg"
rembg i -m u2netp "public\assets\ronaldo.jpg" "public\assets\ronaldo_cutout.png"

# 2. Fetch Real Portugal & Denmark National Team Photos
Get-CommonsPhoto "Portugal national football team match" "public\assets\portugal_team.jpg"
Get-CommonsPhoto "Denmark national football team match" "public\assets\denmark_team.jpg"

# 3. 60-Second Conversational Human-Opinion Script (6 Synced Scenes)
$scripts = @(
    "Everyone called it a tribute night for Cristiano Ronaldo, yet Portugal walked off humiliated four-one by Denmark, and honestly, the warning signs were obvious from the start.",
    "Look at the tension around Portugal right now. Even top Portuguese managers like Jorge Jesus have openly questioned building everything around Ronaldo, and this night felt more like pre-match showmanship than real respect on the pitch.",
    "Meanwhile, Denmark's Rasmus Hojlund stepped up and buried two clinical goals against his childhood idol's team. Hojlund usually hits Ronaldo's iconic celebration, yet after scoring twice here, he refused to do it out of pure respect.",
    "Tactically, Denmark's manager completely outcoached Portugal. Denmark packed the central midfield, cut off every passing lane into Ronaldo, and launched ruthless counter-attacks into the empty space behind Portugal's full-backs.",
    "Portugal's players looked stunned and out of ideas as the scoreline hit four-one. Pre-match ceremonies and big names mean nothing when the tactical structure falls apart.",
    "Hojlund showed more class in silent respect than Portugal showed in ninety minutes. Was this a wake-up call for Portugal? Let me know what you think."
)

$frameCounts = @()
$scriptLog = @()

for ($i = 0; $i -lt $scripts.Count; $i++) {
    $num = $i + 1
    $mp3Path = "public\audio\scene$num.mp3"
    $text = $scripts[$i]
    $scriptLog += "Scene ${num}: $text"

    Write-Host "Generating natural English commentary for Scene $num..." -ForegroundColor Cyan
    edge-tts --voice en-GB-RyanNeural --rate="+4%" --text "$text" --write-media $mp3Path

    $durStr = ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $mp3Path
    $frames = [math]::Ceiling(([double]$durStr + 0.30) * 60)
    $frameCounts += $frames
}

$timings = [ordered]@{
    s1 = $frameCounts[0]
    s2 = $frameCounts[1]
    s3 = $frameCounts[2]
    s4 = $frameCounts[3]
    s5 = $frameCounts[4]
    s6 = $frameCounts[5]
    totalFrames = ($frameCounts | Measure-Object -Sum).Sum
}
$timings | ConvertTo-Json | Set-Content "public\timings.json" -Encoding UTF8
$scriptLog -join "`r`n`r`n" | Set-Content "public\english_script.txt" -Encoding UTF8

$totalSec = [math]::Round($timings.totalFrames / 60, 1)
Write-Host "ALL DONE! Real photos, cutouts, and synced ${totalSec}s commentary ready." -ForegroundColor Green
