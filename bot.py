import os
import requests
import json

# جلب الـ Secrets الأربعة بالكامل
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK", "https://google.com")

if not GROQ_API_KEY:
    print("ERROR: Missing GROQ_API_KEY")
    exit(1)

# الخمس ألعاب المستهدفة (عربي وإنجليزي = 10 صفحات)
GAMES_CONFIG = [
    {"slug": "pubg-mobile-mod", "game": "PUBG Mobile / ببجي موبايل", "lang": "ar"},
    {"slug": "pubg-mobile-mod-en", "game": "PUBG Mobile", "lang": "en"},
    {"slug": "8-ball-pool-mod", "game": "8 Ball Pool / 8 بال بول", "lang": "ar"},
    {"slug": "8-ball-pool-mod-en", "game": "8 Ball Pool", "lang": "en"},
    {"slug": "roblox-mod-menu", "game": "Roblox / روبلوكس", "lang": "ar"},
    {"slug": "roblox-mod-menu-en", "game": "Roblox", "lang": "en"},
    {"slug": "clash-of-clans-mod", "game": "Clash of Clans / كلاش أوف كلانس", "lang": "ar"},
    {"slug": "clash-of-clans-mod-en", "game": "Clash of Clans", "lang": "en"},
    {"slug": "free-fire-mod", "game": "Free Fire / فري فاير", "lang": "ar"},
    {"slug": "free-fire-mod-en", "game": "Free Fire", "lang": "en"}
]

def send_telegram_msg(message):
    """ إرسال إشعار للـ Telegram عند انتهاء التوليد """
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Telegram error: {e}")

def generate_ai_content(item):
    """ توليد الكلمات المفتاحية الـ SEO الذهبية للتهكير + المقال بواسطة Groq """
    if item["lang"] == "ar":
        prompt = f"""أنت خبير SEO واختراق ألعاب. ادرس لعبة "{item['game']}" واستخرج أقوى الكلمات المفتاحية الذهبية الأكثر بحثاً من الأجهزة والجوالات (مثل: هكر، aimbot، sharp shooter، مجاناً، جواهر، شدات، ضد الحظر، mod menu).
ثم اكتب مقالاً تسويقياً طويلاً ومغرياً جداً يغري اللاعبين والأطفال بالتحميل فوراً.

أرجع النتيجة بصيغة JSON فقط بهذه الهيكلية:
{{
  "title": "عنوان المقال الرئيسي القوي والمغري جداً للتحميل",
  "keywords": "الكلمات المفتاحية الـ 10 التي استخرجتها مفصولة بفاصلة",
  "content": "نص المقال المفصل بالعناوين الفرعية باستخدام # و ## بدون أي روابط أو HTML"
}}"""
    else:
        prompt = f"""You are an SEO & Gaming Mod expert. Analyze the game "{item['game']}" and generate highest-converting viral search keywords (Aimbot, Mod Menu, Free Currency, Anti-Ban, Sharp Shooter, Unlimited Hacks, Injector).
Then write a long, highly-persuasive promotional landing page guide.

Return ONLY a valid JSON object in this format:
{{
  "title": "High-converting catchy title",
  "keywords": "10 AI generated keywords separated by comma",
  "content": "Detailed article body using # and ## for headers. No HTML tags, no URLs."
}}"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "temperature": 0.7
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        if res.status_code == 200:
            return json.loads(res.json()["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"Error fetching AI content for {item['slug']}: {e}")

    return {
        "title": f"Download {item['game']} VIP Mod Hack",
        "keywords": "mod, hack, free, aimbot, vip",
        "content": "Get the latest mod menu update now with anti-ban protection."
    }

def build_dark_html(item, ai_data):
    """ المظهر الداكن + تتبع الزوار لحظياً عبر التليجرام """
    paragraphs = ai_data["content"].split("\n\n")
    body_content = ""
    for p in paragraphs:
        p_str = p.strip()
        if p_str.startswith("#"):
            clean_t = p_str.replace("#", "").strip()
            body_content += f"<h2 style='color:#38bdf8; margin-top:30px; font-size:1.3rem; border-right:4px solid #3b82f6; padding-right:10px;'>{clean_t}</h2>\n"
        elif p_str:
            body_content += f"<p style='line-height:1.9; color:#cbd5e1; font-size:1.05rem; margin-bottom:18px;'>{p_str}</p>\n"

    btn_label = "⚡ اضغط هنا للتحميل المباشر وتفعيل الـ VIP" if item["lang"] == "ar" else "⚡ Click Here for Instant VIP Mod Download"
    
    # كود تتبع الزائر وإرسال تنبيه للتليجرام عند فتح الصفحة
    visitor_tracker_script = f"""
    <script>
        (function() {{
            var botToken = "{TELEGRAM_BOT_TOKEN or ''}";
            var chatId = "{TELEGRAM_CHAT_ID or ''}";
            if(botToken && chatId) {{
                var msg = "👁️ <b>زائر جديد دخل الصفحة!</b>\\n\\n🎮 الصفحة: " + encodeURIComponent(document.title) + "\\n🔗 الرابط: " + encodeURIComponent(window.location.href);
                fetch("https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + chatId + "&text=" + msg + "&parse_mode=HTML")
                .catch(function(e){{}});
            }}
        }})();
    </script>
    """

    html = f"""<!DOCTYPE html>
<html lang="{item['lang']}" dir="{"rtl" if item['lang']=="ar" else "ltr"}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="keywords" content="{ai_data['keywords']}">
    <title>{ai_data['title']}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 15px; }}
        .card {{ max-width: 800px; margin: 20px auto; background: #1e293b; padding: 30px; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        .badge {{ display: inline-block; background: #3b82f6; color: #fff; font-size: 0.8rem; font-weight: bold; padding: 4px 12px; border-radius: 20px; margin-bottom: 15px; text-transform: uppercase; }}
        h1 {{ color: #ffffff; font-size: 1.7rem; line-height: 1.4; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 15px; }}
        .btn-box {{ text-align: center; margin: 30px 0; padding: 25px; background: #0f172a; border-radius: 12px; border: 1px dashed #3b82f6; }}
        .dl-btn {{ display: inline-block; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #ffffff !important; font-weight: 800; font-size: 1.25rem; padding: 18px 38px; border-radius: 10px; text-decoration: none; box-shadow: 0 0 20px rgba(37,99,235,0.5); transition: all 0.3s ease; }}
        .dl-btn:hover {{ transform: scale(1.03); box-shadow: 0 0 30px rgba(59,130,246,0.8); }}
        .footer-note {{ text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 20px; }}
    </style>
    {visitor_tracker_script}
</head>
<body>
    <div class="card">
        <span class="badge">VIP STATUS: ONLINE ✅</span>
        <h1>{ai_data['title']}</h1>
        
        <div class="btn-box">
            <a href="{MONETAG_AD_LINK}" target="_blank" class="dl-btn">{btn_label}</a>
        </div>

        <div>
            {body_content}
        </div>

        <div class="btn-box">
            <a href="{MONETAG_AD_LINK}" target="_blank" class="dl-btn">{btn_label}</a>
        </div>
        <div class="footer-note">Protected by Anti-Cheat Shield v4.1 • Fast Server Direct Download</div>
    </div>
</body>
</html>"""
    return html

def main():
    os.makedirs("posts", exist_ok=True)
    links_list = ""
    tg_msg = "<b>🚀 تم بناء الـ 10 صفحات الهبوط المظلمة وتفعيل تتبع الزوار بنجاح!</b>\n\n"
    
    for item in GAMES_CONFIG:
        print(f"Generating page for: {item['slug']}...")
        ai_data = generate_ai_content(item)
        full_html = build_dark_html(item, ai_data)
        
        # حفظ كل صفحة بشكل مستقل
        with open(f"posts/{item['slug']}.html", "w", encoding="utf-8") as f:
            f.write(full_html)
            
        links_list += f"""<li style="margin-bottom: 15px;">
            <a href="posts/{item['slug']}.html" style="color: #38bdf8; text-decoration: none; font-size: 1.1rem; font-weight: bold;">
               🎮 {ai_data['title']}
            </a>
        </li>\n"""
        
        tg_msg += f"• <a href='https://gaba-101010.github.io/GamesMod/posts/{item['slug']}.html'>{ai_data['title']}</a>\n"

    # إنشاء صفحة الـ index الرئيسية
    index_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Mods & VIP Tools Portal</title>
    <style>
        body {{ font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }}
        .box {{ max-width: 800px; margin: 20px auto; background: #1e293b; padding: 30px; border-radius: 16px; border: 1px solid #334155; }}
        h1 {{ color: #38bdf8; font-size: 1.6rem; margin-bottom: 25px; border-bottom: 1px solid #334155; padding-bottom: 10px; }}
        ul {{ list-style: none; padding: 0; }}
    </style>
</head>
<body>
    <div class="box">
        <h1>🔥 بوابة أدوات وتحديثات الألعاب (VIP Mod Pages)</h1>
        <ul>
            {links_list}
        </ul>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # إرسال قائمة الروابط لتليجرام
    send_telegram_msg(tg_msg)
    print("ALL 10 PAGES GENERATED & TRACKER ENABLED!")

if __name__ == "__main__":
    main()
