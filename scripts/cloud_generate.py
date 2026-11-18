import os, sys, json, time, subprocess, urllib.request, urllib.parse

prompt = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "ÙƒÙŠÙ ØªØ®ØªØ§Ø± Ø¯Ù‡Ø§Ù† ÙŠØ¹ÙŠØ´ Ø³Ù†ÙŠÙ† Ø¨Ø¯ÙˆÙ† ØªÙ‚Ø´ÙŠØ±"
groq_key = os.environ.get("GROQ_API_KEY", "").strip()
pixabay_key = os.environ.get("PIXABAY_API_KEY", "").strip()

print(f"Generating viral Saudi Reel for prompt: {prompt}")

os.makedirs("public/assets", exist_ok=True)
os.makedirs("public/clips", exist_ok=True)
os.makedirs("public/audio", exist_ok=True)
os.makedirs("public/sfx", exist_ok=True)
os.makedirs("out", exist_ok=True)
os.makedirs("/tmp/v_src", exist_ok=True)

if not os.path.exists("public/assets/shop_front.jpg"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x0F172A:s=1080x1344:d=1", "-frames:v", "1", "public/assets/shop_front.jpg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Upbeat rhythmic background groove
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.18*sin(2*PI*55*t)*exp(-8*mod(t,0.5)) + 0.05*sin(2*PI*220*t) + 0.04*sin(2*PI*330*t)':s=44100:d=50",
    "-af", "lowpass=f=900,volume=0.32",
    "public/audio/bg_groove.mp3"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

SHOP_NAME = "\u0645\u062d\u0644 \u062e\u064a\u0628\u0631 \u0627\u0644\u062f\u0647\u0627\u0646\u0627\u062a"
LOCATION  = "\u0627\u0644\u0631\u064a\u0627\u0636 \u2022 \u062d\u064a \u0627\u0644\u062e\u0644\u064a\u062c \u2022 \u0634\u0627\u0631\u0639 \u0627\u0644\u0623\u0645\u064a\u0631 \u0628\u0646\u062f\u0631 \u0628\u0646 \u0639\u0628\u062f\u0627\u0644\u0639\u0632\u064a\u0632 13223"

# 1. Generate dynamic, fast-paced 8-scene Saudi TikTok/Reel script via Groq Llama-3.3-70B
scenes_data = None
if groq_key:
    try:
        sys_msg = (
            "You are an elite Saudi TikTok/Reels viral ad director for a paint store in Riyadh called Ù…Ø­Ù„ Ø®ÙŠØ¨Ø± Ø§Ù„Ø¯Ù‡Ø§Ù†Ø§Øª "
            "(selling Jotun, 777, National paints - NEVER mention Dulux). "
            "Write a fast, punchy, exciting 8-scene viral Reel script in natural spoken Saudi dialect (NOT boring professor talk). "
            "Each scene is 3 seconds (~8 to 11 Arabic words max). "
            "Return ONLY valid JSON with key 'scenes': a list of 8 objects, each having: "
            "'tag' (2-word Arabic badge), 'headline' (3-5 word punchy Arabic hook), "
            "'spoken' (energetic Saudi dialect voiceover line), "
            "'video_query' (2-word English visual search query for moving video like 'painting wall', 'paint roller', 'color mixing', 'living room', 'peeling paint', 'paint brush', 'modern house', 'paint cans'), "
            "'accent' (hex color like '#EF4444', '#F59E0B', '#10B981', '#38BDF8', '#A855F7')."
        )
        body = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "response_format": {"type": "json_object"},
            "temperature": 0.85,
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": f"Create an 8-scene viral Saudi Reel script about: {prompt}"}
            ]
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json",
                "User-Agent": "KhyberStudio/2.0"
            }
        )
        res = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
        parsed = json.loads(res["choices"][0]["message"]["content"])
        if isinstance(parsed.get("scenes"), list) and len(parsed["scenes"]) >= 6:
            scenes_data = parsed["scenes"][:8]
            print("Generated custom AI Saudi script via Groq!")
    except Exception as e:
        print(f"Groq fallback triggered: {e}")

if not scenes_data:
    scenes_data = [
        {"tag": "ÙˆÙ‚Ù Ø´ÙˆÙŠ!", "headline": prompt[:26], "spoken": f"{prompt}! Ù„Ø§ ØªØµØ¨Øº Ø¨ÙŠØªÙƒ Ù‚Ø¨Ù„ Ù…Ø§ ØªØ´ÙˆÙ Ù‡Ø§Ù„Ø³Ø±!", "video_query": "painting wall", "accent": "#EF4444"},
        {"tag": "Ø£ÙƒØ¨Ø± ØºÙ„Ø·Ø©", "headline": "Ø§Ù„Ø¨ÙˆÙŠØ© Ø§Ù„Ø±Ø®ÙŠØµØ© ØªØªÙ‚Ø´Ø±!", "spoken": "Ø£ØºÙ„Ø¨ Ø§Ù„Ù†Ø§Ø³ ÙŠØ®Ø³Ø±ÙˆÙ† ÙÙ„ÙˆØ³Ù‡Ù… Ø¹Ù„Ù‰ Ø¨ÙˆÙŠØ© ØªØªÙ‚Ø´Ø± Ø¨Ø¹Ø¯ Ø´Ù‡ÙˆØ±!", "video_query": "peeling paint", "accent": "#F59E0B"},
        {"tag": "Ø§Ù„Ø³Ø± Ù‡Ù†Ø§", "headline": "Ø¨Ø±Ø§ÙŠÙ…Ø± Ø£ØµÙ„ÙŠ ÙŠÙ…Ø³Ùƒ Ø§Ù„Ø¬Ø¯Ø§Ø±", "spoken": "Ø§Ù„Ø³Ø± Ø¥Ù†Ùƒ ØªØ£Ø³Ø³ Ø¨Ø¨Ø±Ø§ÙŠÙ…Ø± Ù‚ÙˆÙŠ ÙŠÙ‚ÙÙ„ Ø§Ù„Ù…Ø³Ø§Ù… ØµØ­!", "video_query": "paint brush", "accent": "#10B981"},
        {"tag": "Ø¯Ù‚Ø© 100%", "headline": "Ø®Ù„Ø· Ø£Ù„ÙˆØ§Ù† Ø¨Ø§Ù„ÙƒÙ…Ø¨ÙŠÙˆØªØ±", "spoken": "ÙˆØ¨Ø§Ù„ÙƒÙ…Ø¨ÙŠÙˆØªØ± Ù†Ø®Ù„Ø· Ù„Ùƒ Ù†ÙØ³ Ø§Ù„Ø¯Ø±Ø¬Ø© Ø§Ù„Ù„ÙŠ ÙÙŠ Ø¨Ø§Ù„Ùƒ Ø¨Ø§Ù„Ø¶Ø¨Ø·!", "video_query": "color mixing", "accent": "#38BDF8"},
        {"tag": "ÙØ®Ø§Ù…Ø©", "headline": "Ø£Ù„ÙˆØ§Ù† ØªÙˆØ³Ø¹ Ø§Ù„Ù…ÙƒØ§Ù†", "spoken": "Ø´ÙˆÙ ÙƒÙŠÙ Ø§Ù„Ø¯Ø±Ø¬Ø§Øª Ø§Ù„Ù‡Ø§Ø¯ÙŠØ© ØªÙ‚Ù„Ø¨ Ø§Ù„ØµØ§Ù„Ø© Ù‚ØµØ±!", "video_query": "living room", "accent": "#A855F7"},
        {"tag": "Ø¶Ø¯ Ø§Ù„Ø´Ù…Ø³", "headline": "Ø­Ù…Ø§ÙŠØ© Ù…Ù† Ø­Ø± Ø§Ù„Ø±ÙŠØ§Ø¶", "spoken": "ÙˆÙ„Ù„ÙˆØ§Ø¬Ù‡Ø§Øª Ø¹Ù†Ø¯Ù†Ø§ Ø¹ÙˆØ§Ø²Ù„ ØªØªØ­Ù…Ù„ Ø´Ù…Ø³ Ø§Ù„Ø±ÙŠØ§Ø¶ Ø®Ù…Ø³ÙŠÙ† Ø¯Ø±Ø¬Ø©!", "video_query": "modern house", "accent": "#F59E0B"},
        {"tag": "ØªÙˆÙÙŠØ±", "headline": "Ù†Ø­Ø³Ø¨ Ø§Ù„ÙƒÙ…ÙŠØ© Ù…Ø¬Ø§Ù†Ø§Ù‹", "spoken": "Ø¹Ø·Ù†ÙŠ Ù…Ù‚Ø§Ø³Ø§Øª ØºØ±ÙØªÙƒ ÙˆÙ†Ø­Ø³Ø¨ Ù„Ùƒ Ø§Ù„ÙƒÙ…ÙŠØ© Ø¨Ø¯ÙˆÙ† Ø²ÙŠØ§Ø¯Ø© Ø±ÙŠØ§Ù„!", "video_query": "home renovation", "accent": "#10B981"},
        {"tag": "Ø§Ù„Ø£ØµÙ„ÙŠ", "headline": "Ø¬ÙˆØªÙ† â€¢ 777 â€¢ Ù†Ø§Ø´ÙˆÙ†Ø§Ù„", "spoken": "ÙƒÙ„ Ø¯Ù‡Ø§Ù†Ø§Øª Ø¬ÙˆØªÙ† ÙˆØ³Ø¨Ø¹Ù…ÙŠØ© ÙˆØ³Ø¨Ø¹Ø© ÙˆØ³Ø¨Ø¹ÙŠÙ† ÙˆÙ†Ø§Ø´ÙˆÙ†Ø§Ù„ Ø§Ù„Ø£ØµÙ„ÙŠØ© Ø¹Ù†Ø¯Ù†Ø§!", "video_query": "paint roller", "accent": "#38BDF8"},
    ]

# 2. Fetch REAL MOVING HD Videos from Pixabay API for each scene
used_video_ids = set()
for idx, sc in enumerate(scenes_data, 1):
    clip_out = f"public/clips/scene_{idx:02d}.mp4"
    raw_vid = f"/tmp/v_src/pixabay_{idx:02d}.mp4"
    q = sc.get("video_query") or "painting wall"
    downloaded = False

    if pixabay_key:
        try:
            p_url = f"https://pixabay.com/api/videos/?key={urllib.parse.quote(pixabay_key)}&q={urllib.parse.quote(q)}&per_page=10"
            req = urllib.request.Request(p_url, headers={"User-Agent": "Mozilla/5.0"})
            pdata = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
            for hit in pdata.get("hits", []):
                vid_id = hit.get("id")
                if vid_id in used_video_ids:
                    continue
                vids = hit.get("videos", {})
                dl_url = (vids.get("medium") or vids.get("small") or {}).get("url")
                if dl_url:
                    req_v = urllib.request.Request(dl_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req_v, timeout=25) as r_v, open(raw_vid, "wb") as f_v:
                        f_v.write(r_v.read())
                    if os.path.exists(raw_vid) and os.path.getsize(raw_vid) > 120000:
                        used_video_ids.add(vid_id)
                        downloaded = True
                        print(f"Downloaded moving Pixabay clip {idx}: {q}")
                        break
        except Exception as e:
            print(f"Pixabay skip {idx}: {e}")

    if downloaded:
        subprocess.run([
            "ffmpeg", "-y", "-ss", "0.5", "-t", "3.2", "-i", raw_vid,
            "-an", "-vf", "scale=1080:1344:force_original_aspect_ratio=increase,crop=1080:1344,eq=contrast=1.08:saturation=1.18,fps=60",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", clip_out
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        c_hex = sc.get("accent", "#38BDF8").replace("#", "0x")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"color=c={c_hex}:s=1080x1344:d=3.2:r=60",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", clip_out
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# 3. Synthesize energetic Saudi voiceover per scene & mix subtle groove
beats_out = []
total_frames = 0

all_steps = scenes_data + [{
    "isShopEnd": True,
    "tag": "Ø²ÙˆØ±ÙˆÙ†Ø§ Ø§Ù„ÙŠÙˆÙ…!",
    "headline": SHOP_NAME,
    "spoken": "Ø­ÙŠØ§ÙƒÙ… Ø§Ù„Ù„Ù‡ ÙÙŠ Ù…Ø­Ù„ Ø®ÙŠØ¨Ø± Ø§Ù„Ø¯Ù‡Ø§Ù†Ø§Øª Ø¨Ø§Ù„Ø±ÙŠØ§Ø¶ØŒ Ø±Ø§Ø³Ù„Ù†Ø§ ÙˆØ§ØªØ³Ø§Ø¨ Ø§Ù„Ø­ÙŠÙ† Ø¹Ù„Ù‰ ØµÙØ± Ø®Ù…Ø³Ø© ØªØ³Ø¹Ø© ØªØ³Ø¹Ø© Ø£Ø±Ø¨Ø¹Ø© Ø«Ù…Ø§Ù†ÙŠØ© Ø£Ø±Ø¨Ø¹Ø© ØµÙØ± Ø³ØªØ© Ø«Ù…Ø§Ù†ÙŠØ©!",
    "accent": "#22C55E"
}]

for i, sc in enumerate(all_steps):
    is_shop = bool(sc.get("isShopEnd", False))
    target_sec = 5.5 if is_shop else 3.0
    idx = f"{i+1:02d}"
    raw_mp3 = f"/tmp/v_src/v_{idx}_raw.mp3"
    trim_mp3 = f"/tmp/v_src/v_{idx}_trim.mp3"
    rel_mp3 = f"audio/reel_beat_{idx}.mp3"
    final_mp3 = f"public/{rel_mp3}"

    for attempt in range(5):
        time.sleep(0.6 + attempt * 0.4)
        r = subprocess.run([
            "edge-tts", "--voice", "ar-SA-HamedNeural",
            "--rate=+14%", "--pitch=+8Hz",
            "--text", sc["spoken"], "--write-media", raw_mp3
        ], capture_output=True)
        if r.returncode == 0 and os.path.exists(raw_mp3) and os.path.getsize(raw_mp3) > 1000:
            break
    else:
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono:d={target_sec-0.2}", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        frames = round(target_sec * 60)
        total_frames += frames
        beats_out.append({"isShopEnd": is_shop, "visualType": "reel", "clip": "" if is_shop else f"clips/scene_{idx}.mp4", "audio": rel_mp3, "frames": frames, "tag": sc["tag"], "headline": sc["headline"], "accent": sc["accent"]})
        continue

    subprocess.run([
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.06:stop_threshold=-42dB,acompressor=threshold=-16dB:ratio=3.2:attack=4:release=45",
        trim_mp3
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", trim_mp3
    ]).decode().strip())

    max_audio = target_sec - 0.05
    if dur > max_audio:
        tempo = min(1.28, dur / max_audio)
        subprocess.run(["ffmpeg", "-y", "-i", trim_mp3, "-af", f"atempo={tempo:.3f}", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-i", trim_mp3, "-c", "copy", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    frames = round(target_sec * 60)
    total_frames += frames
    beats_out.append({
        "isShopEnd": is_shop,
        "visualType": "reel",
        "clip": "" if is_shop else f"clips/scene_{idx}.mp4",
        "audio": rel_mp3,
        "frames": frames,
        "tag": sc["tag"],
        "headline": sc["headline"],
        "accent": sc["accent"]
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
    "out/raw_video.mp4", "--codec", "h264", "--crf", "19", "--concurrency=2"
], check=True)

subprocess.run([
    "ffmpeg", "-y", "-i", "out/raw_video.mp4", "-stream_loop", "-1", "-i", "public/audio/bg_groove.mp3",
    "-filter_complex", "[0:a]volume=1.15[v];[1:a]volume=0.22[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
    "out/final_telegram_video.mp4"
], check=True)
