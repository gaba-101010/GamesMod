import os
import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK", "https://google.com")

if not GROQ_API_KEY:
    print("ERROR: Missing GROQ_API_KEY")
    exit(1)

# قائمة الـ 10 صفحات المستقلة
LANDING_PAGES = [
    {"slug": "pubg-mobile-mod", "game": "ببجي موبايل", "lang": "ar", "title": "تحميل وتحديث ببجي موبايل PUBG Mobile (النسخة المطورة)"},
    {"slug": "pubg-mobile-mod-en", "game": "PUBG Mobile", "lang": "en", "title": "Download PUBG Mobile Mod & Update Guide"},
    {"slug": "8-ball-pool-mod", "game": "8 Ball Pool", "lang": "ar", "title": "ترقية وتحديث 8 Ball Pool (الخط الطويل والفلوس)"},
    {"slug": "8-ball-pool-mod-en", "game": "8 Ball Pool", "lang": "en", "title": "8 Ball Pool Long Line & Mod Setup"},
    {"slug": "roblox-mod-menu", "game": "روبلوكس", "lang": "ar", "title": "أدوات وسكريبتات روبلوكس Roblox Mod Menu"},
    {"slug": "roblox-mod-menu-en", "game": "Roblox", "lang": "en", "title": "Roblox Mod Menu & Safety Guide"},
    {"slug": "clash-of-clans-mod", "game": "كلاش أوف كلانس", "lang": "ar", "title": "سيرفرات وترقيات كلاش أوف كلانس Clash of Clans"},
    {"slug": "clash-of-clans-mod-en", "game": "Clash of Clans", "lang": "en", "title": "Clash of Clans Private Server & Mod Guide"},
    {"slug": "free-fire-headshot", "game": "فري فاير", "lang": "ar", "title": "حزم وتحديثات فري فاير Free Fire (Headshot Mod)"},
    {"slug": "free-fire-headshot-en", "game": "Free Fire", "lang": "en", "title": "Free Fire Headshot Sensitivity & Tools Guide"}
]

def generate_article_text(page):
    if page["lang"] == "ar":
        prompt = f"""اكتب مقالاً ترويجياً وتثقيفياً مطولاً واحترافياً يستهدف SEO عن: "{page['title']}".
تحدث عن مميزات التحديث والأمان وتحسين الأداء.
اكتب النص في فقرات وعناوين فرعية فقط بدون أي روابط أو أكواد HTML إطلاقاً."""
    else:
        prompt = f"""Write a comprehensive SEO-optimized guide about: "{page['title']}".
Focus on features, performance tools, and setup instructions.
Output clean plain text with section titles only. Do NOT include any links or HTML tags."""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error fetching from Groq: {e}")
        
    return "محتوى إرشادي لتحديث اللعبة وسرعة التحميل."

def build_html_page(page, article_text):
    paragraphs = article_text.split("\n\n")
    body_content = ""
    for p in paragraphs:
        p_str = p.strip()
        if p_str.startswith("#"):
            clean_t = p_str.replace("#", "").strip()
            body_content += f"<h2 style='color:#1e293b; margin-top:20px;'>{clean_t}</h2>\n"
        elif p_str:
            body_content += f"<p style='line-height:1.8; color:#334155; font-size:1.1rem; margin-bottom:15px;'>{p_str}</p>\n"

    btn_label = "🚀 اضغط هنا للتحميل المباشر والتفعيل" if page["lang"] == "ar" else "🚀 Click Here to Download & Setup Now"
    
    html = f"""<!DOCTYPE html>
<html lang="{page['lang']}" dir="{"rtl" if page['lang']=="ar" else "ltr"}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page['title']}</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 20px; }}
        .box {{ max-width: 800px; margin: 20px auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #0f172a; border-bottom: 3px solid #2563eb; padding-bottom: 10px; font-size: 1.8rem; }}
        .btn-box {{ text-align: center; margin: 30px 0; padding: 20px; background: #eff6ff; border-radius: 10px; border: 1px dashed #2563eb; }}
        .dl-btn {{ display: inline-block; background: #2563eb; color: #ffffff !important; font-weight: bold; font-size: 1.25rem; padding: 16px 36px; border-radius: 8px; text-decoration: none; box-shadow: 0 4px 12px rgba(37,99,235,0.3); }}
        .dl-btn:hover {{ background: #1d4ed8; }}
    </style>
</head>
<body>
    <div class="box">
        <h1>{page['title']}</h1>
        
        <div class="btn-box">
            <a href="{MONETAG_AD_LINK}" target="_blank" class="dl-btn">{btn_label}</a>
        </div>

        <div>
            {body_content}
        </div>

        <div class="btn-box">
            <a href="{MONETAG_AD_LINK}" target="_blank" class="dl-btn">{btn_label}</a>
        </div>
    </div>
</body>
</html>"""
    return html

def main():
    os.makedirs("posts", exist_ok=True)
    
    for page in LANDING_PAGES:
        print(f"Generating page: {page['slug']}...")
        text = generate_article_text(page)
        full_page = build_html_page(page, text)
        
        with open(f"posts/{page['slug']}.html", "w", encoding="utf-8") as f:
            f.write(full_page)

    # توجيه رابط الجذر مباشرة إلى الصفحة الأولى داخل مجلد GamesMod
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f'<meta http-equiv="refresh" content="0; url=posts/{LANDING_PAGES[0]["slug"]}.html">')

    print("DONE: Generated 10 independent landing pages!")

if __name__ == "__main__":
    main()
