import os
import random
import requests

# 1. إعداد المفاتيح والروابط من البيئة
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK", "https://google.com")

# 2. قائمة المواضيع والألعاب
GAMES = [
    {"slug": "pubg-mobile-lag-fix", "title": "حل مشكلة اللاج والتقطيع في ببجي موبايل PUBG Mobile"},
    {"slug": "free-fire-headshot-sensitivity", "title": "أفضل إعدادات الحساسية للهيدشوت في فري فاير Free Fire"},
    {"slug": "gta-san-andreas-cheats-android", "title": "جميع كلمات سر وجراند ثفت أوتو سان أندرياس للأندرويد"},
    {"slug": "call-of-duty-mobile-fps-boost", "title": "رفع الفريمات إلى 60 و 90 FPS في كول أوف ديوتي موبايل"},
    {"slug": "roblox-free-robux-guide", "title": "دليل الأمان والمصداقية في لعبة روبلوكس Roblox"},
    {"slug": "eafc-mobile-coins-guide", "title": "طرق جمع الكوينز وبناء فريق قوي في FC Mobile"}
]

def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error from Groq API: {res.status_code} - {res.text}")
        return None

def generate_article(game):
    prompt = f"""
    اكتب مقالاً إرشادياً مفصلاً واحترافياً باللغة العربية عن: "{game['title']}".
    اجعل المقال يحتوي على:
    1. مقدمة مشوقة.
    2. نصائح خطوة بخطوة وحلول عملية.
    3. قسم تحذيري أو إرشادات مهمة للحفاظ على أمان الحساب.
    4. خاتمة مشجعة.
    
    ملاحظة مهمة جداً: اكتب المقال بنص عادي مع استخدام العناوين الرئيسة والفرعية، ولا تضف أي روابط أو أكواد HTML إطلاقاً.
    """
    
    content = ask_groq(prompt)
    if not content:
        content = "عذراً، لم نتمكن من جلب المحتوى حالياً. يرجى المحاولة لاحقاً."

    # تحويل النص القادم من الذكاء الاصطناعي إلى فقرات HTML
    paragraphs = content.split("\n\n")
    html_body = ""
    for p in paragraphs:
        if p.strip().startswith("#"):
            clean_title = p.replace("#", "").strip()
            html_body += f"<h2 style='color: #1e293b; margin-top: 25px;'>{clean_title}</h2>\n"
        else:
            html_body += f"<p style='line-height: 1.8; color: #334155; font-size: 1.1rem; margin-bottom: 15px;'>{p.strip()}</p>\n"

    # قليب تصميم الصفحة HTML بالكامل وضمان عمل الرابط كاملاً
    full_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{game['title']}</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 30px auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        h1 {{
            color: #0f172a;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
            font-size: 1.8rem;
        }}
        .btn-container {{
            text-align: center;
            margin: 35px 0;
            padding: 20px;
            background-color: #eff6ff;
            border-radius: 10px;
            border: 1px dashed #2563eb;
        }}
        .download-btn {{
            display: inline-block;
            background-color: #2563eb;
            color: #ffffff !important;
            font-weight: bold;
            font-size: 1.2rem;
            padding: 15px 35px;
            border-radius: 8px;
            text-decoration: none;
            transition: background 0.3s ease;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
        }}
        .download-btn:hover {{
            background-color: #1d4ed8;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 20px;
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{game['title']}</h1>
        
        <!-- زر الإعلان والتحميل الأزرق الواضح والأنك -->
        <div class="btn-container">
            <p style="margin-top:0; font-size:1rem; color:#475569;">اضغط على الزر أدناه للذهاب للرابط المطلوب مباشرة:</p>
            <a href="{MONETAG_AD_LINK}" target="_blank" class="download-btn">🚀 اضغط هنا للتحميل / الانتقال للرابط</a>
        </div>

        <!-- محتوى المقال -->
        <div class="content">
            {html_body}
        </div>

        <!-- زر إعلان ثاني في نهاية المقال -->
        <div class="btn-container">
            <a href="{MONETAG_AD_LINK}" target="_blank" class="download-btn">📥 تحميل الملفات والملحقات الآن</a>
        </div>

        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin-top: 30px;">
        <a href="../index.html" class="back-link">⬅ العودة إلى الصفحة الرئيسية</a>
    </div>
</body>
</html>
"""
    return full_html

def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def main():
    os.makedirs("posts", exist_ok=True)
    
    # اختيار لعبة عشوائية
    game = random.choice(GAMES)
    
    # توليد المقال بتنسيق HTML
    html_content = generate_article(game)
    file_path = f"posts/{game['slug']}.html"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Generated: {file_path}")
    
    # تحديث الصفحة الرئيسية index.html
    update_index_page()

    # إرسال إشعار لتليجرام
    site_url = f"https://gaba-101010.github.io/posts/{game['slug']}.html"
    telegram_msg = f"<b>تم نشر مقال جديد بنجاح! 🎉</b>\n\n<b>العنوان:</b> {game['title']}\n\n<b>الرابط:</b> {site_url}"
    send_telegram(telegram_msg)

def update_index_page():
    posts_files = [f for f in os.listdir("posts") if f.endswith(".html")]
    
    links_html = ""
    for pf in posts_files:
        title = pf.replace(".html", "").replace("-", " ").title()
        links_html += f"""
        <li style="margin-bottom: 12px; background: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
            <a href="posts/{pf}" style="color: #2563eb; text-decoration: none; font-weight: bold; font-size: 1.1rem;">
                📌 {title}
            </a>
        </li>
        """
        
    index_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدونة الألعاب والشروحات</title>
    <style>
        body {{ font-family: system-ui, sans-serif; background: #f8fafc; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; }}
        h1 {{ color: #0f172a; border-bottom: 2px solid #2563eb; padding-bottom: 10px; }}
        ul {{ list-style: none; padding: 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 دليل وشروحات الألعاب</h1>
        <p>اختر المقال الذي تريد قراءته:</p>
        <ul>
            {links_html}
        </ul>
    </div>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

if __name__ == "__main__":
    main()
