import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# قائمة تطبيقاتك
APPS = [
    {"name": "Luxury Estate Guide", "url": "https://play.google.com/store/apps/details?id=luxury.estateguide"},
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"}
]

# كلمات مفتاحية متخصصة في العقارات والاستثمار لضمان القبول
KEYWORDS = [
    "Luxury Real Estate Trends 2026", "US Housing Market Forecast", 
    "High-End Property Investment", "Smart Home Technology in Luxury Estates", 
    "Mortgage Rates for Premium Buyers", "Global Luxury Housing Demand"
]

def generate_pro_article():
    app = random.choice(APPS)
    kw = random.sample(KEYWORDS, 2)
    
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    # برومبت جديد يضمن استخراج العنوان بشكل منفصل واحترافي
    prompt = f"""Write a 900-word SEO expert article. 
    Topic: {kw[0]} and {kw[1]}.

    STRICT STRUCTURE:
    1. The first line MUST be the title (Catchy & Human-like, NO hashtags).
    2. Then write [SEP].
    3. Then write a 150-char Meta Description.
    4. Then write the full article in clean HTML (starting with <h2>, NOT <h1>).
    5. Use 5+ sections with <h2> tags.
    6. Include an HTML table for market stats.
    7. Include this EXACT button: 
       <div style='text-align: center; margin: 20px;'><a href='{app['url']}' style='background-color: #28a745; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;'>Get the {app['name']} Now</a></div>
    """

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6 # تقليل الحرارة لزيادة الواقعية والجودة
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
        return response.json()['choices'][0]['message']['content']
    except: return None

def send_to_blogger(content):
    if not content or len(content) < 1500: return

    # منطق جديد لاستخراج العنوان بدقة
    if "[SEP]" in content:
        subject, body = content.split("[SEP]", 1)
        subject = subject.strip().replace("Title:", "").replace("\"", "")
    else:
        # حل احتياطي إذا فشل التقسيم
        subject = f"Exclusive Insights: Future of {KEYWORDS[0]} in 2026"
        body = content

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(body.strip(), subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print(f"✅ Success: Published with Title: {subject}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    article = generate_pro_article()
    send_to_blogger(article)
