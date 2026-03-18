import os
import smtplib
from email.message import EmailMessage
import google.generativeai as genai

# إعداد Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_luxury_article():
    # برومبت احترافي لجذب الزوار الأمريكيين
    prompt = """
    Write a high-end, SEO-optimized blog post for luxury real estate investors in the USA.
    Topic: Why 2026 is the best year to invest in Florida and Texas mansions.
    - Title should be catchy (e.g., The Billionaire's Guide to 2026 Real Estate).
    - Use professional, engaging English.
    - Include H2 headings and a list of investment benefits.
    - Use HTML tags like <h2>, <p>, and <ul> for formatting.
    """
    response = model.generate_content(prompt)
    return response.text

def send_to_blogger(content):
    # تفاصيل الإيميل من الـ Secrets اللي أنت لسه ضايفها
    msg = EmailMessage()
    msg['Subject'] = "Luxury Estate Investment Trends 2026"  # عنوان الرسالة
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        # الاتصال بسيرفر جوجل لإرسال الإيميل
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print("✅ Success! Article sent to Blogger.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    article = generate_luxury_article()
    send_to_blogger(article)
