import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from atproto import Client, client_utils # ضيف دي فوق

# الإعدادات
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
            client = Client()
            client.login(acc['handle'], acc['password'])

            # 1. بناء النص والهاشتاجات بشكل تفاعلي
            tb = client_utils.TextBuilder()
            tb.text(f"🚨 {title}\n\n")
            tb.tag("#RealEstate", "RealEstate") # الهاشتاج هينور أزرق هنا
            tb.text(" ")
            tb.tag("#USA", "USA")
            tb.text("\n\nRead more here:")

            # 2. إرسال البوست مع الـ Embed (المعاينة) والـ TextBuilder
            client.send_post(
                text=tb,
                embed=models.AppBskyEmbedExternal.Main(
                    external=models.AppBskyEmbedExternal.External(
                        uri=link,
                        title=title,
                        description="Latest US Real Estate & Economy Updates 2026",
                    )
                )
            )
            print(f"✅ Shared with Blue Tags on {acc['handle']}")
        except Exception as e: 
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    title, link = get_latest_post()
    last_link = ""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f: last_link = f.read().strip()

    if link and link != last_link:
        post_to_bsky(title, link)
        with open(CACHE_FILE, "w") as f: f.write(link)
