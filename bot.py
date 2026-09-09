import os
import requests
import re

# جلب الـ Secrets الأربعة بالكامل
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK", "https://google.com")

if not GROQ_API_KEY:
    print("ERROR: Missing GROQ_API_KEY")
    exit(1)

# الخمس ألعاب المستهدفة (عربي وإنجليزي منفصلان تماماً)
GAMES_CONFIG = [
    {"slug": "pubg-mobile-mod", "game": "PUBG Mobile", "lang": "ar", "keywords_hint": "شارب شوتر, كشف اماكن, ثبات سلاح, ملف 90 فريم, هكر ببجي, شدات مجانا"},
    {"slug": "pubg-mobile-mod-en", "game": "PUBG Mobile", "lang": "en", "keywords_hint": "Sharp Shooter, Aimbot, Wallhack, 90 FPS Mod, Free UC, Anti-Ban"},
    {"slug": "8-ball-pool-mod", "game": "8 Ball Pool", "lang": "ar", "keywords_hint": "تهكير 8 بال بول, مسار طويل, كوينز مجانا, هكر سهم طويل, مد منيو"},
    {"slug": "8-ball-pool-mod-en", "game": "8 Ball Pool", "lang": "en", "keywords_hint": "Long Line Hack, Unlimited Coins, Guideline Hack, Mod Menu"},
    {"slug": "roblox-mod-menu", "game": "Roblox", "lang": "ar", "keywords_hint": "هكر روبلوكس, روبوكس مجانا, طيران روبلوكس, مود منيو روبلوكس, سرعة"},
    {"slug": "roblox-mod-menu-en", "game": "Roblox", "lang": "en", "keywords_hint": "Free Robux, Fly Hack, Wallhack, Roblox Mod Menu, God Mode"},
    {"slug": "clash-of-clans-mod", "game": "Clash of Clans", "lang": "ar", "keywords_hint": "مجواهر غير محدودة, سيرفر خاص, تهكير كلاش اوف كلانس, اكسير مجاني"},
    {"slug": "clash-of-clans-mod-en", "game": "Clash of Clans", "lang": "en", "keywords_hint": "Unlimited Gems, Private Server, CoC Mod APK, Free Elixir"},
    {"slug": "free-fire-mod", "game": "Free Fire", "lang": "ar", "keywords_hint": "جواهر فري فاير, ثبات الايم, هكر فري فاير, كشف المكان, التحديث الجديد"},
    {"slug": "free-fire-mod-en", "game": "Free Fire", "lang": "en", "keywords_hint": "Free Diamonds, Headshot Hack, Auto Aim, Free Fire Mod Menu"}
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
    """ توليد المقال كاملاً بتنسيق Markdown مفصل لتجنب أخطاء JSON """
    if item["lang"] == "ar":
        prompt = f"""أنت خبير متقدم في SEO واختراق الألعاب ومحتوى الجيمينج الجذاب للأطفال والشباب.
اكتب مقالاً تسويقياً طويلاً جداً ومفصلاً باللغة العربية الفصحى فقط عن أحدث تحديث وتهكير للعبة "{item['game']}".

استخدم الكلمات المفتاحية الأكثر بحثاً مثل: {item['keywords_hint']}.

الشروط المطلوبة:
1. السطر الأول في استجابتك يجب أن يكون العنوان الرئيسي فقط ويكون جذاباً وتنافسياً جداً (مثل: تحميل أحدث مود منيو {item['game']} مع كشف أماكن وضد الحظر).
2. باقي النص مقال طويل مفصل يحتوي على العناوين الفرعية التالية باستخدام # و ##:
   - مميزات التحديث الأخير والخصائص الخارقة.
   - طريقة التفعيل والأمان ضد الحظر (Anti-Ban).
   - إرشادات التحميل المباشر.
3. اكتب باللغة العربية بالكامل دون خلط الإنجليزي بالكلمات. لا تضع أي روابط خارجية أو وسم HTML."""
    else:
        prompt = f"""You are an SEO & Gaming Mod expert creating high-converting viral landing pages for gamers.
Write a comprehensive, highly persuasive long-form guide in pure English for the latest mod hack of "{item['game']}".

Incorporate these highly searched keywords naturally: {item['keywords_hint']}.

Requirements:
1. The first line MUST be the main catchy Title only (e.g., Download Ultimate {item['game']} Mod Menu VIP Anti-Ban).
2. The rest must be a detailed article using Markdown (# and ## for headers) covering:
   - Key Features & Injector Capabilities.
   - Anti-Ban Security & Installation Guide.
   - How to Activate VIP Features.
3. Do NOT include any external URLs or HTML tags."""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=40)
        if res.status_code == 200:
            raw_text = res.json()["choices"][0]["message"]["content"].strip()
            lines = raw_text.split("\n")
            title = lines[0].replace("#", "").strip()
            content = "\n".join(lines[1:]).strip()
            return {"title": title, "content": content, "keywords": item["keywords_hint"]}
    except Exception as e:
        print(f"Error fetching AI content for {item['slug']}: {e}")

    # Fallback في حال الانقطاع المفاجئ للشبكة
    default_title = f"تحميل تحديث مود منيو {item['game']} VIP" if item["lang"] == "ar" else f"Download {item['game']} Mod Menu VIP Update"
    return {
        "title": default_title,
        "content": f"## مميزات المود المباشر\nاحصل على كافة الخصائص المتقدمة وتجاوز الحظر للتحديث الأخير من {item['game']}.",
        "keywords": item["keywords_hint"]
    }

def build_dark_html(item, ai_data):
    """ المظهر الداكن (Dark Gaming Theme) + تتبع الزوار عبر التليجرام """
    paragraphs = ai_data["content"].split("\n\n")
    body_content = ""
    for p in paragraphs:
        p_str = p.strip()
        if p_str.startswith("#"):
            clean_t = re.sub(r'^#+\s*', '', p_str)
            body_content += f"<h2 style='color:#38bdf8; margin-top:30px; font-size:1.3rem; border-right:4px solid #3b82f6; padding-right:10px;'>{clean_t}</h2>\n"
        elif p_str:
            body_content += f"<p style='line-height:1.9; color:#cbd5e1; font-size:1.05rem; margin-bottom:18px;'>{p_str}</p>\n"

    btn_label = "⚡ اضغط هنا للتحميل المباشر وتفعيل الـ VIP" if item["lang"] == "ar" else "⚡ Click Here for Instant VIP Mod Download"
    
    # كود تتبع الزائر بالـ JavaScript
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
        .badge {{ display: inline-block; background: #22c55e; color: #fff; font-size: 0.8rem; font-weight: bold; padding: 4px 12px; border-radius: 20px; margin-bottom: 15px; text-transform: uppercase; }}
        h1 {{ color: #ffffff; font-size: 1.6rem; line-height: 1.4; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 15px; }}
        .btn-box {{ text-align: center; margin: 30px 0; padding: 25px; background: #0f172a; border-radius: 12px; border: 1px dashed #3b82f6; }}
        .dl-btn {{ display: inline-block; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #ffffff !important; font-weight: 800; font-size: 1.25rem; padding: 18px 38px; border-radius: 10px; text-decoration: none; box-shadow: 0 0 20px rgba(37,99,235,0.5); transition: all 0.3s ease; }}
        .dl-btn:hover {{ transform: scale(1.03); box-shadow: 0 0 30px rgba(59,130,246,0.8); }}
        .footer-note {{ text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 20px; }}
    </style>
    {visitor_tracker_script}
</head>
<body>
    <div class="card">
        <span class="badge">VIP STATUS: ONLINE & UPDATED ✅</span>
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
    tg_msg = "<b>🚀 تم بناء وتحديث الـ 10 صفحات الهبوط بالكامل!</b>\n\n"
    
    for item in GAMES_CONFIG:
        print(f"Generating article for: {item['slug']}...")
        ai_data = generate_ai_content(item)
        full_html = build_dark_html(item, ai_data)
        
        # استبدال وتحديث الملف القديم بملف جديد
        with open(f"posts/{item['slug']}.html", "w", encoding="utf-8") as f:
            f.write(full_html)
            
        links_list += f"""<li style="margin-bottom: 15px;">
            <a href="posts/{item['slug']}.html" style="color: #38bdf8; text-decoration: none; font-size: 1.1rem; font-weight: bold;">
               🎮 {ai_data['title']}
            </a>
        </li>\n"""
        
        tg_msg += f"• <a href='https://gaba-101010.github.io/GamesMod/posts/{item['slug']}.html'>{ai_data['title']}</a>\n"

    # إنشاء صفحة index الرئيسية المظلمة
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

    # إرسال تقرير التليجرام
    send_telegram_msg(tg_msg)
    print("ALL 10 PAGES GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
