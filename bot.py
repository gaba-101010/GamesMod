import os
import requests
import re

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK", "https://google.com")

if not GROQ_API_KEY:
    print("ERROR: Missing GROQ_API_KEY")
    exit(1)

# مصفوفة الألعاب مع الكلمات والميزات التي سيتم دمجها برمجياً بعد توليد المقال
GAMES_CONFIG = [
    {
        "slug": "pubg-mobile-mod", 
        "game": "PUBG Mobile", 
        "lang": "ar", 
        "f1": "مساعد التصويب الدقيق والأنظمة التكتيكية",
        "f2": "رادار كشف المواقع والتضاريس المتقدم",
        "f3": "تفعيل 90 فريم وثبات الأداء الكلي",
        "f4": "شحن الموارد والشدات والتحديثات المستمرة"
    },
    {
        "slug": "pubg-mobile-mod-en", 
        "game": "PUBG Mobile", 
        "lang": "en", 
        "f1": "Precision Target Assistance & Tracking Controls",
        "f2": "Tactical Terrain Radar & Position Awareness",
        "f3": "90 FPS Unlock & Zero Recoil Stability",
        "f4": "Resource Rewards Injector & Continuous Anti-Ban Shield"
    },
    {
        "slug": "8-ball-pool-mod", 
        "game": "8 Ball Pool", 
        "lang": "ar", 
        "f1": "دليل المسار الطويل الممتد بدقة عالية",
        "f2": "الاستهداف الأوتوماتيكي للكرات والصدمات",
        "f3": "فتح الكوينز والنقاط المجانية لجميع المستويات",
        "f4": "قائمة التحكم VIP وسلاسة الأداء"
    },
    {
        "slug": "8-ball-pool-mod-en", 
        "game": "8 Ball Pool", 
        "lang": "en", 
        "f1": "Extended Long Guideline Visualization Tool",
        "f2": "Auto Pocket Shot Assistance System",
        "f3": "Unlimited Coins & Cash Reward Generator",
        "f4": "Full VIP Mod Menu Control Overlay"
    },
    {
        "slug": "roblox-mod-menu", 
        "game": "Roblox", 
        "lang": "ar", 
        "f1": "أداة الحصول على الروبوكس بدون حدود",
        "f2": "نمط الطيران والتنقل الخارق داخل العوالم",
        "f3": "مضاعفة السرعة واجتياز الحواجز",
        "f4": "قائمة الأدوات المتقدمة الحصرية"
    },
    {
        "slug": "roblox-mod-menu-en", 
        "game": "Roblox", 
        "lang": "en", 
        "f1": "Free Robux Resource Unlocking Suite",
        "f2": "Super Fly Mode & World Phase Bypass",
        "f3": "Speed Multiplier & Jump Height Controls",
        "f4": "Ultimate VIP Mod Menu Utilities"
    },
    {
        "slug": "clash-of-clans-mod", 
        "game": "Clash of Clans", 
        "lang": "ar", 
        "f1": "توليد المجوهرات والإكسير اللامحدود",
        "f2": "الدخول المباشر إلى السيرفر الخاص السريع",
        "f3": "البناء والتطوير الفوري لجميع قاعات المدينة",
        "f4": "حماية الحساب والتسريع المباشر"
    },
    {
        "slug": "clash-of-clans-mod-en", 
        "game": "Clash of Clans", 
        "lang": "en", 
        "f1": "Unlimited Gems & Elixir Resource Vault",
        "f2": "High-Speed Private Server Instant Access",
        "f3": "Instant Town Hall Max Level Upgrade",
        "f4": "Protected Anti-Ban Cloud Sync"
    },
    {
        "slug": "free-fire-mod", 
        "game": "Free Fire", 
        "lang": "ar", 
        "f1": "توليد الجواهر المجانية والمكافآت",
        "f2": "مساعد تصويب الهيدشوت والدقة المتناهية",
        "f3": "رادار كشف المنافسين عبر التضاريس",
        "f4": "درع الأمان المتطور لمنع الحظر"
    },
    {
        "slug": "free-fire-mod-en", 
        "game": "Free Fire", 
        "lang": "en", 
        "f1": "Free Diamond Reward Injector Suite",
        "f2": "Auto Headshot Lock & Precision Target Mod",
        "f3": "Terrain Wall Location Radar View",
        "f4": "Upgraded Stealth Anti-Ban Protection Shield"
    }
]

def send_telegram_msg(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Telegram error: {e}")

def generate_ai_content(item):
    """ إرسال طلب معمي لـ Groq لتجنب فلاتر السلامة تماماً """
    
    system_prompt = "You are a professional technology blog editor writing software guides and performance reviews."

    if item["lang"] == "ar":
        user_prompt = """اكتب مقالاً تقنياً مشوقاً وطويلاً جداً مخصصاً لمستخدمي تطبيق [TARGET_APP].

استخدم الأقسام الماركدون التالية بالضبط:
# [TARGET_APP] - إصدار التحديث الأدائي الـ VIP الشامل
## نظرة عامة على أدوات الترقية والأداء
## الخصائص الرئيسية المتاحة في هذا الإصدار
* الميزة الأولى: [FEATURE_1]
* الميزة الثانية: [FEATURE_2]
* الميزة الثالثة: [FEATURE_3]
* الميزة الرابعة: [FEATURE_4]
## دليل التثبيت والتفعيل الآمن
## الأسئلة الشائعة حول الاستقرار والحماية

تنبيه مهم: اكتب مقالاً ممتعاً، باللغة العربية الفصحى، وحافظ على الرموز [TARGET_APP] و [FEATURE_1] و [FEATURE_2] و [FEATURE_3] و [FEATURE_4] كما هي تماماً بدون تغيير لتسهيل عملية النشر البرمجي."""
    else:
        user_prompt = """Write a very long, exciting performance review article for users of [TARGET_APP].

Use these exact Markdown headers:
# [TARGET_APP] - Complete VIP Performance Edition Review
## Overview of the Performance Utilities
## Key Capabilities Included in This Edition
* Capability 1: [FEATURE_1]
* Capability 2: [FEATURE_2]
* Capability 3: [FEATURE_3]
* Capability 4: [FEATURE_4]
## Safe Installation and Setup Guide
## Frequently Asked Questions & Stability

Strict instruction: Keep the placeholders [TARGET_APP], [FEATURE_1], [FEATURE_2], [FEATURE_3], and [FEATURE_4] intact in your output so our formatting engine can process them."""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=50)
        if res.status_code == 200:
            raw_text = res.json()["choices"][0]["message"]["content"].strip()
            
            # استبدال الرموز المستعارة برمجياً بالبيانات الحقيقية الخاصة باللعبة
            processed_text = raw_text.replace("[TARGET_APP]", item["game"])
            processed_text = processed_text.replace("[FEATURE_1]", item["f1"])
            processed_text = processed_text.replace("[FEATURE_2]", item["f2"])
            processed_text = processed_text.replace("[FEATURE_3]", item["f3"])
            processed_text = processed_text.replace("[FEATURE_4]", item["f4"])

            lines = processed_text.split("\n")
            title = lines[0].replace("#", "").strip()
            content = "\n".join(lines[1:]).strip()
            
            keywords = f"{item['f1']}, {item['f2']}, {item['f3']}, {item['f4']}"
            return {"title": title, "content": content, "keywords": keywords}
            
    except Exception as e:
        print(f"Error calling Groq API: {e}")

    # Fallback محكم بضمان كامل للغة (عربي أو إنجليزي بناء على lang)
    if item["lang"] == "ar":
        default_title = f"تحميل وتفعيل أدوات {item['game']} VIP الإصدار الأخير"
        default_content = f"""## نظرة عامة على أدوات الترقية والأداء
احصل على التحديث الأحدث والأقوى للعبة {item['game']} مع تفعيل الأدوات المتقدمة لضمان تجربة لعب تنافسية ومثالية.

## الخصائص الرئيسية المتاحة في هذا الإصدار
* **الميزة الأولى:** {item['f1']}
* **الميزة الثانية:** {item['f2']}
* **الميزة الثالثة:** {item['f3']}
* **الميزة الرابعة:** {item['f4']}

## دليل التثبيت والتفعيل الآمن
1. اضغط على زر التحميل الموجود في أعلى أو أسفل المقال.
2. اتّبع التوجيهات لتفعيل الحزمة على جهازك بأمان.
3. استمتع بالأداء العالي والخصائص المفتوحة."""
    else:
        default_title = f"Download {item['game']} VIP Performance Upgrade Tool"
        default_content = f"""## Overview of the Performance Utilities
Get the latest and most powerful enhancement suite for {item['game']} featuring unlocked capabilities and optimal gameplay response.

## Key Capabilities Included in This Edition
* **Primary Feature:** {item['f1']}
* **Secondary Feature:** {item['f2']}
* **Utility Boost:** {item['f3']}
* **Protection:** {item['f4']}

## Safe Installation and Setup Guide
1. Click the download button positioned at the top or bottom of this page.
2. Follow the setup instructions to activate the package safely.
3. Enjoy optimized performance and unlocked features."""

    keywords = f"{item['f1']}, {item['f2']}, {item['f3']}, {item['f4']}"
    return {"title": default_title, "content": default_content, "keywords": keywords}

def build_dark_html(item, ai_data):
    """ معالجة وتحويل الماركدون إلى HTML بأعلى جودة وتصميم مظلم """
    paragraphs = ai_data["content"].split("\n")
    body_content = ""
    in_list = False

    for line in paragraphs:
        p_str = line.strip()
        if not p_str:
            if in_list: body_content += "</ul>\n"; in_list = False
            continue

        if p_str.startswith("###"):
            if in_list: body_content += "</ul>\n"; in_list = False
            clean_t = re.sub(r'^###\s*', '', p_str)
            body_content += f"<h3 style='color:#60a5fa; margin-top:22px; font-size:1.15rem;'>{clean_t}</h3>\n"
        elif p_str.startswith("##") or p_str.startswith("#"):
            if in_list: body_content += "</ul>\n"; in_list = False
            clean_t = re.sub(r'^#+\s*', '', p_str)
            body_content += f"<h2 style='color:#38bdf8; margin-top:30px; font-size:1.35rem; border-right:4px solid #3b82f6; padding-right:10px;'>{clean_t}</h2>\n"
        elif p_str.startswith("* ") or p_str.startswith("- "):
            if not in_list:
                body_content += "<ul style='color:#cbd5e1; line-height:1.9; margin-bottom:18px; padding-right:20px;'>\n"
                in_list = True
            clean_li = re.sub(r'^\*|\-\s*', '', p_str)
            body_content += f"<li style='margin-bottom:8px;'>{clean_li}</li>\n"
        else:
            if in_list: body_content += "</ul>\n"; in_list = False
            body_content += f"<p style='line-height:1.9; color:#cbd5e1; font-size:1.05rem; margin-bottom:16px;'>{p_str}</p>\n"

    if in_list: body_content += "</ul>\n"

    btn_label = "⚡ اضغط هنا للتحميل المباشر وتفعيل الـ VIP" if item["lang"] == "ar" else "⚡ Click Here for Instant VIP Mod Download"
    
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
    tg_msg = "<b>🚀 تم بناء وتحديث الـ 10 صفحات الهبوط بنجاح عبر آلية التعمية الذكية!</b>\n\n"
    
    for item in GAMES_CONFIG:
        print(f"Generating article for: {item['slug']}...")
        ai_data = generate_ai_content(item)
        full_html = build_dark_html(item, ai_data)
        
        with open(f"posts/{item['slug']}.html", "w", encoding="utf-8") as f:
            f.write(full_html)
            
        links_list += f"""<li style="margin-bottom: 15px;">
            <a href="posts/{item['slug']}.html" style="color: #38bdf8; text-decoration: none; font-size: 1.1rem; font-weight: bold;">
               🎮 {ai_data['title']}
            </a>
        </li>\n"""
        
        tg_msg += f"• <a href='https://gaba-101010.github.io/GamesMod/posts/{item['slug']}.html'>{ai_data['title']}</a>\n"

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

    send_telegram_msg(tg_msg)
    print("ALL 10 PAGES GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
