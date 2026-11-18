import os, sys, json, time, subprocess, urllib.request, urllib.parse

prompt = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "لماذا تتقشر بوية الجدران بعد الشتاء"
groq_key = os.environ.get("GROQ_API_KEY", "").strip()

print(f"Generating full-screen cinematic storytelling Reel for: {prompt}")

os.makedirs("public/assets", exist_ok=True)
os.makedirs("public/audio", exist_ok=True)
os.makedirs("out", exist_ok=True)
os.makedirs("/tmp/v_src", exist_ok=True)

if not os.path.exists("public/assets/shop_front.jpg"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x0F172A:s=1080x1920:d=1", "-frames:v", "1", "public/assets/shop_front.jpg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Cinematic suspenseful background score loop
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.16*sin(2*PI*45*t)*exp(-5*mod(t,1.0)) + 0.04*sin(2*PI*180*t) + 0.03*sin(2*PI*220*t)':s=44100:d=110",
    "-af", "lowpass=f=750,volume=0.25",
    "public/audio/bg_groove.mp3"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

SHOP_NAME = "\u0645\u062d\u0644 \u062e\u064a\u0628\u0631 \u0627\u0644\u062f\u0647\u0627\u0646\u0627\u062a"
LOCATION  = "\u0627\u0644\u0631\u064a\u0627\u0635 \u2022 \u062d\u064a \u0627\u0644\u062e\u0644\u064a\u062c \u2022 \u0634\u0627\u0631\u0639 \u0627\u0644\u0623\u0645\u064a\u0631 \u0628\u0646\u062f\u0631"

# 1. Generate cinematic science/storytelling script via Groq Llama-3.3-70B
scenes_data = None
if groq_key:
    try:
        sys_msg = (
            "You are an elite master science and medical storytelling director (like Zack D. Films or Kurzgesagt) "
            "creating high-retention viral vertical Reels for محل خيبر الدهانات in Riyadh. "
            "Write an 12-scene gripping, suspenseful storytelling script starting with a massive psychological hook and questions, "
            "explaining the physics and science of wall damage, and revealing the paint shop as the ultimate scientific solution. "
            "Return ONLY valid JSON with key 'scenes': a list of 12 objects, each having: "
            "'visualStyle' (MUST be one of: 'horror_peel', 'sun_blister', 'molecular_bond', 'color_laser', 'luxury_reveal'), "
            "'hookTitle' (3-6 word bold title on screen), "
            "'narrationText' (engaging spoken sentence in natural Saudi dialect), "
            "'accent' (hex color like '#EF4444', '#F59E0B', '#10B981', '#38BDF8', '#A855F7')."
        )
        body = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "response_format": {"type": "json_object"},
            "temperature": 0.85,
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": f"Create a cinematic science storytelling script about: {prompt}"}
            ]
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json",
                "User-Agent": "KhyberCinematic/4.0"
            }
        )
        res = json.loads(urllib.request.urlopen(req, timeout=25).read().decode())
        parsed = json.loads(res["choices"][0]["message"]["content"])
        if isinstance(parsed.get("scenes"), list) and len(parsed["scenes"]) >= 8:
            scenes_data = parsed["scenes"][:12]
            print("Generated cinematic science storytelling script via Groq!")
    except Exception as e:
        print(f"Groq fallback: {e}")

if not scenes_data:
    scenes_data = [
        {"visualStyle": "horror_peel", "hookTitle": "هل تخيلت يوماً...", "narrationText": "هل تخيلت يوماً لماذا تتقشر بوية جدران بيتك رغم أنك دفعت آلاف الريالات؟", "accent": "#EF4444"},
        {"visualStyle": "horror_peel", "hookTitle": "السر المرعب!", "narrationText": "السر يكمن في الفيزياء والمسام الخرسانية التي تشرب الرطوبة بصمت!", "narrationText2": "السر يكمن في الفيزياء والرطوبة التي تدمر الجدار من الداخل!", "accent": "#F59E0B"},
        {"visualStyle": "sun_blister", "hookTitle": "محارق الرياض 50°C", "narrationText": "في صيف الرياض، ترتفع حرارة الجدار إلى خمسين درجة مئوية فيتكسر الدهان التجاري!", "accent": "#F59E0B"},
        {"visualStyle": "molecular_bond", "hookTitle": "الحل الجزيئي الكيميائي", "narrationText": "الحل ليس إعادة الصبغ العشوائي، بل استخدام برايمر عازل يغلق المسام مجهرياً.", "accent": "#10B981"},
        {"visualStyle": "color_laser", "hookTitle": "دقة مطابقة الكمبيوتر", "narrationText": "وفي محل خيبر الدهانات، نستخدم أنظمة خلط كمبيوتر متطورة تطابق لونك بدقة مذهلة.", "accent": "#38BDF8"},
        {"visualStyle": "luxury_reveal", "hookTitle": "فخامة تدوم 10 سنين", "narrationText": "مع دهانات جوتن وسبعمية وسبعة وسبعين الأصلية، يعود بيتك كأنه قصر جديد.", "accent": "#A855F7"},
    ]

# 2. Synthesize calm, suspenseful Saudi voiceover per scene
beats_out = []
total_frames = 0

all_steps = scenes_data + [{
    "isShopEnd": True,
    "visualStyle": "luxury_reveal",
    "hookTitle": "زورونا اليوم في الرياض",
    "narrationText": "حياكم الله في محل خيبر الدهانات بحي الخليج، راسلنا واتساب الحين وفالكم طيب!",
    "accent": "#22C55E"
}]

for i, sc in enumerate(all_steps):
    is_shop = bool(sc.get("isShopEnd", False))
    idx = f"{i+1:02d}"
    raw_mp3 = f"/tmp/v_src/v_{idx}_raw.mp3"
    trim_mp3 = f"/tmp/v_src/v_{idx}_trim.mp3"
    rel_mp3 = f"audio/story_beat_{idx}.mp3"
    final_mp3 = f"public/{rel_mp3}"
    spoken_text = sc.get("narrationText") or sc.get("hookTitle")

    for attempt in range(5):
        time.sleep(0.5 + attempt * 0.3)
        r = subprocess.run([
            "edge-tts", "--voice", "ar-SA-HamedNeural",
            "--rate=-2%", "--pitch=+2Hz",
            "--text", spoken_text, "--write-media", raw_mp3
        ], capture_output=True)
        if r.returncode == 0 and os.path.exists(raw_mp3) and os.path.getsize(raw_mp3) > 1000:
            break
    else:
        fallback_sec = 6.0 if is_shop else 5.0
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono:d={fallback_sec-0.2}", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        frames = round(fallback_sec * 60)
        total_frames += frames
        beats_out.append({
            "isShopEnd": is_shop,
            "visualStyle": sc.get("visualStyle", "horror_peel"),
            "audio": rel_mp3,
            "frames": frames,
            "hookTitle": sc.get("hookTitle", ""),
            "narrationText": spoken_text,
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

    scene_sec = max(4.5, min(6.5, dur + 0.4))
    if is_shop:
        scene_sec = max(6.5, dur + 0.6)

    subprocess.run(["ffmpeg", "-y", "-i", trim_mp3, "-c", "copy", final_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    frames = round(scene_sec * 60)
    total_frames += frames
    beats_out.append({
        "isShopEnd": is_shop,
        "visualStyle": sc.get("visualStyle", "horror_peel"),
        "audio": rel_mp3,
        "frames": frames,
        "hookTitle": sc.get("hookTitle", ""),
        "narrationText": spoken_text,
        "accent": sc.get("accent", "#38BDF8")
    })

print(f"Total cinematic story duration: {total_frames / 60:.1f} seconds ({len(beats_out)} scenes)")

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
    "-filter_complex", "[0:a]volume=1.18[v];[1:a]volume=0.22[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
    "out/final_telegram_video.mp4"
], check=True)