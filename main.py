import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

# الموديل الأسرع والأكثر استقراراً حالياً
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# قائمة تطبيقاتك الـ 20 كاملة لترويج متنوع 
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
    selected_app = random.choice(APPS)
    
    # البرومبت اللي بيطلع مقال "وحش"
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an expert US Real Estate and Economy journalist. Write a viral, 800-word SEO article in HTML format.
    <|start_header_id|>user<|end_header_id|>
    Topic: High-impact 2026 US Economy or Real Estate trends.
    Structure: Viral H1 title with hashtag, 5 sections with H2, Economic Brief (Gold/Silver/Stocks), Engagement Question, and a footer alert for the 'Luxury Estate Guide' app.
    Promotion: Recommend this app naturally: {selected_app['name']} ({selected_app['url']}).
    <|start_header_id|>assistant<|end_header_id|>"""

    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 1000, "temperature": 0.7, "top_p": 0.9}}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        result = response.json()
        if isinstance(result, list):
            return result[0]['generated_text'].split("<|end_header_id|>")[-1].strip()
        return None
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def send_to_blogger(content):
    # فحصنا الذكي عشان المحتوى المكرر
    if not content or len(content) < 800:
        print("❌ AI content failed or too short. Skipping.")
        return

    title_match = re.search('<h1>(.*?)</h1>', content)
    subject = title_match.group(1) if title_match else f"Market Report {random.randint(100, 999)}"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
        smtp.send_message(msg)
    print(f"✅ Article Published: {subject}")

if __name__ == "__main__":
    article = generate_viral_article()
    send_to_blogger(article)
