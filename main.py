import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# إعدادات Groq (تأكد من وضع GROQ_API_KEY في السيكرتس)
API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# قائمة تطبيقاتك الـ 20 (سيختار منها واحد عشوائي لكل مقال) [cite: 1, 2, 3]
APPS = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "Quick ToolsHub", "url": "https://play.google.com/store/apps/details?id=quick.toolshub"},
    {"name": "ASD 26", "url": "https://play.google.com/store/apps/details?id=com.eslamegyp.asd26"},
    {"name": "NoteEye", "url": "https://play.google.com/store/apps/details?id=noteeye.ayzi"}
    # يمكنك إضافة بقية الروابط هنا [cite: 1, 2, 3]
]

def generate_viral_content():
    selected_app = random.choice(APPS)
    
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    
    # البرومبت الجديد: حددنا له النيتش وتركنا له اختيار الموضوع الساخن
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system", 
                "content": "You are a top-tier US financial journalist. Your goal is to find a trending, high-traffic niche topic in US Real Estate, Luxury Living, or US Economy and write about it to drive viral clicks."
            },
            {
                "role": "user", 
                "content": f"""Generate a unique, viral SEO blog post based on a CURRENT hot topic in the US Real Estate or Economy niche.
                
                Strict Requirements:
                1. Viral Title: Short, punchy, attracts US readers, includes a trending hashtag. (Wrap in <h1>)
                2. Length: Minimum 800 words, organized into professional sections with <h2>.
                3. App Promotion: Naturally recommend this app as a helpful tool: {selected_app['name']} ({selected_app['url']}).
                4. Economic Brief: Include a dedicated section with current Gold, Silver, and Currency trends + a stock/crypto recommendation.
                5. Engagement: End with a provocative question and ask readers to comment.
                6. Footer: Add a bold notice: 'Download the Luxury Estate Guide app on your phone for instant real estate alerts and economic tips.'
                
                Format everything in clean HTML."""
            }
        ],
        "temperature": 1.0, # زيادة العشوائية لمنع التكرار تماماً
        "max_tokens": 2000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_to_blogger(content):
    if not content or len(content) < 1500: # التأكد من جودة وطول المقال
        print("❌ Content too short or failed. Skipping.")
        return

    # استخراج العنوان ليكون موضوع الإيميل
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"US Market Alert {random.randint(100, 999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print(f"✅ Viral Article Published: {subject}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    article = generate_viral_content()
    send_to_blogger(article)
