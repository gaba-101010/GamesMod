import os
import requests
from groq import Groq

# --- سحب المفاتيح بأمان تام من خزنة GitHub Secrets ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MONETAG_AD_LINK = os.environ.get("MONETAG_AD_LINK")

# قائمة الألعاب الـ 5 المستهدفة (عربي وإنجليزي)
GAMES_LIST = [
    {"id": "pubg", "name_ar": "ببجي موبايل", "name_en": "PUBG Mobile"},
    {"id": "pool", "name_ar": "8 Ball Pool", "name_en": "8 Ball Pool"},
    {"id": "roblox", "name_ar": "روبلوكس", "name_en": "Roblox"},
    {"id": "clash", "name_ar": "كلاش أوف كلانس", "name_en": "Clash of Clans"},
    {"id": "freefire", "name_ar": "فري فاير", "name_en": "Free Fire"}
]

client = Groq(api_key=GROQ_API_KEY)

def send_telegram_alert(message):
    """إرسال إشعار فوري إلى بوت التليجرام"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def generate_content_with_groq(game_name, lang):
    """توليد محتوى متجدد عبر Groq AI مع دمج الروابط المخفية"""
    if lang == "ar":
        prompt = f"اكتب مقالاً تسويقياً قصيراً جداً ومحفزاً باللغة العربية عن لعبة {game_name} وترقياتها وأدوات التحكم المساعدة. اجعل الأسلوب تشويقياً، وضع رابطاً مخفياً بكلمات زرقاء طبيعية مثل [اضغط هنا للتحميل والبدء]({MONETAG_AD_LINK}) لتوجيه المستخدم. تجنب ذكر أرقام إصدارات ليبقى المقال صالحاً دائماً."
    else:
        prompt = f"Write a very short, engaging promotional article in English about {game_name} mods and control tools. Include a natural anchor text link like [Click here to download and start]({MONETAG_AD_LINK}) to direct the user. Avoid version numbers."

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

print("🚀 جاري توليد وتحديث المحتوى بأمان...")
for game in GAMES_LIST:
    content_ar = generate_content_with_groq(game['name_ar'], "ar")
    content_en = generate_content_with_groq(game['name_en'], "en")
    print(f"تم تحديث لعبة: {game['name_ar']}")

send_telegram_alert("🔔 تم تحديث مقالات المدونة الـ 10 أوتوماتيكيًا وبأمان تام!")
