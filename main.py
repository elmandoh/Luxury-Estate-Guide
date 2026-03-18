import os
import smtplib
import requests
from email.message import EmailMessage

# إعداد البديل (Hugging Face)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def generate_ai_article():
    prompt = "<s>[INST] Write a 500-word SEO blog post about 'Investing in USA Luxury Real Estate 2026'. Use HTML tags for headings and lists. Target high ROI keywords. [/INST]"
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 1000, "temperature": 0.7}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        # استخراج النص الناتج
        result = response.json()
        if isinstance(result, list):
            content = result[0]['generated_text'].split("[/INST]")[-1]
            return content
        return None
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def send_to_blogger(content):
    if not content: return
    
    msg = EmailMessage()
    msg['Subject'] = "2026 USA Luxury Real Estate Trends"
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = os.getenv("BLOGGER_EMAIL")
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            smtp.send_message(msg)
        print("✅ Success! AI Article Published without Visa!")
    except Exception as e:
        print(f"Sending Error: {e}")

if __name__ == "__main__":
    article = generate_ai_article()
    send_to_blogger(article)
