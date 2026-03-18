import os
import smtplib
import requests
import random
import re
from email.message import EmailMessage

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY")

# القائمة الكاملة من ملفك لضمان الترويج لجميع منتجاتك 
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
    
    # برومبت هجومي لضمان الروابط والطول والتنسيق
    prompt = f"""Write a VIRAL 900-word SEO blog post for US readers. 
    Topic: High-impact 2026 US Real Estate or Economic Trend.
    
    STRICT STRUCTURE:
    1. Viral H1 Title with #HashTag.
    2. Compelling Introduction.
    3. 5 Detailed Sections (H2) with expert analysis.
    4. PROMOTION: You MUST include this clickable HTML link as a professional recommendation: <a href='{app['url']}'>{app['name']}</a>. Make it look like expert advice.
    5. DATA TABLE: An HTML table showing current Gold, Silver, and Top Stock prices.
    6. ENGAGEMENT: A controversial question for the comments section.
    7. FOOTER: A bold red alert: 'STAY UPDATED! Download our Luxury Estate Guide mobile app now for real-time notifications.'
    
    Format: Use ONLY professional HTML tags."""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.85
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=120)
        return response.json()['choices'][0]['message']['content']
    except: return None

def send_to_blogger(content):
    if not content or len(content) < 2000: return

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
    print(f"✅ Success: {subject}")

if __name__ == "__main__":
    article = generate_viral_article()
    send_to_blogger(article)
