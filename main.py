import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# الإعدادات
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")
PINTEREST_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")
BOARD_ID = os.getenv("PINTEREST_BOARD_ID")

# تطبيقاتك الـ 20 (تم التأكد من عمل الموديل الجديد معها)
APPS = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"}
    # أضف البقية هنا..
]

def post_to_pinterest(title, link):
    """دالة لنشر المقال كـ Pin على بينترست لجلب زوار أمريكان"""
    if not PINTEREST_TOKEN: return
    
    url = "https://api.pinterest.com/v5/pins"
    headers = {
        "Authorization": f"Bearer {PINTEREST_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "link": link,
        "title": title,
        "description": f"Check out the latest US market update: {title} #RealEstate #Finance",
        "board_id": BOARD_ID,
        "media_source": {
            "source_type": "image_url",
            "url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?q=80&w=1000&auto=format&fit=crop" # صورة افتراضية عقارية
        }
    }
    try:
        requests.post(url, json=data, headers=headers)
        print("✅ Pinned to Pinterest!")
    except: pass

def generate_pro_article():
    app = random.choice(APPS)
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    # استخدام الموديل الشغال حالياً llama-3.3-70b-versatile
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"Write a VIRAL 900-word SEO article for US readers. Topic: 2026 US Economic Trend. Include a green HTML button for: {app['name']} ({app['url']}). Format in HTML."}],
        "temperature": 0.8
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
        return response.json()['choices'][0]['message']['content']
    except: return None

def send_to_blogger(content):
    if not content or len(content) < 2000: return

    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Market Update {random.randint(100, 999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print(f"✅ Published: {subject}")
        # بعد النشر، نقوم بعمل الـ Pin
        post_to_pinterest(subject, "https://yourblog.blogspot.com")
    except: pass

if __name__ == "__main__":
    article = generate_pro_article()
    send_to_blogger(article)
