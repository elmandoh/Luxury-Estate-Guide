import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# إعدادات Groq الصاروخية (تأكد من إضافة GROQ_API_KEY في GitHub Secrets)
API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# قائمة تطبيقاتك الـ 20 لضمان تنوع الروابط 
APPS = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"},
    {"name": "Quick ToolsHub", "url": "https://play.google.com/store/apps/details?id=quick.toolshub"}
    # السكريبت هيختار واحد عشوائياً في كل مرة
]

def generate_viral_article():
    selected_app = random.choice(APPS)
    
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    
    # البرومبت اللي بيجبره يدور على تريند ويكتب 700+ كلمة بشروطك
    data = {
        "model": "llama3-70b-8192", # الموديل الأقوى لضمان عدم التكرار
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional US viral news editor. Write in long-form, engaging, and unique styles."
            },
            {
                "role": "user", 
                "content": f"""Find a trending hot topic in the USA Real Estate or Economy for March 2026 and write a VIRAL article.
                
                Requirements:
                1. Viral H1 Title: Short, punchy, with hashtag, for US audience. (Wrap in <h1>)
                2. Body: Minimum 800 words, high-quality, split into 5+ sections with <h2> tags.
                3. Advice-style Promotion: Recommend this app naturally as an expert tip: {selected_app['name']} ({selected_app['url']}).
                4. Economic Data: A special section for current Gold, Silver, and Currency rates + best stock pick.
                5. Engagement: A provocative question to make readers comment.
                6. Footer: Bold notice to download 'Luxury Estate Guide' app for mobile alerts.
                
                Format: Strictly use HTML (<h1>, <h2>, <p>, <strong>, <ul>)."""
            }
        ],
        "temperature": 1.0, # لأقصى درجة من الحصرية ومنع التكرار
        "max_tokens": 2500
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=120)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def send_to_blogger(content):
    # السكريبت مش هينشر لو المقال طلع قصير (عشان يحمي الـ SEO بتاعك)
    if not content or len(content) < 2000: 
        print("❌ Article too short or generation failed. Skipping to avoid bad content.")
        return

    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"USA Market Alert {random.randint(100, 999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print(f"✅ Success! Published: {subject}")
    except Exception as e:
        print(f"❌ Mail Error: {e}")

if __name__ == "__main__":
    article = generate_viral_article()
    send_to_blogger(article)
