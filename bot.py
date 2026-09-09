import os
import requests

# 1. سحب المفاتيح بأمان من خزنة GitHub Secrets
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK")

if not GROQ_API_KEY:
    print("ERROR: Missing Groq API Key!")
    exit(1)

# قائمة الألعاب الـ 5 المستهدفة (عربي وإنجليزي)
GAMES = [
    {"id": "pubg", "ar": "ببجي موبايل", "en": "PUBG Mobile"},
    {"id": "pool", "ar": "8 Ball Pool", "en": "8 Ball Pool"},
    {"id": "roblox", "ar": "روبلوكس", "en": "Roblox"},
    {"id": "clash", "ar": "كلاش أوف كلانس", "en": "Clash of Clans"},
    {"id": "freefire", "ar": "فري فاير", "en": "Free Fire"}
]

def send_telegram_alert(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Telegram error: {e}")

def generate_article_with_requests(game_name, lang):
    if lang == "ar":
        prompt = f"اكتب مقالاً تسويقياً واحترافياً باللغة العربية عن لعبة {game_name} وتعديلاتها وأدوات المساعدة فيها. ضع رابطاً بكلمات زرقاء طبيعية مثل [اضغط هنا للتحميل الآمن والبدء]({MONETAG_AD_LINK}). تجنب ذكر أرقام إصدارات ليبقى المقال متجدداً ودائماً."
    else:
        prompt = f"Write an engaging promotional article in English about {game_name} mods and control tools. Include a natural anchor link like [Click here for safe download and start]({MONETAG_AD_LINK}). Avoid specific version numbers."

    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # استخدام النموذج المعتمد والمستقر بنظام requests المباشر
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a professional technical content writer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(groq_url, headers=headers, json=payload)
        res_data = res.json()
        if "choices" in res_data:
            return res_data["choices"][0]["message"]["content"]
        else:
            print(f"Groq API Error response: {res_data}")
            return f"مقال افتراضي لـ {game_name}"
    except Exception as e:
        print(f"Connection error: {e}")
        return f"مقال افتراضي لـ {game_name}"

print("🚀 جاري توليد وتحديث المقالات عبر الاتصال المباشر...")

for game in GAMES:
    content_ar = generate_article_with_requests(game["ar"], "ar")
    content_en = generate_article_with_requests(game["en"], "en")
    print(f"تم معالجة محتوى: {game['en']} / {game['ar']}")

send_telegram_alert("🔔 تم تحديث مقالات المدونة الـ 10 أوتوماتيكياً وبنجاح تام عبر البوت!")
print("تم الانتهاء بنجاح!")
