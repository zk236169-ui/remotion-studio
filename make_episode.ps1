New-Item -ItemType Directory -Path "public\assets", "public\audio", "D:\remotion-temp" -Force | Out-Null

$scripts = @(
    "They turned Braga into a grand tribute night for Cristiano Ronaldo, yet Portugal walked off humiliated four-one by Denmark, and honestly, the collapse was coming.",
    "Every Portugal player wore a Ronaldo seven shirt while the stands waved GOAT banners, but once the whistle blew, it looked like showmanship instead of real passion.",
    "Even Portugal's own manager Jorge Jesus has warned against building every attack around Ronaldo, and after four straight wins, his system finally snapped under real pressure.",
    "Meanwhile, Rasmus Hojlund buried a volley and a solo strike against his childhood idol's nation, yet he refused to hit Ronaldo's celebration out of pure respect.",
    "Tactically, Denmark completely outcoached them. After Hojbjerg's penalty and Hojlund's brace, Joachim Andersen headed home a fourth while Denmark choked every passing lane into Portugal's box.",
    "Portugal's squad looked completely stunned until Bernardo Silva grabbed a meaningless ninety-fourth-minute consolation. Pre-match ceremonies mean nothing when your tactical shape falls apart.",
    "Hojlund showed more class in silent respect than Portugal showed in ninety minutes. Was this finally a wake-up call for Portugal? Drop your take."
)

$frameCounts = @()
$scriptLog = @()

for ($i = 0; $i -lt $scripts.Count; $i++) {
    $num = $i + 1
    $mp3 = "public\audio\scene$num.mp3"
    $text = $scripts[$i]
    $scriptLog += "Scene ${num}: $text"

    Write-Host "Generating voiceover Scene $num..." -ForegroundColor Cyan
    edge-tts --voice en-GB-RyanNeural --rate="+6%" --text $text --write-media $mp3
    $dur = ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $mp3
    $frameCounts += [math]::Ceiling(([double]$dur + 0.25) * 60)
}

$timings = [ordered]@{
    s1 = $frameCounts[0]; s2 = $frameCounts[1]; s3 = $frameCounts[2]
    s4 = $frameCounts[3]; s5 = $frameCounts[4]; s6 = $frameCounts[5]
    s7 = $frameCounts[6]
    totalFrames = ($frameCounts | Measure-Object -Sum).Sum
}
$timings | ConvertTo-Json | Set-Content "public\timings.json" -Encoding UTF8
$scriptLog -join "`r`n`r`n" | Set-Content "public\english_script.txt" -Encoding UTF8

$sec = [math]::Round($timings.totalFrames / 60, 1)
Write-Host "READY! 7 scenes synced (${sec}s total / $($timings.totalFrames) frames)." -ForegroundColor Green
