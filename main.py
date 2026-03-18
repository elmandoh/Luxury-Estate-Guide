import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# موديل Mistral هو الأفضل حالياً للمقالات الطويلة والحصرية
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# لستة التطبيقات الـ 20 لترويجها بشكل متنوع
APPS = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"},
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"}
    # يمكنك إضافة بقية الـ 20 هنا بنفس التنسيق
]

def generate_viral_article():
    selected_app = random.choice(APPS)
    
    # برومبت تفصيلي لضمان الطول والحصرية والتفاعل
    prompt = f"""<s>[INST] Write a VIRAL 800-word SEO blog post for a US audience.
    Topic: A random trending 2026 economic or luxury real estate event in the USA.
    
    Structure:
    1. Viral Title (H1) with a hashtag.
    2. Deep Analysis (4+ Sections with H2).
    3. Naturally recommend this app: {selected_app['name']} ({selected_app['url']}).
    4. Economic Insight: Latest on Gold, Silver, and a 'Top Stock' pick.
    5. Engagement: A controversial question for comments.
    6. Footer: Remind readers to download the 'Luxury Estate Guide' mobile app.

    Formatting: Use ONLY HTML tags (<h1>, <h2>, <p>, <ul>, <li>, <strong>). [/INST]"""

    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 1200, "temperature": 0.85}}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text'].split("[/INST]")[-1].strip()
        return None
    except Exception as e:
        print(f"AI Failure: {e}")
        return None

def send_to_blogger(content):
    # فحص صارم: لو المقال قصير جداً (أقل من 400 كلمة) مش هيتنشر حفاظاً على جودة المدونة
    if not content or len(content) < 1500: 
        print("❌ Content too short or failed. Skipping to prevent duplicate/thin content.")
        return

    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"USA Market Alert {random.randint(1000, 9999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print(f"✅ Article Published: {subject}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    article = generate_viral_article()
    send_to_blogger(article)
