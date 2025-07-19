import requests
import re
from bs4 import BeautifulSoup

def resolve_share_link(url):
    try:
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        print(f"[ℹ️] Redirected to: {final_url}")
        return final_url
    except Exception as e:
        print(f"[❌] Error resolving share link: {e}")
        return None

def extract_uid_from_url(url):
    # Case 1: Direct UID in URL (profile.php?id=...)
    match = re.search(r'profile\.php\?id=(\d+)', url)
    if match:
        return match.group(1)

    # Case 2: Username-based URL (like /zuck)
    match = re.search(r'facebook\.com/([^/?&]+)', url)
    if match:
        username = match.group(1)
        return resolve_username_to_uid(username)

    return None

def resolve_username_to_uid(username):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        url = f"https://mbasic.facebook.com/{username}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find profile.php?id= in the page
        for a in soup.find_all('a', href=True):
            href = a['href']
            match = re.search(r'profile\.php\?id=(\d+)', href)
            if match:
                return match.group(1)

    except Exception as e:
        print(f"[❌] Error resolving username: {e}")
    return None

def main():
    print("🔍 Facebook UID Extractor Tool")
    print("-----------------------------")
    url = input("📎 Enter Facebook Profile/Page/Post URL: ").strip()

    if "facebook.com/share/" in url:
        print("[🔄] Detected share link. Resolving...")
        resolved_url = resolve_share_link(url)
        if resolved_url:
            print(f"[🔗] Using resolved URL: {resolved_url}")
            uid = extract_uid_from_url(resolved_url)
        else:
            uid = None
    else:
        uid = extract_uid_from_url(url)

    if uid:
        print(f"✅ UID Extracted: {uid}")
    else:
        print("❌ Could not extract UID from the given URL.")

if __name__ == "__main__":
    main()