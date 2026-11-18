import os, sys, json, time, subprocess, urllib.request

prompt = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "لماذا تتقشر بوية الجدران وكيف تختار الدهان الصحيح"
groq_key = os.environ.get("GROQ_API_KEY", "").strip()

print(f"Generating 60s 1080x1920 60fps Whiteboard Explainer for: {prompt}")

os.makedirs("public/wb_audio", exist_ok=True)
os.makedirs("out", exist_ok=True)
os.makedirs("/tmp/wb_src", exist_ok=True)

subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.10*sin(2*PI*261.6*t)*exp(-6*mod(t,0.5)) + 0.08*sin(2*PI*329.6*t)*exp(-6*mod(t+0.25,0.5)) + 0.06*sin(2*PI*392.0*t)*exp(-5*mod(t,1.0))':s=44100:d=90",
    "-af", "lowpass=f=1100,volume=0.22",
    "public/wb_audio/bg_whiteboard.mp3"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

SHOP_NAME  = "محل خيبر للدهانات"
LOCATION   = "الرياض • حي الخليج • شارع الأمير بندر"
WHATSAPP   = "0599484068"
OFFER_TEXT = "استشارة ألوان مجانية + دهانات أصلية بضمان"

scenes_data = None
if groq_key:
    try:
        sys_msg = (
            "You are a viral short-form video hook master & whiteboard animation director for a paint shop in Riyadh (محل خيبر للدهانات). "
            "Every video MUST start with a shocking, pattern-interrupt hook in the first 3 seconds (e.g., 'STOP! You are wasting thousands of Riyals on paint...' or 'Look at this wall disaster!'). "
            "SHOW concrete visual examples on white paper: point directly at what is drawn ('Look at this!', 'See why this bubbled?'), "
            "compare wrong vs right, include a funny relatable analogy, and show the 3-step fix. "
            "Total spoken script across 6 scenes must last ~52 seconds (~120-140 lively Saudi Arabic words total). "
            "Return ONLY valid JSON with key 'scenes': a list of exactly 6 objects, each having: "
            "'illustration' (MUST be one of: 'peeling_wall', 'moisture_pores', 'wrong_vs_right', 'funny_comparison', 'roller_steps', 'color_machine'), "
            "'stepTag' (short 2-3 word Arabic hook tag like 'شوف الكارثة ❌'), "
            "'title' (3-5 word punchy Arabic headline), "
            "'narration' (18-24 words in energetic, conversational Saudi Arabic explaining the drawing on screen), "
            "'leftLabel' (short 2-word Arabic label), "
            "'rightLabel' (short 2-word Arabic label), "
            "'callout' (short 3-4 word Arabic stamp/badge text), "
            "'accent' (hex color: '#DC2626', '#D97706', '#16A34A', '#0284C7', or '#7C3AED')."
        )
        body = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "response_format": {"type": "json_object"},
            "temperature": 0.9,
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": f"Create a high-retention, entertaining 6-scene whiteboard explainer with visual examples about: {prompt}"}
            ]
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json",
                "User-Agent": "KhyberWhiteboard/1.0"
            }
        )
        res = json.loads(urllib.request.urlopen(req, timeout=25).read().decode())
        parsed = json.loads(res["choices"][0]["message"]["content"])
        if isinstance(parsed.get("scenes"), list) and len(parsed["scenes"]) >= 5:
            scenes_data = parsed["scenes"][:6]
            print("Generated hooked whiteboard script via Groq!")
    except Exception as e:
        print(f"Groq fallback: {e}")

if not scenes_data:
    scenes_data = [
        {
            "illustration": "peeling_wall",
            "stepTag": "وقف! شوف هنا ❌",
            "title": "ليش بويتك تتقشر بعد 6 شهور؟",
            "narration": "وقف لحظة وشوف هذا الجدار! صاحبه دفع آلاف الريالات، وبعد ستة شهور بس انتفخت البوية وتقشرت مثل قشر الموز!",
            "callout": "خطأ يكلفك مرتين!",
            "accent": "#DC2626"
        },
        {
            "illustration": "moisture_pores",
            "stepTag": "السر المخفي 🔬",
            "title": "الرطوبة وحرارة الرياض 50°",
            "narration": "المشكلة مو في اللون! الخرسانة تشرب رطوبة مخفية، ومع شمس الصيف تتمدد وتدفع الدهان التجاري لبرا لين ينفجر.",
            "callout": "ضغط الرطوبة والحرارة",
            "accent": "#D97706"
        },
        {
            "illustration": "wrong_vs_right",
            "stepTag": "قارن بعينك 👀",
            "title": "شغل تجاري vs شغل أصول",
            "narration": "على اليسار جدار انصبغ مباشرة بدون أساس فتشقق بسرعة، وعلى اليمين جدار أخذ برايمر عازل وبقي ناعم مثل الحرير.",
            "leftLabel": "بدون برايمر ❌",
            "rightLabel": "مع برايمر ✅",
            "accent": "#0284C7"
        },
        {
            "illustration": "funny_comparison",
            "stepTag": "خليك ذكي 😂",
            "title": "لا تلبس بدلة بدون قميص!",
            "narration": "تخيل تلبس أفخم بدلة بدون قميص تحتها! هذا بالضبط اللي يصير لما تشتري أغلى بوية وتحطها على جدار بدون أساس.",
            "callout": "الأساس هو السر!",
            "accent": "#7C3AED"
        },
        {
            "illustration": "roller_steps",
            "stepTag": "الحل بـ 3 خطوات ✅",
            "title": "دهان يعيش معك 10 سنين",
            "narration": "الطريقة الصح بسيطة: أولاً صنفر ونظف الجدار، ثانياً حط وجه برايمر عازل، وثالثاً ادهن وجهين دهان أصلي مقاوم.",
            "callout": "3 خطوات ذهبية",
            "accent": "#16A34A"
        },
        {
            "illustration": "color_machine",
            "stepTag": "دقة الكمبيوتر 🎨",
            "title": "جرب اللون على جدارك أول!",
            "narration": "وفي محل خيبر للدهانات نخلط لك اللون بالكمبيوتر بدقة مية بالمية ونعطيك العينة تجربها على جدار بيتك قبل ما تشتري.",
            "callout": "خلط كمبيوتر + ضمان أصلي",
            "accent": "#0284C7"
        }
    ]

all_scenes = scenes_data + [{
    "isShopEnd": True,
    "illustration": "color_machine",
    "stepTag": "زورونا اليوم",
    "title": SHOP_NAME,
    "narration": "حياكم الله في محل خيبر للدهانات بحي الخليج بالرياض، راسلنا واتساب الحين لاستشارة مجانية وأقوى العروض!",
    "accent": "#16A34A"
}]

scenes_out = []

for i, sc in enumerate(all_scenes):
    idx = f"{i+1:02d}"
    raw_mp3 = f"/tmp/wb_src/raw_{idx}.mp3"
    clean_mp3 = f"public/wb_audio/v_{idx}.mp3"
    rel_mp3 = f"wb_audio/v_{idx}.mp3"
    spoken = sc["narration"]

    for attempt in range(5):
        time.sleep(0.4 + attempt * 0.3)
        r = subprocess.run([
            "edge-tts", "--voice", "ar-SA-HamedNeural",
            "--rate=+6%", "--pitch=+2Hz",
            "--text", spoken, "--write-media", raw_mp3
        ], capture_output=True)
        if r.returncode == 0 and os.path.exists(raw_mp3) and os.path.getsize(raw_mp3) > 1000:
            break
    else:
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:d=7.5", clean_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        scenes_out.append({
            "isShopEnd": bool(sc.get("isShopEnd", False)),
            "audio": rel_mp3,
            "frames": 480,
            "stepTag": sc.get("stepTag", ""),
            "title": sc.get("title", ""),
            "narration": spoken,
            "illustration": sc.get("illustration", "peeling_wall"),
            "leftLabel": sc.get("leftLabel", "بدون برايمر ❌"),
            "rightLabel": sc.get("rightLabel", "مع برايمر ✅"),
            "callout": sc.get("callout", ""),
            "accent": sc.get("accent", "#DC2626")
        })
        continue

    subprocess.run([
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.06:stop_threshold=-42dB,acompressor=threshold=-16dB:ratio=2.8:attack=5:release=50",
        clean_mp3
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", clean_mp3
    ]).decode().strip())

    scenes_out.append({
        "isShopEnd": bool(sc.get("isShopEnd", False)),
        "audio": rel_mp3,
        "frames": round((dur + 0.45) * 60),
        "stepTag": sc.get("stepTag", ""),
        "title": sc.get("title", ""),
        "narration": spoken,
        "illustration": sc.get("illustration", "peeling_wall"),
        "leftLabel": sc.get("leftLabel", "بدون برايمر ❌"),
        "rightLabel": sc.get("rightLabel", "مع برايمر ✅"),
        "callout": sc.get("callout", ""),
        "accent": sc.get("accent", "#DC2626")
    })

TARGET_FRAMES = 3600
current_sum = sum(s["frames"] for s in scenes_out)
scale = TARGET_FRAMES / max(1, current_sum)
total_frames = 0
for idx_s, s in enumerate(scenes_out):
    if idx_s == len(scenes_out) - 1:
        s["frames"] = max(360, TARGET_FRAMES - total_frames)
    else:
        s["frames"] = max(300, round(s["frames"] * scale))
    total_frames += s["frames"]

print(f"Total 60fps Portrait Whiteboard duration: {total_frames / 60:.1f}s ({total_frames} frames)")

with open("public/current_whiteboard.json", "w", encoding="utf-8") as f:
    json.dump({
        "shopName": SHOP_NAME,
        "locationText": LOCATION,
        "whatsapp": WHATSAPP,
        "offerText": OFFER_TEXT,
        "totalFrames": total_frames,
        "scenes": scenes_out
    }, f, ensure_ascii=False, indent=2)

subprocess.run([
    "npx", "remotion", "render", "src/index.ts", "PaintWhiteboard9x16",
    "out/raw_video.mp4", "--codec", "h264", "--crf", "19", "--concurrency=2"
], check=True)

subprocess.run([
    "ffmpeg", "-y", "-i", "out/raw_video.mp4", "-stream_loop", "-1", "-i", "public/wb_audio/bg_whiteboard.mp3",
    "-filter_complex", "[0:a]volume=1.20[v];[1:a]volume=0.20[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
    "out/final_telegram_video.mp4"
], check=True)