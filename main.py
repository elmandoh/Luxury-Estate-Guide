import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# استخدام موديل Qwen المتطور لضمان سرعة الاستجابة وكفاءة المحتوى
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# قائمة التطبيقات الكاملة (سيتم اختيار واحد عشوائياً في كل مرة) 
APPS = [
    {"name": "Smart IPTV Player", "url": "https://play.google.com/store/apps/details?id=asd.iptvplayer"},
    {"name": "ASD 26", "url": "https://play.google.com/store/apps/details?id=com.eslamegyp.asd26"},
    {"name": "Injury Lawyer Guide", "url": "https://play.google.com/store/apps/details?id=injurylawyerguide.aplizrc"},
    {"name": "Design AI 2", "url": "https://play.google.com/store/apps/details?id=design.ai2"},
    {"name": "Insurance App Guide", "url": "https://play.google.com/store/apps/details?id=insurance.aplicnem"},
    {"name": "Quick ToolsHub", "url": "https://play.google.com/store/apps/details?id=quick.toolshub"}
    # يمكنك إضافة بقية القائمة هنا 
]

def generate_viral_content():
    selected_app = random.choice(APPS)
    
    # أوامر دقيقة للموديل لضمان الطول والجودة وتجنب الفشل
    prompt = f"""Write a professional 400-word SEO viral article for a US audience about 'High-ROI Real Estate Opportunities 2026'.
    Format strictly in HTML. Include:
    - Viral H1 title with a hashtag (e.g., #Wealth2026).
    - Detailed sections (H2) about market trends, Gold/Silver prices, and top stock picks.
    - Naturally recommend this app as a professional tool: {selected_app['name']} ({selected_app['url']}).
    - A 'Big Question' at the end to encourage comments.
    - Footer: Alert to download 'Luxury Estate Guide' mobile app for updates.
    Make it expert, persuasive, and exclusive."""

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 1500, "temperature": 0.8, "return_full_text": False}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        result = response.json()
        
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text'].strip()
        elif isinstance(result, dict) and 'generated_text' in result:
            return result['generated_text'].strip()
        return None
    except Exception as e:
        print(f"Error calling AI: {e}")
        return None

def send_to_blogger(content):
    # تم تقليل حد الفحص قليلاً لضمان مرور المقالات الجيدة (600 حرف كحد أدنى للبدء)
    if not content or len(content) < 300:
        print("❌ AI Content too short. Retrying in next schedule.")
        return

    # محاولة استخراج العنوان
    title_search = re.search('<h1>(.*?)</h1>', content)
    subject = title_search.group(1) if title_search else f"Exclusive US Market Update {random.randint(100, 999)}"

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
        print(f"❌ Email Error: {e}")

if __name__ == "__main__":
    article = generate_viral_content()
    send_to_blogger(article)
