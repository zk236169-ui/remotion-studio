import os, sys, json, time, subprocess, urllib.request, urllib.parse

prompt = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "نصائح اختيار الدهانات الأصلية لبيتك"
print(f"Building scene-by-scene video for: {prompt}")

os.makedirs("public/assets", exist_ok=True)
os.makedirs("public/clips", exist_ok=True)
os.makedirs("public/audio", exist_ok=True)
os.makedirs("public/sfx", exist_ok=True)
os.makedirs("out", exist_ok=True)
os.makedirs("/tmp/v_src", exist_ok=True)

if not os.path.exists("public/assets/shop_front.jpg"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x0F172A:s=1080x1344:d=1", "-frames:v", "1", "public/assets/shop_front.jpg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 12 distinct real-world queries matched 1-to-1 with each voiceover scene
scene_queries = [
    ("story_01", "peeling paint wall",          "zoompan=z='min(zoom+0.0018,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_02", "water damage wall",           "zoompan=z='1.22-0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_03", "cracked wall paint",          "zoompan=z='min(zoom+0.0016,1.24)':x='on*1.2':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_05", "paint roller wall",           "zoompan=z='min(zoom+0.0018,1.25)':x='iw/2-(iw/zoom/2)':y='on*1.5':d=192:s=1080x1344:fps=60"),
    ("story_06", "house painter wall",          "zoompan=z='1.24-0.0013*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_09", "paint color mixing",          "zoompan=z='min(zoom+0.0020,1.28)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_10", "luxury living room interior", "zoompan=z='min(zoom+0.0015,1.22)':x='on*1.4':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_13", "masking tape painting",       "zoompan=z='1.22-0.0012*on':x='iw/2-(iw/zoom/2)':y='on*1.3':d=192:s=1080x1344:fps=60"),
    ("story_07", "modern bedroom interior",     "zoompan=z='min(zoom+0.0016,1.24)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_08", "modern villa facade",         "zoompan=z='min(zoom+0.0017,1.25)':x='on*1.1':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_11", "paint color swatches",        "zoompan=z='1.25-0.0013*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
    ("story_14", "paint cans brushes",          "zoompan=z='min(zoom+0.0018,1.26)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1080x1344:fps=60"),
]

used_urls = set()

for idx_s, (clip_name, query, zp) in enumerate(scene_queries):
    img_path = f"/tmp/v_src/{clip_name}.jpg"
    out_clip = f"public/clips/{clip_name}.mp4"
    fetched = False
    try:
        api_url = (
            "https://commons.wikimedia.org/w/api.php?action=query&generator=search"
            f"&gsrsearch=filetype:bitmap+{urllib.parse.quote(query)}"
            "&gsrnamespace=6&gsrlimit=6&prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json"
        )
        req = urllib.request.Request(api_url, headers={"User-Agent": "KhyberVideoBot/1.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
        pages = data.get("query", {}).get("pages", {})
        for p in pages.values():
            thumb = p.get("imageinfo", [{}])[0].get("thumburl")
            if thumb and thumb not in used_urls:
                req_img = urllib.request.Request(thumb, headers={"User-Agent": "KhyberVideoBot/1.0"})
                with urllib.request.urlopen(req_img, timeout=15) as r_img, open(img_path, "wb") as f_img:
                    f_img.write(r_img.read())
                if os.path.exists(img_path) and os.path.getsize(img_path) > 15000:
                    used_urls.add(thumb)
                    fetched = True
                    print(f"Fetched unique scene image for {clip_name}: {query}")
                    break
    except Exception as e:
        print(f"Fallback for {clip_name}: {e}")

    if fetched:
        subprocess.run([
            "ffmpeg", "-y", "-i", img_path,
            "-vf", f"scale=1600:-2,{zp},eq=contrast=1.08:saturation=1.18",
            "-t", "3.2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out_clip
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        hue = idx_s * 30
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"color=c=0x1E293B:s=1080x1344:d=3.2:r=60,hue=h={hue}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out_clip
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

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