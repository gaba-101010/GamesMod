import os
import json
import requests
from groq import Groq

# 1. سحب المفاتيح بأمان من خزنة GitHub Secrets
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK")

if not GROQ_API_KEY:
    print("ERROR: Missing Groq API Key!")
    exit(1)

client = Groq(api_key=GROQ_API_KEY)

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
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def generate_article(game_name, lang):
    if lang == "ar":
        prompt = f"اكتب مقالاً تسويقياً واحترافياً باللغة العربية عن لعبة {game_name} وتعديلاتها وأدوات المساعدة فيها. ضع رابطاً بكلمات زرقاء طبيعية مثل [اضغط هنا للتحميل الآمن والبدء]({MONETAG_AD_LINK}). تجنب ذكر أرقام إصدارات ليبقى المقال متجدداً ودائماً."
    else:
        prompt = f"Write an engaging promotional article in English about {game_name} mods and control tools. Include a natural anchor link like [Click here for safe download and start]({MONETAG_AD_LINK}). Avoid specific version numbers."

    # استخدام النموذج المعتمد والسريع والمتاح دائماً
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

print("🚀 جاري توليد وتحديث الـ 10 مقالات للمدونة...")

for game in GAMES:
    content_ar = generate_article(game["ar"], "ar")
    content_en = generate_article(game["en"], "en")
    print(f"تم توليد محتوى: {game['en']} / {game['ar']}")

send_telegram_alert("🔔 تم تحديث المقالات الـ 10 في مدونة الألعاب بنجاح عبر البوت!")
