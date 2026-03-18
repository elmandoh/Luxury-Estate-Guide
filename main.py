import os
import smtplib
from email.message import EmailMessage

def generate_static_article():
    # مقال جاهز عشان نتأكد إن الإرسال شغال
    content = """
    <h2>Why 2026 is the Best Year for Luxury Investments</h2>
    <p>The US real estate market is booming, especially in Miami and Austin.</p>
    <ul>
        <li>High ROI potential</li>
        <li>Growing demand for mansions</li>
        <li>Tax benefits for investors</li>
    </ul>
    <p>Stay tuned for more updates on luxury living.</p>
    """
    return content

def send_to_blogger(content):
    msg = EmailMessage()
    msg['Subject'] = "Luxury Investment Guide 2026 (Live Now)"
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print("✅ SUCCESS! Article sent to your blog!")
    except Exception as e:
        print(f"❌ Error during sending: {e}")

if __name__ == "__main__":
    # هنبعت مقال ثابت حالاً للتجربة
    article_html = generate_static_article()
    send_to_blogger(article_html)
