import os, sys, json, time, random, hashlib, subprocess, urllib.request, urllib.parse

raw_input = sys.argv[1].strip() if len(sys.argv) > 1 else ""
groq_key = os.environ.get("GROQ_API_KEY", "").strip()
pixabay_key = os.environ.get("PIXABAY_API_KEY", "").strip()

os.makedirs("public/wb_audio", exist_ok=True)
os.makedirs("public/wb_clips", exist_ok=True)
os.makedirs("out", exist_ok=True)
os.makedirs("/tmp/wb_src", exist_ok=True)

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

state["total_generated"] = state.get("total_generated", 0) + 1
cycle_num = state.get("cycle", 1)

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"[Cycle {cycle_num} | Video #{state['total_generated']}] Topic: {prompt}")

# Ambient modern corporate audio bed
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

THEMES = [
    {"name": "Royal Gold & Obsidian", "accent": "#D97706", "secondary": "#FBBF24"},
    {"name": "Emerald Architectural", "accent": "#059669", "secondary": "#34D399"},
    {"name": "Riyadh Terracotta", "accent": "#EA580C", "secondary": "#FB923C"},
    {"name": "Sapphire Contractor", "accent": "#0284C7", "secondary": "#38BDF8"},
]
active_theme = THEMES[(cycle_num + state["total_generated"]) % len(THEMES)]

# Strict verified Pixabay paint/interior video downloader (NEVER accepts random unrelated clips!)
ALLOWED_TAGS = {
    "paint", "painting", "painter", "wall", "roller", "brush", "interior",
    "living room", "room", "renovation", "home", "house", "architecture",
    "decor", "design", "color", "colour", "plaster", "construction", "apartment", "villa"
}
BANNED_TAGS = {
    "food", "cooking", "animal", "dog", "cat", "car", "traffic", "beach",
    "ocean", "forest", "mountain", "space", "galaxy", "flower", "sport", "fitness"
}
used_clip_ids = set()

def fetch_verified_paint_clip(search_query: str, out_mp4: str) -> bool:
    if not pixabay_key:
        return False
    # Force paint/interior context in query
    queries = [search_query, "painting wall roller", "modern living room interior", "paint brush color"]
    for q in queries:
        try:
            url = (
                f"https://pixabay.com/api/videos/?key={urllib.parse.quote(pixabay_key)}"
                f"&q={urllib.parse.quote(q)}&per_page=15&safesearch=true"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "KhyberPaintStudio/3.0"})
            data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
            hits = data.get("hits", [])
            random.shuffle(hits)
            for hit in hits:
                vid_id = hit.get("id")
                if vid_id in used_clip_ids:
                    continue
                tags_str = hit.get("tags", "").lower()
                tag_tokens = {t.strip() for t in tags_str.split(",")}
                if any(b in tags_str for b in BANNED_TAGS):
                    continue
                if not any(a in tags_str for a in ALLOWED_TAGS):
                    continue
                videos = hit.get("videos", {})
                mp4_url = (
                    videos.get("medium", {}).get("url")
                    or videos.get("small", {}).get("url")
                    or videos.get("large", {}).get("url")
                )
                if not mp4_url:
                    continue
                raw_dl = out_mp4 + ".raw.mp4"
                urllib.request.urlretrieve(mp4_url, raw_dl)
                # Normalize clip to 1080x1920 30fps silent H.264 so Remotion OffthreadVideo plays smoothly
                r = subprocess.run([
                    "ffmpeg", "-y", "-i", raw_dl, "-t", "10",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                    "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                    out_mp4
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(raw_dl):
                    os.remove(raw_dl)
                if r.returncode == 0 and os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 30000:
                    used_clip_ids.add(vid_id)
                    print(f"Verified paint clip #{vid_id} ({tags_str}) -> {out_mp4}")
                    return True
        except Exception as e:
            print(f"Pixabay query '{q}' skipped: {e}")
    return False

scenes_data = None
if groq_key:
    for attempt in range(3):
        try:
            sys_msg = (
                "You are an elite Saudi architectural paint advisor and viral short-form video director for 'محل خيبر للدهانات' in Riyadh. "
                "Audience: Riyadh villa owners, contractors, painters, and paint dealers (NOT kids). "
                "Create a 60-second vertical video script (~125-145 lively Saudi Arabic words across 6 scenes). "
                "Scene 1 MUST open with a strong pattern-interrupt hook in the first 3 seconds (shocking cost mistake or contractor secret). "
                "Return ONLY valid JSON with key 'scenes': a list of exactly 6 objects, each having: "
                "'visualType' (MUST be one of: 'before_after_peel', 'sheen_comparison', 'wall_layers_xray', 'cost_calculator', 'color_swatches_wall', 'tinting_machine'), "
                "'videoQuery' (2-3 simple English keywords for real paint/interior video footage: MUST be one of 'painting wall roller', 'luxury living room interior', 'paint brush color', 'home wall renovation', 'modern villa interior'), "
                "'stepTag' (short 2-3 word punchy Arabic badge), "
                "'title' (3-5 word bold Arabic headline), "
                "'narration' (20-25 words in energetic, authoritative Saudi Arabic), "
                "'statBadge' (short 2-4 word Arabic metric like 'توفير 35% من التكلفة' or 'ضمان 10 سنوات'), "
                "'leftMetric' (short 2-3 word Arabic comparison label), "
                "'rightMetric' (short 2-3 word Arabic comparison label)."
            )
            body = json.dumps({
                "model": "llama-3.3-70b-versatile",
                "response_format": {"type": "json_object"},
                "temperature": 0.92,
                "messages": [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": f"Variation #{state['total_generated']} (Cycle {cycle_num}). Create an original 6-scene Saudi Arabic commercial video script about: {prompt}"}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=body,
                headers={
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "KhyberProStudio/3.0"
                }
            )
            res = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
            parsed = json.loads(res["choices"][0]["message"]["content"])
            if isinstance(parsed.get("scenes"), list) and len(parsed["scenes"]) >= 5:
                scenes_data = parsed["scenes"][:6]
                print("Generated custom Groq script!")
                break
        except Exception as e:
            print(f"Groq attempt {attempt+1} error: {e}")
            time.sleep(1.5)

if not scenes_data:
    scenes_data = [
        {
            "visualType": "before_after_peel",
            "videoQuery": "painting wall roller",
            "stepTag": "تنبيه للملاك والمقاولين ⚠️",
            "title": prompt[:42],
            "narration": f"وقف لحظة! قبل ما تبدأ في {prompt}، شوف الغلطة اللي تكلف أصحاب الفلل والمقاولين في الرياض آلاف الريالات وتخرب التشطيب بالكامل.",
            "statBadge": "تجنب خسارة التشطيب",
            "leftMetric": "دهان تجاري يتقشر ❌",
            "rightMetric": "تأسيس أصلي 10 سنوات ✅"
        },
        {
            "visualType": "wall_layers_xray",
            "videoQuery": "home wall renovation",
            "stepTag": "السر الهندسي 📐",
            "title": "4 طبقات تحمي جدارك",
            "narration": "الفرق بين الجدار اللي يتشقق بعد ستة أشهر والجدار الفندقي الناعم هو ترتيب الطبقات: صنفرة، معجون أصلي، برايمر عازل، ووجهين دهان مقاوم.",
            "statBadge": "عمر أطول 3 أضعاف",
            "leftMetric": "بدون برايمر عازل",
            "rightMetric": "نظام حماية متكامل"
        },
        {
            "visualType": "sheen_comparison",
            "videoQuery": "luxury living room interior",
            "stepTag": "مقارنة اللمعة 🔍",
            "title": "مطفي vs ربع لمعة vs نصف لمعة",
            "narration": "المطفي يخفي عيوب اللياسة في الأسقف، وربع لمعة هو ملك المجالس والصالات، أما نصف لمعة فيتحمل الغسيل اليومي في الممرات والمطابخ.",
            "statBadge": "اختر اللمعة الصح",
            "leftMetric": "مطفي للأسقف",
            "rightMetric": "ربع لمعة للمجالس"
        },
        {
            "visualType": "cost_calculator",
            "videoQuery": "modern villa interior",
            "stepTag": "احسبها صح 💰",
            "title": "وفر 30% من ميزانية البوية",
            "narration": "الدهان الأصلي تغطيته أعلى للمتر المربع من التجاري، يعني تشتري براميل أقل وتوفر أجرة يد وتاخذ ضمان حقيقي ضد التبهيت والرطوبة.",
            "statBadge": "تغطية أعلى 35%",
            "leftMetric": "هدر وتكرار أوجه",
            "rightMetric": "تغطية من وجهين"
        },
        {
            "visualType": "color_swatches_wall",
            "videoQuery": "paint brush color",
            "stepTag": "اختبار الإضاءة 💡",
            "title": "لا تختار اللون من الكتالوج فقط!",
            "narration": "إضاءة الليد الدافئة تغير درجة البيج والأبيض على الجدار، عشان كذا نعطيك عينة تجريبية تشوفها في بيتك قبل ما تعتمد الكمية.",
            "statBadge": "عينة تجريبية لبيتك",
            "leftMetric": "لون الكتالوج",
            "rightMetric": "اللون تحت إضاءتك"
        },
        {
            "visualType": "tinting_machine",
            "videoQuery": "painting wall roller",
            "stepTag": "دقة الكمبيوتر 🎨",
            "title": "تطابق ألوان 100% بالكمبيوتر",
            "narration": "في محل خيبر للدهانات نخلط لك أي درجة عالمية بالكمبيوتر بدقة متناهية مع حساب الكمية الدقيقة لشقتك أو مشروعك مجاناً.",
            "statBadge": "خلط كمبيوتر معتمد",
            "leftMetric": "تخمين عشوائي",
            "rightMetric": "حساب دقيق بالملي"
        }
    ]

all_scenes = scenes_data + [{
    "isShopEnd": True,
    "visualType": "tinting_machine",
    "videoQuery": "modern villa interior",
    "stepTag": "زورونا في الرياض",
    "title": SHOP_NAME,
    "narration": "حياكم الله في محل خيبر للدهانات بحي الخليج شارع الأمير بندر بالرياض، راسلنا واتساب الحين لحساب كمية البوية مجاناً وأقوى عروض المقاولين والملاك!",
    "statBadge": OFFER_TEXT,
    "leftMetric": "حي الخليج",
    "rightMetric": "شارع الأمير بندر"
}]

scenes_out = []
FPS = 30

for i, sc in enumerate(all_scenes):
    idx = f"{i+1:02d}"
    raw_mp3 = f"/tmp/wb_src/raw_{idx}.mp3"
    clean_mp3 = f"public/wb_audio/v_{idx}.mp3"
    rel_mp3 = f"wb_audio/v_{idx}.mp3"
    clip_mp4 = f"public/wb_clips/clip_{idx}.mp4"
    rel_clip = f"wb_clips/clip_{idx}.mp4"
    spoken = sc["narration"]

    has_video = fetch_verified_paint_clip(sc.get("videoQuery", "painting wall roller"), clip_mp4)

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
        "video": rel_clip if has_video else "",
        "visualType": sc.get("visualType", "before_after_peel"),
        "frames": round((dur + 0.4) * FPS),
        "stepTag": sc.get("stepTag", ""),
        "title": sc.get("title", ""),
        "narration": spoken,
        "statBadge": sc.get("statBadge", ""),
        "leftMetric": sc.get("leftMetric", ""),
        "rightMetric": sc.get("rightMetric", ""),
        "accent": active_theme["accent"],
        "secondary": active_theme["secondary"]
    })

TARGET_FRAMES = 60 * FPS
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