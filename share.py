import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# الإعدادات من السيكرتس
BSKY_ACCOUNTS = [
    {"handle": os.getenv("BSKY_HANDLE_1"), "password": os.getenv("BSKY_PASSWORD_1")},
    {"handle": os.getenv("BSKY_HANDLE_2"), "password": os.getenv("BSKY_PASSWORD_2")}
]

BLOG_RSS_URL = "https://luxuryestateguide.blogspot.com/feeds/posts/default?alt=rss"
CACHE_FILE = "last_post.txt"

def get_latest_post():
    try:
        response = requests.get(BLOG_RSS_URL, timeout=30)
        root = ET.fromstring(response.content)
        item = root.find('.//item')
        if item is not None:
            return item.find('title').text, item.find('link').text
    except: return None, None

def post_to_bsky(title, link):
    for acc in BSKY_ACCOUNTS:
        if not acc['handle'] or not acc['password']: continue
        try:
            session = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession",
                                    json={"identifier": acc['handle'], "password": acc['password']}).json()
            headers = {"Authorization": f"Bearer {session['accessJwt']}"}
            post_data = {
                "repo": session['did'], "collection": "app.bsky.feed.post",
                "record": {
                    "text": f"🚨 New Viral Post: {title}\n\nRead more:\n{link}",
                    "createdAt": datetime.utcnow().isoformat() + "Z"
                }
            }
            requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord", json=post_data, headers=headers)
            print(f"✅ Shared on {acc['handle']}")
        except Exception as e: print(f"❌ Error: {e}")

if __name__ == "__main__":
    title, link = get_latest_post()
    
    # التأكد لو الرابط اتنشر قبل كدا ولا لا
    last_link = ""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f: last_link = f.read().strip()

    if link and link != last_link:
        post_to_bsky(title, link)
        # حفظ الرابط الجديد في الذاكرة
        with open(CACHE_FILE, "w") as f: f.write(link)
    else:
        print("☕ No new articles found since last share.")
