import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# إعداد الـ API الخاص بـ Hugging Face (البديل المجاني)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# قائمة التطبيقات المستخرجة من ملفك للترويج لها 
APPS_TO_PROMOTE = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2 (Luxury Home Design)", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"},
    {"name": "BPS Productivity (Business Tracking)", "url": "https://play.google.com/store/apps/details?id=ap3756437.bps"}
]

def generate_viral_article():
    # اختيار تطبيقين عشوائياً لضمان عدم التكرار 
    selected_apps = random.sample(APPS_TO_PROMOTE, 2)
    
    prompt = f"""<s>[INST] Write a VIRAL, high-impact 700-word SEO article for the US market. 
    Topic: A major trending economic or real estate event in the USA (e.g., Fed interest rates, luxury market shifts, or housing crisis solutions).
    
    Requirements:
    1. Viral Title: Short, punchy, click-bait (but honest), including a trending hashtag (e.g., #RealEstate2026 #USWealth).
    2. Content: Professional, exclusive-feeling analysis divided into 5+ organized sections.
    3. Integration: Naturally recommend these 2 apps as expert tools: 
       - {selected_apps[0]['name']} ({selected_apps[0]['url']})
       - {selected_apps[1]['name']} ({selected_apps[1]['url']})
    4. Economic Brief: A dedicated section with the latest on Gold, Silver, Currency trends, and a 'Top Stock/Crypto Pick' recommendation.
    5. Engagement: Add a provocative 'Big Question' at the end to force comments.
    6. Footer: A notification to download the 'Luxury Estate Guide' mobile app for real-time alerts.
    
    Format: Use strictly HTML (<h1>, <h2>, <p>, <strong>, <ul>). [/INST]"""

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 1200, "temperature": 0.8}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        return result[0]['generated_text'].split("[/INST]")[-1]
    except:
        return None

def send_to_blogger(content):
    if not content: return
    
    # استخراج العنوان الفيرال ليكون موضوع الإيميل
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else "Urgent: US Economic & Real Estate Alert"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print("✅ Viral AI Article Published Successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    article = generate_viral_article()
    send_to_blogger(article)
