#!/usr/bin/env python3

import sys
import requests

def fetch_yadisk(url):
    if not url.startswith("http"):
        print("❌ Please provide a valid Yandex.Disk URL.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
    }

    print("🔍 Fetching from:", url)
    r = requests.get(f"https://yadi.sk/d/{url.split('/')[-1]}", headers=headers, allow_redirects=True)

    if r.status_code != 200:
        print(f"❌ Failed to fetch. HTTP {r.status_code}")
        return

    filename = "yadisk_download.zip"
    with open(filename, "wb") as f:
        f.write(r.content)

    print(f"✅ Done! Saved as {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: yadisk-fetch <yandex.disk.url>")
    else:
        fetch_yadisk(sys.argv[1])
