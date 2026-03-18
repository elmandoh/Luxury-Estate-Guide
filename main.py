import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# الموديل ده حالياً من أكتر الموديلات استقراراً ومجاني
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# سحب روابط تطبيقاتك من القائمة
APPS_TO_PROMOTE = [
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"}
]

def generate_viral_article():
    # اختيار تطبيق عشوائي لضمان التنوع في كل مقال
    app = random.choice(APPS_TO_PROMOTE)
    
    # برومبت يطلب توليد عنوان عشوائي ومحتوى مختلف كل مرة
    prompt = f"""<s>[INST] Write a unique, expert 700-word SEO article for the US market.
    Topic: Pick a random trending 2026 luxury real estate or economic topic in the USA.
    Make it strictly HTML. Include <h1>, <h2>, and <ul> tags.
    Integrate a recommendation for the app '{app['name']}' with this link: {app['url']}.
    The content MUST be original and not repetitive. [/INST]"""

    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 1000, "temperature": 0.9}}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        result = response.json()
        
        # التأكد إن الـ AI رد فعلاً بمحتوى جديد
        if isinstance(result, list) and 'generated_text' in result[0]:
            content = result[0]['generated_text'].split("[/INST]")[-1].strip()
            return content
        return None # لو الـ AI فشل، نرجع "لا شيء"
    except Exception as e:
        print(f"AI Failed: {e}")
        return None

def send_to_blogger(content):
    # أهم سطر: لو المحتوى فارغ أو مكرر (قصير جداً)، نوقف العملية فوراً
    if not content or len(content) < 300:
        print("❌ AI content failed or too short. Skipping post to avoid duplication.")
        return

    # استخراج العنوان ليكون موضوع الإيميل
    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"USA Real Estate Insights {random.randint(100,999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print(f"✅ SUCCESS: Unique article published: {subject}")
    except Exception as e:
        print(f"❌ SMTP Error: {e}")

if __name__ == "__main__":
    article = generate_viral_article()
    send_to_blogger(article)
