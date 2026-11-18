import os, sys, json, time, random, hashlib, subprocess, urllib.request, urllib.parse

raw_input = sys.argv[1].strip() if len(sys.argv) > 1 else ""
groq_key = os.environ.get("GROQ_API_KEY", "").strip()

os.makedirs("public/wb_audio", exist_ok=True)
os.makedirs("public/wb_frames", exist_ok=True)
os.makedirs("out", exist_ok=True)
os.makedirs("/tmp/wb_src", exist_ok=True)

# Load 60+ viral paint topics & anti-repeat state
with open("scripts/topics_bank.json", "r", encoding="utf-8") as f:
    TOPICS_BANK = json.load(f)

STATE_FILE = "scripts/used_topics.json"
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception:
        state = {"used_indices": [], "cycle": 1, "total_generated": 0}
else:
    state = {"used_indices": [], "cycle": 1, "total_generated": 0}

TRIGGER_WORDS = {
    "create a video", "create video", "make a video", "make video", "video",
    "جديد", "فيديو", "سوي فيديو", "اعمل فيديو", "ابغى فيديو", "فيديو جديد"
}

is_auto_mode = (not raw_input) or (raw_input.lower() in TRIGGER_WORDS) or (len(raw_input) < 12)

available = [i for i in range(len(TOPICS_BANK)) if i not in state["used_indices"]]
if not available:
    state["used_indices"] = []
    state["cycle"] = state.get("cycle", 1) + 1
    available = list(range(len(TOPICS_BANK)))

if is_auto_mode:
    chosen_idx = random.choice(available)
    prompt = TOPICS_BANK[chosen_idx]
    state["used_indices"].append(chosen_idx)
else:
    prompt = raw_input
    # Still advance cycle variety even on custom prompts
    chosen_idx = state.get("total_generated", 0) % len(TOPICS_BANK)

state["total_generated"] = state.get("total_generated", 0) + 1
cycle_num = state.get("cycle", 1)

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"[Cycle {cycle_num} | Video #{state['total_generated']}] Topic: {prompt}")

# Subtle luxury corporate ambient bed
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.08*sin(2*PI*220.0*t)*exp(-4*mod(t,1.0)) + 0.06*sin(2*PI*277.18*t)*exp(-4*mod(t+0.5,1.0)) + 0.05*sin(2*PI*329.63*t)*exp(-3*mod(t,2.0))':s=44100:d=90",
    "-af", "lowpass=f=950,volume=0.18",
    "public/wb_audio/bg_whiteboard.mp3"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

SHOP_NAME  = "محل خيبر للدهانات"
LOCATION   = "الرياض • حي الخليج • شارع الأمير بندر"
WHATSAPP   = "0599484068"
OFFER_TEXT = "استشارة ألوان مجانية + دهانات أصلية بضمان"

# Rotate visual theme per cycle so repeated topics in Cycle 2+ look brand new
THEMES = [
    {"name": "Royal Gold & Obsidian", "bg": "#0B0F19", "accent": "#D97706", "badgeBg": "#FEF3C7", "badgeText": "#92400E"},
    {"name": "Emerald Architectural", "bg": "#06141B", "accent": "#059669", "badgeBg": "#D1FAE5", "badgeText": "#065F46"},
    {"name": "Riyadh Terracotta Luxury", "bg": "#140D0B", "accent": "#EA580C", "badgeBg": "#FFEDD5", "badgeText": "#9A3412"},
    {"name": "Sapphire Contractor Pro", "bg": "#09111E", "accent": "#0284C7", "badgeBg": "#E0F2FE", "badgeText": "#075985"},
]
active_theme = THEMES[(cycle_num + state["total_generated"]) % len(THEMES)]

scenes_data = None
if groq_key:
    for attempt in range(3):
        try:
            sys_msg = (
                "You are an elite Saudi architectural paint advisor and viral short-form video director for 'محل خيبر للدهانات' in Riyadh. "
                "Your audience is Riyadh villa owners, building contractors, painters, and paint dealers—NOT kids. "
                "Create a high-retention 60-second vertical video script (~125-145 lively Saudi Arabic words across 6 scenes). "
                "Scene 1 MUST open with a powerful, pattern-interrupt hook in the first 3 seconds (shocking cost mistake, contractor secret, or visual proof). "
                "Each scene MUST include a detailed English photorealistic image prompt ('visualPrompt') that EXACTLY depicts what the Arabic voiceover is talking about in that scene "
                "(e.g., luxury Saudi majlis wall painting, close-up of peeling exterior concrete paint in Riyadh sun, professional painter applying primer roller, paint tinting machine, etc. — NO text inside image, NO cartoons). "
                "Return ONLY valid JSON with key 'scenes': a list of exactly 6 objects, each having: "
                "'stepTag' (short 2-3 word punchy Arabic badge), "
                "'title' (3-5 word bold Arabic headline), "
                "'narration' (20-25 words in natural, authoritative, engaging Saudi Arabic), "
                "'visualPrompt' (20-30 words in English describing a photorealistic 9:16 vertical architectural/paint photograph matching this exact narration), "
                "'statBadge' (short 2-4 word Arabic key metric or pro tip like 'توفير 35% من التكلفة' or 'ضمان 10 سنوات'), "
                "'motion' (one of: 'zoom_in', 'zoom_out', 'pan_left', 'pan_right')."
            )
            body = json.dumps({
                "model": "llama-3.3-70b-versatile",
                "response_format": {"type": "json_object"},
                "temperature": 0.92,
                "messages": [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": f"Variation #{state['total_generated']} (Cycle {cycle_num}). Create an original, high-impact 6-scene Saudi Arabic video script with exact photorealistic visual prompts about: {prompt}"}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=body,
                headers={
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "KhyberProStudio/2.0"
                }
            )
            res = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
            parsed = json.loads(res["choices"][0]["message"]["content"])
            if isinstance(parsed.get("scenes"), list) and len(parsed["scenes"]) >= 5:
                scenes_data = parsed["scenes"][:6]
                print("Successfully generated custom Groq script + scene-matched visual prompts!")
                break
        except Exception as e:
            print(f"Groq attempt {attempt+1} error: {e}")
            time.sleep(1.5)

if not scenes_data:
    # Topic-aware dynamic fallback so even without Groq it uses the exact chosen topic!
    scenes_data = [
        {
            "stepTag": "تنبيه للملاك والمقاولين ⚠️",
            "title": prompt[:42],
            "narration": f"قبل ما تبدأ في موضوع {prompt}، انتبه من الغلطة اللي تكلف أصحاب الفلل والمقاولين في الرياض آلاف الريالات وتخرب التشطيب بالكامل.",
            "visualPrompt": "Photorealistic luxury modern Saudi villa living room interior wall painting renovation, dramatic architectural lighting, vertical 9:16",
            "statBadge": "تجنب خسارة التشطيب",
            "motion": "zoom_in"
        },
        {
            "stepTag": "المشكلة في الموقع 🔍",
            "title": "ليش يفشل الشغل التجاري؟",
            "narration": "أغلب المشاكل تبدأ لما يتم تجاهل تجهيز السطح أو اختيار مواد تجارية ما تتحمل حرارة الرياض ورطوبة التكييف، والنتيجة تقشر وتشقق سريع.",
            "visualPrompt": "Close up macro photograph of cracked peeling wall paint on concrete wall in bright sunlight, realistic architectural defect",
            "statBadge": "حرارة 50° تكشف الجودة",
            "motion": "pan_left"
        },
        {
            "stepTag": "الفرق الهندسي 📐",
            "title": "الأساس الصحيح يضاعف العمر",
            "narration": "الفرق بين الدهان اللي يعيش سنة والدهان اللي يعيش عشر سنين هو طبقة البرايمر العازل والمعجون الأصلي قبل الوجه النهائي.",
            "visualPrompt": "Professional painter applying white primer coat with paint roller on smooth plastered wall, clean modern construction site",
            "statBadge": "عمر أطول 3 أضعاف",
            "motion": "zoom_out"
        },
        {
            "stepTag": "نصيحة الخبراء 💡",
            "title": "اختيار الدرجة واللمعة",
            "narration": "سواء كنت مقاول تستلم مشروع أو صاحب بيت تأسس مجلسك، اختيار اللمعة المناسبة والدهان القابل للغسيل يوفر عليك صيانة مستمرة.",
            "visualPrompt": "Luxury beige and greige paint color swatches next to modern Saudi majlis interior design, warm LED lighting, photorealistic",
            "statBadge": "قابل للغسيل ومقاوم",
            "motion": "pan_right"
        },
        {
            "stepTag": "دقة الكمبيوتر 🎨",
            "title": "تطابق الألوان 100%",
            "narration": "في محل خيبر للدهانات نخلط لك أي درجة لون بالكمبيوتر بدقة متناهية مع عينات تجريبية تشوفها على جدارك تحت إضاءة بيتك.",
            "visualPrompt": "Modern automated paint tinting and color mixing machine in a clean professional paint store, vibrant pigments, realistic photo",
            "statBadge": "خلط كمبيوتر معتمد",
            "motion": "zoom_in"
        },
        {
            "stepTag": "قرارك الصح ✅",
            "title": "جودة أصلية وسعر منافس",
            "narration": "لا تخاطر بتشطيب بيتك أو مشروعك مع مواد مجهولة، اعتمد على دهانات أصلية بضمان واستشارة فنية تحسب لك الكمية بالملي.",
            "visualPrompt": "Finished luxury modern Riyadh villa interior hall with flawless smooth matte cream walls and elegant lighting, architectural photography",
            "statBadge": "ضمان الجودة الأصلية",
            "motion": "zoom_out"
        }
    ]

all_scenes = scenes_data + [{
    "isShopEnd": True,
    "stepTag": "زورونا في الرياض",
    "title": SHOP_NAME,
    "narration": "حياكم الله في محل خيبر للدهانات بحي الخليج شارع الأمير بندر بالرياض، راسلنا واتساب الحين لحساب كمية البوية مجاناً وأقوى عروض المقاولين والملاك!",
    "visualPrompt": "Modern luxury paint showroom interior with neatly arranged paint cans and color sample wall, warm lighting, photorealistic",
    "statBadge": OFFER_TEXT,
    "motion": "zoom_in"
}]

def fetch_scene_image(visual_prompt: str, out_path: str, seed: int):
    clean_p = f"{visual_prompt}, architectural photography, ultra detailed, 8k, no text, no watermark"
    encoded = urllib.parse.quote(clean_p)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1920&nologo=true&seed={seed}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 KhyberPaintBot/2.0"})
            data = urllib.request.urlopen(req, timeout=35).read()
            if len(data) > 15000:
                with open(out_path, "wb") as img_f:
                    img_f.write(data)
                return True
        except Exception as e:
            print(f"Image fetch retry {attempt+1}: {e}")
            time.sleep(2)
    # Fallback: generate rich textured architectural gradient backdrop via FFmpeg so it NEVER fails
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"gradients=s=1080x1920:c0=#1E293B:c1=#0F172A:x0=0:y0=0:x1=1080:y1=1920:d=1",
        "-frames:v", "1", out_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True

scenes_out = []
FPS = 30

for i, sc in enumerate(all_scenes):
    idx = f"{i+1:02d}"
    raw_mp3 = f"/tmp/wb_src/raw_{idx}.mp3"
    clean_mp3 = f"public/wb_audio/v_{idx}.mp3"
    rel_mp3 = f"wb_audio/v_{idx}.mp3"
    img_path = f"public/wb_frames/frame_{idx}.jpg"
    rel_img = f"wb_frames/frame_{idx}.jpg"
    spoken = sc["narration"]

    seed = int(hashlib.md5(f"{prompt}_{cycle_num}_{i}".encode()).hexdigest()[:8], 16)
    fetch_scene_image(sc.get("visualPrompt", prompt), img_path, seed)

    tts_ok = False
    for attempt in range(5):
        time.sleep(0.4 + attempt * 0.4)
        r = subprocess.run([
            "edge-tts", "--voice", "ar-SA-HamedNeural",
            "--rate=+7%", "--pitch=+1Hz",
            "--text", spoken, "--write-media", raw_mp3
        ], capture_output=True)
        if r.returncode == 0 and os.path.exists(raw_mp3) and os.path.getsize(raw_mp3) > 1000:
            tts_ok = True
            break

    if not tts_ok:
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:d=8.0", clean_mp3], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        dur = 8.0
    else:
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
        "image": rel_img,
        "frames": round((dur + 0.4) * FPS),
        "stepTag": sc.get("stepTag", ""),
        "title": sc.get("title", ""),
        "narration": spoken,
        "statBadge": sc.get("statBadge", ""),
        "motion": sc.get("motion", "zoom_in"),
        "accent": active_theme["accent"]
    })

TARGET_FRAMES = 60 * FPS  # Exact 60.0s at 30fps = 1800 frames
current_sum = sum(s["frames"] for s in scenes_out)
scale = TARGET_FRAMES / max(1, current_sum)
total_frames = 0
for idx_s, s in enumerate(scenes_out):
    if idx_s == len(scenes_out) - 1:
        s["frames"] = max(180, TARGET_FRAMES - total_frames)
    else:
        s["frames"] = max(150, round(s["frames"] * scale))
    total_frames += s["frames"]

print(f"Total 30fps Portrait Video duration: {total_frames / FPS:.1f}s ({total_frames} frames)")

with open("public/current_whiteboard.json", "w", encoding="utf-8") as f:
    json.dump({
        "shopName": SHOP_NAME,
        "locationText": LOCATION,
        "whatsapp": WHATSAPP,
        "offerText": OFFER_TEXT,
        "topicTitle": prompt,
        "theme": active_theme,
        "totalFrames": total_frames,
        "scenes": scenes_out
    }, f, ensure_ascii=False, indent=2)

subprocess.run([
    "npx", "remotion", "render", "src/index.ts", "PaintWhiteboard9x16",
    "out/raw_video.mp4", "--codec", "h264", "--crf", "20", "--concurrency=2"
], check=True)

subprocess.run([
    "ffmpeg", "-y", "-i", "out/raw_video.mp4", "-stream_loop", "-1", "-i", "public/wb_audio/bg_whiteboard.mp3",
    "-filter_complex", "[0:a]volume=1.22[v];[1:a]volume=0.18[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
    "out/final_telegram_video.mp4"
], check=True)