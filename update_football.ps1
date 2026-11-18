$pixabayKey  = "58626770-6884478cb00f7529a77a8f4de"
$subjectWiki = "Hansi_Flick"
$clubWiki    = "FC_Barcelona"

$env:U2NET_HOME = "D:\remotion-temp\u2net"
New-Item -ItemType Directory -Path "public\clips", "public\audio", "public\assets", "D:\remotion-temp\u2net" -Force | Out-Null

# 1. Fetch Manager Portrait & Strip Background into Waist-Up Cutout PNG
Write-Host "Fetching $subjectWiki portrait and removing background..." -ForegroundColor Cyan
$headers = @{ "User-Agent" = "RemotionFootballStudio/1.0 (contact@local.dev)" }
$subjMeta = Invoke-RestMethod -Uri "https://en.wikipedia.org/api/rest_v1/page/summary/$subjectWiki" -Headers $headers
$subjUrl = if ($subjMeta.originalimage.source) { $subjMeta.originalimage.source } else { $subjMeta.thumbnail.source }
Invoke-WebRequest -Uri $subjUrl -Headers $headers -OutFile "D:\remotion-temp\subject_raw.jpg"
rembg i -m u2netp "D:\remotion-temp\subject_raw.jpg" "public\assets\subject.png"
Write-Host "Saved transparent cutout: public\assets\subject.png" -ForegroundColor Green

# 2. Fetch Transparent Club Badge PNG
Write-Host "Fetching $clubWiki transparent badge..." -ForegroundColor Cyan
$clubMeta = Invoke-RestMethod -Uri "https://en.wikipedia.org/api/rest_v1/page/summary/$clubWiki" -Headers $headers
$badgeUrl = if ($clubMeta.thumbnail.source) { $clubMeta.thumbnail.source } else { $clubMeta.originalimage.source }
Invoke-WebRequest -Uri $badgeUrl -Headers $headers -OutFile "D:\remotion-temp\badge_raw.png"
rembg i -m u2netp "D:\remotion-temp\badge_raw.png" "public\assets\badge.png"
Write-Host "Saved transparent badge: public\assets\badge.png" -ForegroundColor Green

# 3. Download 6 True Association Football (Soccer) Clips From Pixabay
Write-Host "Downloading 6 true soccer clips from Pixabay..." -ForegroundColor Cyan
$queries = @(
    "soccer+stadium+lights",
    "soccer+pitch+aerial",
    "soccer+ball+grass",
    "soccer+player+dribble",
    "soccer+goal+net",
    "soccer+referee+whistle"
)
$bannedTags = @("american", "nfl", "rugby", "helmet", "flag", "gridiron")
$usedIds = @()
$clipIndex = 1

foreach ($q in $queries) {
    $apiUrl = "https://pixabay.com/api/videos/?key=$pixabayKey&q=$q&category=sports&order=popular&per_page=15"
    $res = Invoke-RestMethod -Uri $apiUrl
    $validHits = $res.hits | Where-Object {
        $tags = $_.tags.ToLower()
        $isBad = $false
        foreach ($b in $bannedTags) { if ($tags -match $b) { $isBad = $true } }
        (-not $isBad) -and ($usedIds -notcontains $_.id)
    }
    $hit = $validHits | Select-Object -First 1
    if (-not $hit) { $hit = $res.hits | Select-Object -First 1 }
    $usedIds += $hit.id

    $videoUrl = if ($hit.videos.medium.url) { $hit.videos.medium.url } else { $hit.videos.small.url }
    $outClip = "public\clips\clip$clipIndex.mp4"
    Invoke-WebRequest -Uri $videoUrl -OutFile $outClip
    Write-Host "Saved $outClip (Tags: $($hit.tags))" -ForegroundColor Green
    $clipIndex++
}

# 4. Pure-Tactics 6-Scene Script + Synced Word-Chunk Captions
$scripts = @(
    "Why do world-class strikers keep falling into Hansi Flick's suicidal offside trap at Barcelona? Look closely at the tactical blueprint.",
    "Traditional coaches drop their back four deep to protect the penalty box. Flick pushes all four defenders right up to the halfway line, squeezing the pitch into thirty meters.",
    "The secret trigger is body language. The exact split-second an opposing midfielder drops his head to pass, all four defenders sprint forward in unison.",
    "By the time the through-ball leaves his boot, the striker is stranded two yards offside. Under FIFA Law Eleven, even a leaning shoulder cancels the goal.",
    "Why can't teams simply chip the ball over the top? Because Barcelona's sweeper-keeper holds a razor-sharp starting position fifteen yards outside his box to intercept every long pass.",
    "One disciplined step turns a certain one-on-one goal into an instant free kick. Is this the bravest tactic in modern football? Drop your verdict below."
)

function Convert-SrtTimeToSec($t) {
    $parts = $t.Trim() -split '[:,]'
    return ([double]$parts[0] * 3600) + ([double]$parts[1] * 60) + [double]$parts[2] + ([double]$parts[3] / 1000.0)
}

$frameCounts = @()
$captionEntries = @()
$scriptLog = @()

for ($i = 0; $i -lt $scripts.Count; $i++) {
    $num = $i + 1
    $mp3Path = "public\audio\scene$num.mp3"
    $srtPath = "D:\remotion-temp\scene$num.srt"
    $text = $scripts[$i]
    $scriptLog += "Scene $num`: $text"

    Write-Host "Generating synced commentary & captions for Scene $num..." -ForegroundColor Cyan
    edge-tts --voice en-GB-RyanNeural --rate="+12%" --text "$text" --write-media $mp3Path --write-subtitles $srtPath

    $durStr = ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $mp3Path
    $frames = [math]::Ceiling(([double]$durStr + 0.30) * 60)
    $frameCounts += $frames

    # Parse SRT into punchy 2-3 word viral caption chunks
    $srtRaw = Get-Content $srtPath -Raw
    $blocks = $srtRaw -split "\r?\n\r?\n" | Where-Object { $_.Trim() -ne "" }
    $sceneCaptions = @()

    foreach ($b in $blocks) {
        $lines = $b -split "\r?\n"
        if ($lines.Count -ge 3 -and $lines[1] -match "-->") {
            $times = $lines[1] -split "-->"
            $sSec = Convert-SrtTimeToSec $times[0]
            $eSec = Convert-SrtTimeToSec $times[1]
            $phrase = ($lines[2..($lines.Count - 1)] -join " ").Trim()
            $words = $phrase -split "\s+"

            # Group into 3-word viral bursts
            $chunkSize = 3
            $totalChunks = [math]::Ceiling($words.Count / $chunkSize)
            $chunkDur = ($eSec - $sSec) / [math]::Max(1, $totalChunks)

            for ($c = 0; $c -lt $totalChunks; $c++) {
                $startIdx = $c * $chunkSize
                $endIdx = [math]::Min($words.Count - 1, $startIdx + $chunkSize - 1)
                $chunkWords = $words[$startIdx..$endIdx]
                $cStartFrame = [math]::Floor(($sSec + ($c * $chunkDur)) * 60)
                $cEndFrame   = [math]::Ceiling(($sSec + (($c + 1) * $chunkDur)) * 60)

                $sceneCaptions += [ordered]@{
                    startFrame = $cStartFrame
                    endFrame   = $cEndFrame
                    words      = $chunkWords
                }
            }
        }
    }
    $captionEntries += ,@($sceneCaptions)
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
$captionEntries | ConvertTo-Json -Depth 5 | Set-Content "public\captions.json" -Encoding UTF8
$scriptLog -join "`r`n`r`n" | Set-Content "public\english_script.txt" -Encoding UTF8

Write-Host "ALL DONE! Cutouts, soccer clips, and viral captions ready ($([math]::Round($timings.totalFrames / 60, 1))s)." -ForegroundColor Green

if (Test-Path 'D:\remotion-temp\fix_captions.js') { node 'D:\remotion-temp\fix_captions.js' }

