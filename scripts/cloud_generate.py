import os, sys, json, time, subprocess, urllib.request

prompt = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "نصائح اختيار الدهانات الأصلية لبيتك"
print(f"Building video for prompt: {prompt}")

os.makedirs("public/assets", exist_ok=True)
os.makedirs("public/clips", exist_ok=True)
os.makedirs("public/audio", exist_ok=True)
os.makedirs("public/sfx", exist_ok=True)
os.makedirs("out", exist_ok=True)
os.makedirs("/tmp/v_src", exist_ok=True)

if not os.path.exists("public/sfx/impact.mp3"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=90:duration=0.35", "public/sfx/impact.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if not os.path.exists("public/sfx/whoosh.mp3"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anoisesrc=d=0.25:c=pink:r=44100:a=0.2", "public/sfx/whoosh.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if not os.path.exists("public/assets/shop_front.jpg"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x0F172A:s=1080x1344:d=1", "-frames:v", "1", "public/assets/shop_front.jpg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Download royalty-free direct HD paint/color/interior videos from Wikimedia / Pexels CDN (no YouTube bot-block!)
direct_sources = [
    ("paint1", "https://upload.wikimedia.org/wikipedia/commons/transcoded/c/c0/Big_Buck_Bunny_4K.webm/Big_Buck_Bunny_4K.webm.720p.vp9.webm"),
]

# Try Pexels/Pixabay direct public MP4s first, with guaranteed high-res animated paint/texture fallback
pexels_urls = [
    "https://videos.pexels.com/video-files/7578552/7578552-hd_1080_1920_30fps.mp4",
    "https://videos.pexels.com/video-files/4763824/4763824-uhd_2560_1440_24fps.mp4",
    "https://videos.pexels.com/video-files/6474343/6474343-hd_1080_1920_25fps.mp4",
    "https://videos.pexels.com/video-files/5532774/5532774-hd_1080_1920_25fps.mp4",
]

downloaded = []
for idx, url in enumerate(pexels_urls, 1):
    dest = f"/tmp/v_src/src_{idx}.mp4"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as resp, open(dest, "wb") as out_f:
            out_f.write(resp.read())
        if os.path.exists(dest) and os.path.getsize(dest) > 200000:
            downloaded.append(dest)
            print(f"Downloaded clip source {idx}")
    except Exception as e:
        print(f"Source {idx} skipped: {e}")

# Build 16 crisp 1080x1344 60fps 3.2s clips (from downloaded videos OR rich fluid paint-swirl shaders if CDN blocks)
c_idx = 1
if downloaded:
    for s_i in range(16):
        src_mp4 = downloaded[s_i % len(downloaded)]
        out_clip = f"public/clips/story_{c_idx:02d}.mp4"
        dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", src_mp4
        ]).decode().strip())
        ss = min((s_i * 2.1) % max(1.0, dur - 3.5), max(0.0, dur - 3.3))
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{ss:.2f}", "-t", "3.2", "-i", src_mp4,
            "-an", "-vf", "scale=1080:1344:force_original_aspect_ratio=increase,crop=1080:1344,eq=contrast=1.06:saturation=1.15,fps=60",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out_clip
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        c_idx += 1
else:
    # Guaranteed fallback: 16 distinct 60fps fluid paint-wave & architectural texture clips
    palettes = [
        "r='128+127*sin(2*PI*(X/400+T*0.7))':g='60+50*cos(2*PI*(Y/400-T*0.5))':b='60+40*sin(T)'",
        "r='40+30*sin(T)':g='140+100*sin(2*PI*(X/350-T*0.6))':b='180+70*cos(2*PI*(Y/350+T*0.5))'",
        "r='200+50*sin(2*PI*(Y/300+T*0.8))':g='150+80*cos(2*PI*(X/300-T*0.6))':b='50+40*sin(T)'",
        "r='30+25*cos(T)':g='170+80*sin(2*PI*(X/320+T*0.7))':b='120+90*cos(2*PI*(Y/320-T*0.5))'",
    ]
    for s_i in range(16):
        out_clip = f"public/clips/story_{c_idx:02d}.mp4"
        geq = palettes[s_i % len(palettes)]
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", f"nullsrc=s=540x672:d=3.2:r=30,geq={geq},scale=1080:1344:flags=bicubic,fps=60",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out_clip
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        c_idx += 1

SHOP_NAME = "\u0645\u062d\u0644 \u062e\u064a\u0628\u0631 \u0627\u0644\u062f\u0647\u0627\u0646\u0627\u062a"
LOCATION  = "\u0627\u0644\u0631\u064a\u0627\u0636 \u2022 \u062d\u064a \u0627\u0644\u062e\u0644\u064a\u062c \u2022 \u0634\u0627\u0631\u0639 \u0627\u0644\u0623\u0645\u064a\u0631 \u0628\u0646\u062f\u0631 \u0628\u0646 \u0639\u0628\u062f\u0627\u0644\u0639\u0632\u064a\u0632 13223"
short_topic = prompt[:28]

timeline = [
    (False, "peel_wall", "story_01", 3.0, "#EF4444", "\u0627\u0646\u062a\u0628\u0647!", short_topic, "+7Hz", "+10%", f"{prompt}! \u0634\u0648\u0641 \u0643\u064a\u0641 \u0627\u0644\u0628\u0648\u064a\u0629 \u062a\u062a\u0642\u0634\u0631 \u0628\u0633\u0631\u0639\u0629!"),
    (False, "no_primer", "story_02", 3.0, "#F59E0B", "\u0627\u0644\u0633\u0628\u0628\u061f", "\u0635\u0628\u063a \u0628\u062f\u0648\u0646 \u0628\u0631\u0627\u064a\u0645\u0631!", "+4Hz", "+10%", "\u0627\u0644\u0633\u0628\u0628 \u0625\u0646\u0647\u0645 \u064a\u0635\u0628\u063a\u0648\u0646 \u0628\u062f\u0648\u0646 \u0628\u0631\u0627\u064a\u0645\u0631 \u0623\u0635\u0644\u064a!"),
    (False, "cheap_redo", "story_03", 3.0, "#EF4444", "\u062e\u0633\u0627\u0631\u0629!", "\u0627\u0644\u0631\u062e\u064a\u0635 \u064a\u0639\u064a\u062f \u0627\u0644\u0634\u063a\u0644 \u0645\u0631\u062a\u064a\u0646!", "+6Hz", "+10%", "\u0648\u0627\u0644\u0628\u0648\u064a\u0629 \u0627\u0644\u0631\u062e\u064a\u0635\u0629 \u062a\u062e\u0644\u064a\u0643 \u062a\u0639\u064a\u062f \u0627\u0644\u0634\u063a\u0644 \u0645\u0631\u062a\u064a\u0646!"),
    (False, "primer_grip", "story_05", 3.0, "#10B981", "\u0627\u0644\u062d\u0644 \u0627\u0644\u0635\u062d", "\u0628\u0631\u0627\u064a\u0645\u0631 \u0642\u0648\u064a \u064a\u0645\u0633\u0643 \u0627\u0644\u062c\u062f\u0627\u0631!", "+5Hz", "+10%", "\u0627\u0644\u062d\u0644 \u0625\u0646\u0643 \u062a\u0628\u062f\u0623 \u0628\u0628\u0631\u0627\u064a\u0645\u0631 \u0642\u0648\u064a \u064a\u0645\u0633\u0643 \u0627\u0644\u062c\u062f\u0627\u0631!"),
    (False, "roller_coat", "story_06", 3.0, "#38BDF8", "\u062a\u063a\u0637\u064a\u0629 100%", "\u062f\u0647\u0627\u0646 \u0623\u0635\u0644\u064a \u0645\u0646 \u0623\u0648\u0644 \u0648\u062c\u0647!", "+6Hz", "+10%", "\u0634\u0648\u0641 \u0627\u0644\u062f\u0647\u0627\u0646 \u0627\u0644\u0623\u0635\u0644\u064a \u0643\u064a\u0641 \u064a\u063a\u0637\u064a \u0627\u0644\u062c\u062f\u0627\u0631 \u0645\u0646 \u0623\u0648\u0644 \u0648\u062c\u0647!"),
    (False, "pc_mix", "story_09", 3.0, "#F59E0B", "\u0628\u0627\u0644\u0643\u0645\u0628\u064a\u0648\u062a\u0631", "\u0646\u062e\u0644\u0637 \u0644\u0643 \u0646\u0641\u0633 \u0627\u0644\u062f\u0631\u062c\u0629!", "+7Hz", "+10%", "\u0648\u0628\u0627\u0644\u0643\u0645\u0628\u064a\u0648\u062a\u0631 \u0646\u062e\u0644\u0637 \u0644\u0643 \u0646\u0641\u0633 \u0627\u0644\u062f\u0631\u062c\u0629 \u0627\u0644\u0644\u064a \u062a\u0628\u064a\u0647\u0627 \u0628\u0627\u0644\u0636\u0628\u0637!"),
    (False, "room_glow", "story_10", 3.0, "#A855F7", "\u0641\u062e\u0627\u0645\u0629", "\u0623\u0644\u0648\u0627\u0646 \u062a\u0634\u0631\u062d \u0627\u0644\u0635\u062f\u0631!", "+6Hz", "+10%", "\u0623\u0644\u0648\u0627\u0646 \u0647\u0627\u062f\u064a\u0629 \u0648\u0631\u0627\u0642\u064a\u0629 \u062a\u0634\u0631\u062d \u0627\u0644\u0635\u062f\u0631 \u0648\u062a\u0648\u0633\u0639 \u0627\u0644\u0645\u0643\u0627\u0646!"),
    (False, "tape_peel", "story_13", 3.0, "#10B981", "\u062a\u0634\u0637\u064a\u0628 \u0641\u0627\u062e\u0631", "\u062d\u0648\u0627\u0641 \u0646\u0638\u064a\u0641\u0629 \u062a\u0631\u0641\u0639 \u0627\u0644\u0631\u0627\u0633!", "+8Hz", "+11%", "\u0634\u0648\u0641 \u0646\u0638\u0627\u0641\u0629 \u0627\u0644\u062d\u0648\u0627\u0641 \u0644\u0645\u0627 \u062a\u0634\u064a\u0644 \u0627\u0644\u0634\u0631\u064a\u0637\u060c \u0634\u063a\u0644 \u064a\u0631\u0641\u0639 \u0627\u0644\u0631\u0627\u0633!"),
    (False, "wash_stain", "story_07", 3.0, "#38BDF8", "\u0644\u0644\u0639\u0648\u0627\u0626\u0644", "\u0642\u0627\u0628\u0644 \u0644\u0644\u063a\u0633\u064a\u0644 \u0648\u0627\u0644\u0645\u0633\u062d!", "+6Hz", "+10%", "\u0648\u0625\u0630\u0627 \u0639\u0646\u062f\u0643 \u0623\u0637\u0641\u0627\u0644\u060c \u062e\u0630 \u062f\u0647\u0627\u0646 \u0642\u0627\u0628\u0644 \u0644\u0644\u063a\u0633\u064a\u0644 \u062a\u0645\u0633\u062d\u0647 \u0648\u064a\u0631\u062c\u0639 \u062c\u062f\u064a\u062f!"),
    (False, "sun_shield", "story_08", 3.0, "#F59E0B", "\u062d\u0645\u0627\u064a\u0629 \u0643\u0627\u0645\u0644\u0629", "\u0639\u0648\u0627\u0632\u0644 \u062a\u0642\u0627\u0648\u0645 \u0627\u0644\u0634\u0645\u0633!", "+5Hz", "+10%", "\u0648\u0644\u0644\u0648\u0627\u062c\u0647\u0629 \u0648\u0627\u0644\u0633\u0637\u062d\u060c \u0639\u0646\u062f\u0646\u0627 \u0639\u0648\u0627\u0632\u0644 \u0648\u062f\u0647\u0627\u0646\u0627\u062a \u062a\u0642\u0627\u0648\u0645 \u0627\u0644\u0634\u0645\u0633 \u0648\u0627\u0644\u0645\u0637\u0631!"),
    (False, "free_calc", "story_11", 3.0, "#10B981", "\u0648\u0641\u0651\u0631 \u0641\u0644\u0648\u0633\u0643", "\u0646\u062d\u0633\u0628 \u0627\u0644\u0643\u0645\u064a\u0629 \u0645\u062c\u0627\u0646\u0627\u064b!", "+6Hz", "+10%", "\u0648\u0639\u0634\u0627\u0646 \u0646\u0648\u0641\u0631 \u0639\u0644\u064a\u0643\u060c \u0646\u062d\u0633\u0628 \u0644\u0643 \u0627\u0644\u0643\u0645\u064a\u0629 \u0627\u0644\u0644\u064a \u064a\u062d\u062a\u0627\u062c\u0647\u0627 \u0628\u064a\u062a\u0643 \u0645\u062c\u0627\u0646\u0627\u064b!"),
    (False, "brands_trio", "story_14", 3.0, "#F59E0B", "\u0627\u0644\u0623\u0635\u0644\u064a \u0639\u0646\u062f\u0646\u0627", "\u062c\u0648\u062a\u0646 \u2022 777 \u2022 \u0646\u0627\u0634\u0648\u0646\u0627\u0644", "+7Hz", "+10%", "\u0643\u0644 \u0647\u0630\u064a \u0627\u0644\u062d\u0644\u0648\u0644 \u0627\u0644\u0623\u0635\u0644\u064a\u0629 \u0645\u0646 \u062c\u0648\u062a\u0646 \u0648\u0633\u0628\u0639\u0645\u064a\u0629 \u0648\u0633\u0628\u0639\u0629 \u0648\u0633\u0628\u0639\u064a\u0646 \u0648\u0646\u0627\u0634\u0648\u0646\u0627\u0644 \u0639\u0646\u062f\u0646\u0627!"),
    (True, "shop_pin", None, 6.0, "#22C55E", "\u0632\u0648\u0631\u0648\u0646\u0627 \u0627\u0644\u064a\u0648\u0645!", SHOP_NAME, "+7Hz", "+10%", "\u062d\u064a\u0627\u0643\u0645 \u0627\u0644\u0644\u0647 \u0641\u064a \u0645\u062d\u0644 \u062e\u064a\u0628\u0631 \u0627\u0644\u062f\u0647\u0627\u0646\u0627\u062a\u060c \u0631\u0627\u0633\u0644\u0646\u0627 \u0648\u0627\u062a\u0633\u0627\u0628 \u0627\u0644\u0622\u0646 \u0639\u0644\u0649 \u0635\u0641\u0631 \u062e\u0645\u0633\u0629 \u062a\u0633\u0639\u0629 \u062a\u0633\u0639\u0629 \u0623\u0631\u0628\u0639\u0629 \u062b\u0645\u0627\u0646\u064a\u0629 \u0623\u0631\u0628\u0639\u0629 \u0635\u0641\u0631 \u0633\u062a\u0629 \u062b\u0645\u0627\u0646\u064a\u0629!")
]

beats_out = []
total_frames = 0

for i, (is_shop, vtype, clip_id, target_sec, accent, tag, head, pitch, rate, spoken) in enumerate(timeline):
    idx = f"{i+1:02d}"
    raw_mp3 = f"/tmp/v_src/beat_{idx}_raw.mp3"
    trim_mp3 = f"/tmp/v_src/beat_{idx}_trim.mp3"
    rel_mp3 = f"audio/cloud_beat_{idx}.mp3"
    final_mp3 = f"public/{rel_mp3}"

    for attempt in range(5):
        time.sleep(0.7 + attempt * 0.5)
        r = subprocess.run([
            "edge-tts", "--voice", "ar-SA-HamedNeural",
            f"--rate={rate}", f"--pitch={pitch}",
            "--text", spoken, "--write-media", raw_mp3
        ], capture_output=True)
        if r.returncode == 0 and os.path.exists(raw_mp3) and os.path.getsize(raw_mp3) > 1000:
            break
    else:
        # Fallback silent-safe tone if edge-tts rate-limits
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono:d={target_sec-0.2}", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        frames = round(target_sec * 60)
        total_frames += frames
        beats_out.append({"isShopEnd": is_shop, "visualType": vtype, "clip": f"clips/{clip_id}.mp4" if clip_id else "", "audio": rel_mp3, "frames": frames, "tag": tag, "headline": head, "accent": accent})
        continue

    subprocess.run([
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.07:stop_threshold=-42dB,acompressor=threshold=-18dB:ratio=2.8:attack=5:release=50",
        trim_mp3
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", trim_mp3
    ]).decode().strip())

    max_audio = target_sec - 0.06
    if dur > max_audio:
        tempo = min(1.25, dur / max_audio)
        subprocess.run(["ffmpeg", "-y", "-i", trim_mp3, "-af", f"atempo={tempo:.3f}", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-i", trim_mp3, "-c", "copy", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    frames = round(target_sec * 60)
    total_frames += frames
    beats_out.append({
        "isShopEnd": is_shop,
        "visualType": vtype,
        "clip": f"clips/{clip_id}.mp4" if clip_id else "",
        "audio": rel_mp3,
        "frames": frames,
        "tag": tag,
        "headline": head,
        "accent": accent
    })

with open("public/current_episode.json", "w", encoding="utf-8") as f:
    json.dump({
        "shopName": SHOP_NAME,
        "locationText": LOCATION,
        "whatsapp": "0599484068",
        "totalFrames": total_frames,
        "beats": beats_out
    }, f, ensure_ascii=False, indent=2)

subprocess.run([
    "npx", "remotion", "render", "src/index.ts", "KhyberAnimatedDeckAR",
    "out/final_telegram_video.mp4", "--codec", "h264", "--crf", "19", "--concurrency=2"
], check=True)