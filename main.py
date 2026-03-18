import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# الإعدادات
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# لستة تطبيقاتك الـ 20 من ملفك [cite: 1, 2, 3]
APPS = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Quick ToolsHub", "url": "https://play.google.com/store/apps/details?id=quick.toolshub"}
]

def generate_article():
    app = random.choice(APPS)
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    # طلب مقال فيرال طويل بشروطك [cite: 1, 3]
    data = {
        "model": "llama3-8b-8192",
        "messages": [{
            "role": "user",
            "content": f"Write a VIRAL 800-word SEO article for US readers about trending 2026 US Real Estate or Economy. Use HTML. Include Gold/Silver prices. Promote this app: {app['name']} ({app['url']}). End with a question. Footer: Download 'Luxury Estate Guide' for alerts."
        }],
        "temperature": 0.8
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=60)
        res_json = response.json()
        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        else:
            print(f"API Error Response: {res_json}") # عشان نعرف السبب لو فشل
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def send_mail(content):
    if not content or len(content) < 500:
        print("❌ Content generation failed or too short.")
        return

    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else "US Economic & Real Estate Viral Update"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print(f"✅ SUCCESS: Published {subject}")
    except Exception as e:
        print(f"❌ Mail Error: {e}")

if __name__ == "__main__":
    article = generate_article()
    send_mail(article)
