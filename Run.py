import requests
import re
from bs4 import BeautifulSoup

def resolve_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        return response.url
    except requests.RequestException:
        return None

def extract_uid_from_html(html):
    patterns = [
        r'"userID":"(\d+)"',
        r'"entity_id":"(\d+)"',
        r'"fb://profile/(\d+)"',
        r'"pageID":"(\d+)"',
        r'id=(\d+)'  # fallback
    ]

    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    
    # Additional fallback using meta tags
    soup = BeautifulSoup(html, 'html.parser')
    meta = soup.find("meta", attrs={"property": "al:android:url"})
    if meta and "content" in meta.attrs:
        match = re.search(r'id=(\d+)', meta["content"])
        if match:
            return match.group(1)

    return None

def extract_uid_from_url(url):
    resolved_url = resolve_url(url)
    if not resolved_url:
        return None
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(resolved_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return extract_uid_from_html(response.text)
    except requests.RequestException:
        return None

def main():
    print("📎 Enter Facebook Share/Profile/Page/Post URL: ", end="")
    url = input().strip()
    
    uid = extract_uid_from_url(url)
    
    if uid:
        print(f"UID: {uid}")
    else:
        print("❌ UID could not be extracted.")

if __name__ == "__main__":
    main()
