import re
import requests
from bs4 import BeautifulSoup

def resolve_final_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        if response.history:
            print(f"[ℹ️] Redirected to: {response.url}")
        return response.url
    except requests.exceptions.RequestException as e:
        print(f"[!] Error resolving URL: {e}")
        return None

def extract_uid_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for entity_id
    match = re.search(r'"entity_id":"(\d+)"', html)
    if match:
        return match.group(1)
    
    # Try meta property if entity_id fails
    meta = soup.find("meta", property="al:android:url")
    if meta and meta.get("content"):
        match = re.search(r'fb://profile/(\d+)', meta["content"])
        if match:
            return match.group(1)
    
    return None

def get_facebook_uid(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[!] Failed to access URL, status code: {response.status_code}")
            return None
        return extract_uid_from_html(response.text)
    except Exception as e:
        print(f"[!] Exception occurred: {e}")
        return None

def main():
    print("🔍 Facebook UID Extractor Tool")
    print("-----------------------------")
    input_url = input("📎 Enter Facebook Profile/Page/Post URL: ").strip()

    if "/share/" in input_url:
        print("[🔄] Detected share link. Resolving...")
        final_url = resolve_final_url(input_url)
        if not final_url:
            print("❌ Could not resolve the shared URL.")
            return
        input_url = final_url

    print(f"[🔗] Using resolved URL: {input_url}")
    uid = get_facebook_uid(input_url)

    if uid:
        print(f"✅ Facebook UID: {uid}")
    else:
        print("❌ Could not extract UID from the given URL.")

if __name__ == "__main__":
    main()
