import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# الإعدادات المحدثة لعام 2026
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# القائمة الكاملة لتطبيقاتك الـ 20 من ملفك 
APPS = [
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "ASD 26", "url": "https://play.google.com/store/apps/details?id=com.eslamegyp.asd26"},
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Quick ToolsHub", "url": "https://play.google.com/store/apps/details?id=quick.toolshub"},
    {"name": "Smart IPTV Viewer", "url": "https://play.google.com/store/apps/details?id=smart.iptvviewer"},
    {"name": "Fast Lite Web Browser", "url": "https://play.google.com/store/apps/details?id=fast.litewebbrowser"},
    {"name": "NoteEye", "url": "https://play.google.com/store/apps/details?id=noteeye.ayzi"},
    {"name": "QR App Muq", "url": "https://play.google.com/store/apps/details?id=qr.appmuq"},
    {"name": "K-Cafe Finder", "url": "https://play.google.com/store/apps/details?id=kcafe.finder"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "BPS Productivity", "url": "https://play.google.com/store/apps/details?id=ap3756437.bps"},
    {"name": "TV App Ape", "url": "https://play.google.com/store/apps/details?id=tv.appape"},
    {"name": "QR Scanner 377", "url": "https://play.google.com/store/apps/details?id=qr.scanner377"},
    {"name": "SmartSync Hub", "url": "https://play.google.com/store/apps/details?id=smartsync.hub"},
    {"name": "ConnectSphere", "url": "https://play.google.com/store/apps/details?id=connectsphere.aczh"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"},
    {"name": "Digital CV Share", "url": "https://play.google.com/store/apps/details?id=digital.cvshare"},
    {"name": "Al Hilal Fans", "url": "https://play.google.com/store/apps/details?id=al.hilalfans"},
    {"name": "Toolify Daily Monitor", "url": "https://play.google.com/store/apps/details?id=toolify.dailytoolsusagemonitor"},
    {"name": "DHO Productivity", "url": "https://play.google.com/store/apps/details?id=app3514831.dho"}
]

def generate_viral_article():
    app = random.choice(APPS)
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    # استخدام الموديل الجديد لضمان العمل
    data = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [
            {"role": "system", "content": "You are a US Economy & Real Estate viral journalist. Write uniquely."},
            {"role": "user", "content": f"Find a trending US Real Estate topic for March 2026. Write a VIRAL 800-word SEO article in HTML. Include Gold/Silver prices. Promote this app naturally: {app['name']} ({app['url']}). End with a question. Footer: Download 'Luxury Estate Guide' for alerts."}
        ],
        "temperature": 0.9
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=90)
        res_json = response.json()
        return res_json['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_to_blogger(content):
    if not content or len(content) < 1500: # حماية من المحتوى الضعيف
        return

    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Viral Market Update {random.randint(100, 999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
        smtp.send_message(msg)
    print(f"✅ SUCCESS: {subject}")

if __name__ == "__main__":
    article = generate_viral_article()
    send_to_blogger(article)
