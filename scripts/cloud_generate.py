import os, sys, json, time, subprocess, urllib.request, urllib.parse

prompt = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "كيف تختار دهان يعيش سنين بدون تقشير"
groq_key = os.environ.get("GROQ_API_KEY", "").strip()
pixabay_key = os.environ.get("PIXABAY_API_KEY", "").strip()

print(f"Generating 65-75s animated Saudi story Reel for: {prompt}")

os.makedirs("public/assets", exist_ok=True)
os.makedirs("public/clips", exist_ok=True)
os.makedirs("public/audio", exist_ok=True)
os.makedirs("out", exist_ok=True)
os.makedirs("/tmp/v_src", exist_ok=True)

if not os.path.exists("public/assets/shop_front.jpg"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x0F172A:s=1080x1344:d=1", "-frames:v", "1", "public/assets/shop_front.jpg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Warm, emotional storytelling background music loop
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.14*sin(2*PI*55*t)*exp(-6*mod(t,0.75)) + 0.04*sin(2*PI*220*t) + 0.03*sin(2*PI*277.18*t) + 0.03*sin(2*PI*329.63*t)':s=44100:d=95",
    "-af", "lowpass=f=850,volume=0.28",
    "public/audio/bg_groove.mp3"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

SHOP_NAME = "\u0645\u062d\u0644 \u062e\u064a\u0628\u0631 \u0627\u0644\u062f\u0647\u0627\u0646\u0627\u062a"
LOCATION  = "\u0627\u0644\u0631\u064a\u0627\u0636 \u2022 \u062d\u064a \u0627\u0644\u062e\u0644\u064a\u062c \u2022 \u0634\u0627\u0631\u0639 \u0627\u0644\u0623\u0645\u064a\u0631 \u0628\u0646\u062f\u0631 \u0628\u0646 \u0639\u0628\u062f\u0627\u0644\u0639\u0632\u064a\u0632 13223"

# 1. Generate a 13-scene (65-75 second) emotional Saudi story script via Groq
scenes_data = None
if groq_key:
    try:
        sys_msg = (
            "You are a master Saudi storyteller and viral Reels director for محل خيبر الدهانات in Riyadh "
            "(selling Jotun, 777, National paints - NEVER mention Dulux). "
            "Write an emotional, relatable, human 13-scene story script (around 65 seconds total when spoken naturally) in warm spoken Saudi dialect. "
            "Make the viewer feel the frustration of ruined walls, the relief of smart solutions, and the pride of a gorgeous home. "
            "Each scene spoken line should be 12 to 16 Arabic words (~4.5 to 5.2 seconds at calm, natural human speed). "
            "Return ONLY valid JSON with key 'scenes': a list of 13 objects, each having: "
            "'animType' (MUST be one of: 'peeling_wall', 'sun_heat', 'primer_bond', 'roller_stroke', 'color_mixer', 'cost_comparison', 'washable_shield', 'brands_podium'), "
            "'tag' (2-word Arabic emotion/stage badge), "
            "'headline' (3-5 word punchy Arabic headline), "
            "'subline' (4-6 word supporting Arabic subtitle), "
            "'spoken' (warm, expressive Saudi dialect voiceover sentence), "
            "'video_query' (2-word English query for Pixabay moving video like 'painting wall', 'home renovation', 'living room', 'paint roller', 'color mixing', 'modern house', 'family home', 'paint brush'), "
            "'accent' (hex color like '#EF4444', '#F59E0B', '#10B981', '#38BDF8', '#A855F7')."
        )
        body = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "response_format": {"type": "json_object"},
            "temperature": 0.85,
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": f"Write a 13-scene emotional Saudi story Reel (65+ seconds) about: {prompt}"}
            ]
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json",
                "User-Agent": "KhyberStudio/3.0"
            }
        )
        res = json.loads(urllib.request.urlopen(req, timeout=25).read().decode())
        parsed = json.loads(res["choices"][0]["message"]["content"])
        if isinstance(parsed.get("scenes"), list) and len(parsed["scenes"]) >= 10:
            scenes_data = parsed["scenes"][:13]
            print(f"Generated {len(scenes_data)}-scene emotional Saudi script via Groq!")
    except Exception as e:
        print(f"Groq fallback triggered: {e}")

if not scenes_data:
    scenes_data = [
        {"animType": "peeling_wall", "tag": "قصة حقيقية", "headline": "تخيل تصرف آلاف الريالات...", "subline": "وبعد 6 شهور يتقشر الجدار قدام عينك!", "spoken": f"{prompt}! تخيل تدفع دم قلبك على تشطيب بيتك، وبعد ست شهور بس تشوف البوية تتقشر قدام عينك!", "video_query": "peeling paint", "accent": "#EF4444"},
        {"animType": "cost_comparison", "tag": "أكبر ندم", "headline": "البوية الرخيصة تكلفك الضعف", "subline": "تضطر تكشط وتصبغ من جديد", "spoken": "هذا أكبر ندم يطيح فيه أغلب أصحاب البيوت، يأخذون بوية رخيصة ويضطرون يعيدون الشغل مرتين!", "video_query": "home renovation", "accent": "#F59E0B"},
        {"animType": "sun_heat", "tag": "جو الرياض", "headline": "شمسنا ما ترحم أي جدار", "subline": "حرارة 50 درجة تكسر الدهان العادي", "spoken": "خصوصاً في جو الرياض، الشمس والحرارة العالية تفكك أي دهان تجاري ما فيه حماية حقيقية!", "video_query": "modern house", "accent": "#F59E0B"},
        {"animType": "primer_bond", "tag": "السر الأول", "headline": "التأسيس ببرايمر أصلي", "subline": "يمسك في الخرسانة ويمنع الرطوبة", "spoken": "السر الأول اللي يخلي جدارك يعيش عشر سنين إنك تبدأ ببرايمر أصلي يقفل المسام صح!", "video_query": "painting wall", "accent": "#10B981"},
        {"animType": "roller_stroke", "tag": "الفرق واضح", "headline": "تغطية ثقيلة من أول وجه", "subline": "نعومة ولمعة تفتح النفس", "spoken": "شوف الفرق لما تشتغل بدهان أصلي، الرول يمشي بسلاسة ويغطي الجدار من أول وجه!", "video_query": "paint roller", "accent": "#38BDF8"},
        {"animType": "color_mixer", "tag": "نفس الدرجة", "headline": "خلط ألوان بالكمبيوتر", "subline": "تطابق 100% مع تصميم بيتك", "spoken": "وإذا شفت لون عجبك في صورة أو تصميم، بالكمبيوتر نخلط لك نفس الدرجة بالمللي!", "video_query": "color mixing", "accent": "#A855F7"},
        {"animType": "washable_shield", "tag": "راحة بال", "headline": "قابل للغسيل بدون أثر", "subline": "امسح شخبطة الأطفال ويرجع جديد", "spoken": "والأجمل للعوائل، عندنا دهانات قابلة للغسيل، لو شخبطوا الأطفال تمسحه بمنديل ويرجع جديد!", "video_query": "family home", "accent": "#38BDF8"},
        {"animType": "brands_podium", "tag": "ثقة وجودة", "headline": "جوتن • 777 • ناشونال", "subline": "وكلاء معتمدون بأحدث التواريخ", "spoken": "كل منتجات جوتن وسبعمية وسبعة وسبعين وناشونال الأصلية متوفرة عندنا بتواريخ إنتاج جديدة!", "video_query": "paint brush", "accent": "#10B981"},
        {"animType": "cost_comparison", "tag": "هدية لك", "headline": "نحسب كمية بيتك مجاناً", "subline": "لا تشتري سطل واحد زيادة", "spoken": "وعشان ما تخسر ريال واحد زيادة، عطني مقاسات غرفك ونحسب لك الكمية بالضبط مجاناً!", "video_query": "living room", "accent": "#F59E0B"},
        {"animType": "roller_stroke", "tag": "فخامة بيتك", "headline": "خلي بيتك يسر الناظرين", "subline": "ألوان هادية تشرح الصدر", "spoken": "بيتك هو مكان راحتك، اختار له ألوان راقية تشرح صدرك وصدر ضيوفك كل يوم!", "video_query": "interior design", "accent": "#A855F7"},
    ]

# 2. Fetch distinct moving HD videos from Pixabay API
used_video_ids = set()
for idx, sc in enumerate(scenes_data, 1):
    clip_out = f"public/clips/scene_{idx:02d}.mp4"
    raw_vid = f"/tmp/v_src/pixabay_{idx:02d}.mp4"
    q = sc.get("video_query") or "painting wall"
    downloaded = False

    if pixabay_key:
        try:
            p_url = f"https://pixabay.com/api/videos/?key={urllib.parse.quote(pixabay_key)}&q={urllib.parse.quote(q)}&per_page=15"
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
                        print(f"Downloaded Pixabay clip {idx}: {q}")
                        break
        except Exception as e:
            print(f"Pixabay skip {idx}: {e}")

    if downloaded:
        subprocess.run([
            "ffmpeg", "-y", "-stream_loop", "-1", "-t", "6.5", "-i", raw_vid,
            "-an", "-vf", "scale=1080:1344:force_original_aspect_ratio=increase,crop=1080:1344,eq=contrast=1.08:saturation=1.18,fps=60",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", clip_out
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        c_hex = sc.get("accent", "#38BDF8").replace("#", "0x")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"color=c={c_hex}:s=1080x1344:d=6.5:r=60",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", clip_out
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# 3. Synthesize calm, expressive Saudi voiceover and size each beat to natural spoken duration (65-75s total)
beats_out = []
total_frames = 0

all_steps = scenes_data + [{
    "isShopEnd": True,
    "animType": "brands_podium",
    "tag": "زورونا اليوم!",
    "headline": SHOP_NAME,
    "subline": LOCATION,
    "spoken": "حياكم الله في محل خيبر الدهانات بحي الخليج في الرياض، راسلنا واتساب الحين على صفر خمسة تسعة تسعة أربعة ثمانية أربعة صفر ستة ثمانية، وفالكم طيب!",
    "accent": "#22C55E"
}]

for i, sc in enumerate(all_steps):
    is_shop = bool(sc.get("isShopEnd", False))
    idx = f"{i+1:02d}"
    raw_mp3 = f"/tmp/v_src/v_{idx}_raw.mp3"
    trim_mp3 = f"/tmp/v_src/v_{idx}_trim.mp3"
    rel_mp3 = f"audio/reel_beat_{idx}.mp3"
    final_mp3 = f"public/{rel_mp3}"

    for attempt in range(5):
        time.sleep(0.6 + attempt * 0.4)
        r = subprocess.run([
            "edge-tts", "--voice", "ar-SA-HamedNeural",
            "--rate=-2%", "--pitch=+4Hz",
            "--text", sc["spoken"], "--write-media", raw_mp3
        ], capture_output=True)
        if r.returncode == 0 and os.path.exists(raw_mp3) and os.path.getsize(raw_mp3) > 1000:
            break
    else:
        fallback_sec = 6.0 if is_shop else 4.8
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono:d={fallback_sec-0.2}", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        frames = round(fallback_sec * 60)
        total_frames += frames
        beats_out.append({
            "isShopEnd": is_shop,
            "animType": sc.get("animType", "brands_podium"),
            "clip": "" if is_shop else f"clips/scene_{idx}.mp4",
            "audio": rel_mp3,
            "frames": frames,
            "tag": sc.get("tag", ""),
            "headline": sc.get("headline", ""),
            "subline": sc.get("subline", ""),
            "accent": sc.get("accent", "#38BDF8")
        })
        continue

    subprocess.run([
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.08:stop_threshold=-42dB,acompressor=threshold=-16dB:ratio=2.8:attack=5:release=50",
        trim_mp3
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", trim_mp3
    ]).decode().strip())

    # Size each scene naturally to the spoken sentence (+0.35s breathing room) without speeding up voice
    scene_sec = max(4.2, min(6.2, dur + 0.35))
    if is_shop:
        scene_sec = max(6.0, dur + 0.5)

    subprocess.run(["ffmpeg", "-y", "-i", trim_mp3, "-c", "copy", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    frames = round(scene_sec * 60)
    total_frames += frames
    beats_out.append({
        "isShopEnd": is_shop,
        "animType": sc.get("animType", "brands_podium"),
        "clip": "" if is_shop else f"clips/scene_{idx}.mp4",
        "audio": rel_mp3,
        "frames": frames,
        "tag": sc.get("tag", ""),
        "headline": sc.get("headline", ""),
        "subline": sc.get("subline", ""),
        "accent": sc.get("accent", "#38BDF8")
    })

print(f"Total video duration: {total_frames / 60:.1f} seconds ({len(beats_out)} scenes)")

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
    "-filter_complex", "[0:a]volume=1.18[v];[1:a]volume=0.20[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
    "out/final_telegram_video.mp4"
], check=True)