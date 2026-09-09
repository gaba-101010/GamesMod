import os
import json
import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK")
GITHUB_TOKEN = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
REPO_NAME = "gaba-101010/GamesMod" # اسم المستودع حقك

if not GROQ_API_KEY:
    print("ERROR: Missing Groq API Key!")
    exit(1)

# قائمة الـ 10 مقالات المستهدفة (5 ألعاب × لغتين)
GAMES = [
    {"slug": "pubg-ar", "name": "ببجي موبايل", "lang": "ar"},
    {"slug": "pubg-en", "name": "PUBG Mobile", "lang": "en"},
    {"slug": "pool-ar", "name": "8 Ball Pool", "lang": "ar"},
    {"slug": "pool-en", "name": "8 Ball Pool", "lang": "en"},
    {"slug": "roblox-ar", "name": "روبلوكس", "lang": "ar"},
    {"slug": "roblox-en", "name": "Roblox", "lang": "en"},
    {"slug": "clash-ar", "name": "كلاش أوف كلانس", "lang": "ar"},
    {"slug": "clash-en", "name": "Clash of Clans", "lang": "en"},
    {"slug": "freefire-ar", "name": "فري فاير", "lang": "ar"},
    {"slug": "freefire-en", "name": "Free Fire", "lang": "en"},
]

def send_telegram_alert(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Telegram error: {e}")

def generate_article_content(game_name, lang):
    if lang == "ar":
        prompt = f"""
اكتب مقالاً احترافياً وتسويقياً مطولاً باللغة العربية يستهدف محركات البحث (SEO) عن تحميل النسخة المعدلة والمطورة من لعبة {game_name} والمميزات الإضافية فيها.
الشروط:
1. العنوان يجب أن يكون جذاباً ويحتوي على كلمات مفتاحية قوية للبحث.
2. تحدث عن مميزات التعديل وأدوات التحكم والتحسينات المتاحة.
3. في نهاية المقال، ضع فقرة واضحة لتحميل الملف برابط مباشر، واجعل رابط التحميل مصمماً بكلمات بارزة مثل: [تحميل الملف الآمن والتفعيل المباشر الآن]({MONETAG_AD_LINK}).
4. اكتب المقال بصيغة Markdown نظيفة.
"""
    else:
        prompt = f"""
Write a comprehensive and engaging SEO-optimized article in English about downloading the modded version and control tools for {game_name}.
Requirements:
1. Create an attractive SEO-friendly title.
2. Discuss the features, mods, and performance enhancements.
3. At the end, include a clear download section with a high-converting anchor link like: [Click Here for Safe Download and Direct Setup]({MONETAG_AD_LINK}).
4. Output in clean Markdown format.
"""

    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post(groq_url, headers=headers, json=payload)
        res_data = res.json()
        if "choices" in res_data:
            return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq error: {e}")
    
    return f"# {game_name}\n\n[تحميل الملف الآمن]({MONETAG_AD_LINK})"

print("🚀 جاري توليد ونشر الـ 10 مقالات أوتوماتيكياً...")

# إنشاء مجلد للمقالات لو مو موجود
os.makedirs("posts", exist_ok=True)

index_links_ar = []
index_links_en = []

for game in GAMES:
    print(f"جاري معالجة: {game['slug']}...")
    markdown_content = generate_article_content(game["name"], game["lang"])
    
    # حفظ المقال كملف منفصل في مجلد posts/
    file_path = f"posts/{game['slug']}.html"
    
    # تحويل بسيط لـ HTML عشان يفتحم الزوار مباشرة بدون مشاكل عرض
    html_page = f"""<!DOCTYPE html>
<html lang="{game['lang']}">
<head>
    <meta charset="UTF-8">
    <title>{game['name']} - التحديث الأخير</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.8; background: #f9f9f9; color: #333; padding: 20px; max-width: 800px; margin: auto; }}
        h1, h2 {{ color: #007bff; }}
        .download-btn {{ display: block; background: #28a745; color: white; text-align: center; padding: 15px; text-decoration: none; font-size: 20px; font-weight: bold; border-radius: 8px; margin: 30px 0; }}
        .download-btn:hover {{ background: #218838; }}
        a {{ color: #007bff; }}
        .back {{ margin-top: 40px; display: block; }}
    </style>
</head>
<body>
    {markdown_content.replace(f'({MONETAG_AD_LINK})', f'("{MONETAG_AD_LINK}" class="download-btn")')}
    <br><hr>
    <a class="back" href="../index.html">⬅ العودة إلى الرئيسية / Back to Home</a>
</body>
</html>
"""
    
    # حفظ الملف محلياً في المستودع
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_page)
        
    if game["lang"] == "ar":
        index_links_ar.append(f'<li><a href="posts/{game["slug"]}.html">تحميل وتحديث {game["name"]} (نسخة مطورة)</a></li>')
    else:
        index_links_en.append(f'<li><a href="posts/{game["slug"]}.html">Download & Update {game["name"]} (Modded)</a></li>')

# تحديث صفحة البداية index.html لتربط على الـ 10 مقالات بشكل مرتب
index_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>بوابة أدوات وترقيات الألعاب الاحترافية</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Tahoma, sans-serif; line-height: 1.8; background: #121212; color: #e0e0e0; padding: 20px; max-width: 800px; margin: auto; }}
        h1, h2 {{ color: #00ffcc; text-align: center; }}
        ul {{ list-style-type: square; background: #1e1e1e; padding: 20px 40px; border-radius: 10px; }}
        li {{ margin: 15px 0; }}
        a {{ color: #ff007f; text-decoration: none; font-weight: bold; font-size: 18px; }}
        a:hover {{ text-decoration: underline; color: #00ffcc; }}
        .desc {{ text-align: center; color: #aaa; margin-bottom: 30px; }}
    </style>
</head>
<body>
    <h1>🚀 بوابة أدوات وترقيات الألعاب الاحترافية</h1>
    <p class="desc">المنصة الشاملة لأحدث حزم المساعدة والتعديلات للألعاب الشهيرة. اختر لعبتك وابدأ التحديث الفوري.</p>
    
    <h2>🔥 المقالات والنسخ المتاحة (عربي):</h2>
    <ul>
        {"".join(index_links_ar)}
    </ul>

    <h2>🔥 Available Game Mods & Guides (English):</h2>
    <ul>
        {"".join(index_links_en)}
    </ul>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("[-] تم إنشاء جميع الملفات وتحديث الصفحة الرئيسية بنجاح!")
send_telegram_alert("🔔 تم توليد ونشر الـ 10 مقالات بصفحاتها المستقلة وبروابط الإعلانات بنجاح تام!")
