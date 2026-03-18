import os
import requests
from datetime import datetime

# إعدادات Bluesky من GitHub Secrets
BSKY_ACCOUNTS = [
    {"handle": os.getenv("BSKY_HANDLE_1"), "password": os.getenv("BSKY_PASSWORD_1")},
    {"handle": os.getenv("BSKY_HANDLE_2"), "password": os.getenv("BSKY_PASSWORD_2")}
]

# رابط التغذية (RSS) لمدونتك
BLOG_RSS_URL = "https://luxuryestateguide.blogspot.com/feeds/posts/default?alt=rss"

def get_latest_blog_post():
    """جلب عنوان ورابط آخر مقال تم نشره فعلياً على المدونة"""
    try:
        response = requests.get(BLOG_RSS_URL, timeout=30)
        # استخراج أول مقال من الـ RSS
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        item = root.find('.//item')
        if item is not None:
            title = item.find('title').text
            link = item.find('link').text
            return title, link
    except Exception as e:
        print(f"Error fetching RSS: {e}")
    return None, None

def post_to_bluesky(title, link):
    """نشر تفاصيل المقال الجديد على حسابات Bluesky"""
    for acc in BSKY_ACCOUNTS:
        if not acc['handle'] or not acc['password']:
            continue
        try:
            # 1. تسجيل الدخول
            session = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession",
                                    json={"identifier": acc['handle'], "password": acc['password']}).json()
            headers = {"Authorization": "Bearer " + session['accessJwt']}
            
            # 2. إنشاء المنشور
            post_text = f"🔥 New Update: {title}\n\nRead the full article here:\n{link}\n\n#RealEstate #USA #Economy"
            post_data = {
                "repo": session['did'],
                "collection": "app.bsky.feed.post",
                "record": {
                    "text": post_text,
                    "createdAt": datetime.utcnow().isoformat() + "Z"
                }
            }
            requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord", json=post_data, headers=headers)
            print(f"✅ Successfully shared on Bluesky: {acc['handle']}")
        except Exception as e:
            print(f"❌ Error sharing on {acc['handle']}: {e}")

if __name__ == "__main__":
    print("Checking for new posts to share...")
    title, link = get_latest_blog_post()
    if title and link:
        # هنا يمكنك إضافة نظام بسيط للتأكد أن المقال لم ينشر من قبل (مثلاً حفظ الرابط في ملف نصي)
        post_to_bluesky(title, link)
    else:
        print("No new post found to share.")
