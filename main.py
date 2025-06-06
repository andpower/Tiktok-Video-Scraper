"""
© 2025 Matthew Licari. All rights reserved.
This code is part of https://github.com/matthewdotpy/Tiktok-Video-Scraper.

Licensed under the MIT License. See LICENSE file in the project root for full license information.

🔹 Script to extract and download TikTok videos from a public profile without watermarks
🔹 Uses TikMate for no-watermark downloads and Selenium for TikTok scraping
"""

import os
import sys
import time
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from colorama import Fore
import undetected_chromedriver as uc

def update_gui(index, total, current_url, download_link=None, title=None, status=None):
    """Console GUI updater with progress bar and step feedback."""
    os.system("cls" if os.name == "nt" else "clear")

    print(f"📋 Task: Attempting to Download Video {index}/{total}")
    print("—" * 64)
    print(f"🔍 Processing: {current_url}")

    if download_link:
        print(f"🎯 Found download link: {download_link}")

    if title:
        print(f"📥 Downloading: {title}")

    if status == "success":
        print(Fore.GREEN + f"✅ Downloaded: {title}" + Fore.RESET)
    elif status == "fail":
        print(Fore.RED + f"❌ Failed to download: {title or current_url}" + Fore.RESET)

    # Progress bar
    bar_len = 60
    filled = int((index / total) * bar_len)
    bar = "|" * filled + "." * (bar_len - filled)
    percent = int((index / total) * 100)
    print()
    print(f"💫 Progress ({index}/{total})")
    print(f"{bar} ({percent}%)")


def sanitize_filename(name: str) -> str:
    """Remove unsafe characters from video titles for file naming."""
    return re.sub(r'[\\/*?:"<>|]', "", name)


def find_tiktoks_videos(profile_url: str) -> list:
    """Scrape a user's TikTok page and return a list of video URLs."""
    print(Fore.CYAN + f"🔍 Getting video links for: {profile_url}" + Fore.RESET)

    options = uc.ChromeOptions()
    #options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = uc.Chrome(options=options)
    browser.set_script_timeout(300)  # ⏱️ Wait up to 5 minutes for long scrolling


    try:
        browser.get(profile_url)
        time.sleep(3)

        with open("script.js", "r", encoding="UTF-8") as file:
            script = file.read()

        urls_to_download = browser.execute_script(script)

        if not urls_to_download:
            print(Fore.RED + "❌ No links found." + Fore.RESET)
            return []

        print(f"🎯 Found video links: {len(urls_to_download)}")
        return urls_to_download

    except Exception as e:
        print(Fore.RED + f"❌ Error scraping TikTok profile: {e}" + Fore.RESET)
        return []
    finally:
        browser.quit()


def download_with_tikmate(url: str, index: int, total: int):
    """Download a TikTok video via TikMate's frontend using Selenium."""
    update_gui(index, total, current_url=url)

    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = uc.Chrome(options=options)

    try:
        browser.get("https://tikmate.app")
        time.sleep(3)

        input_box = browser.find_element("id", "url")
        input_box.clear()
        input_box.send_keys(url)

        submit_btn = browser.find_element("id", "submit-button")
        submit_btn.click()

        time.sleep(6)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        download_link_tag = soup.find(id="download-hd")

        if not download_link_tag:
            update_gui(index, total, current_url=url, status="fail")
            return

        download_link = download_link_tag.get("href")
        update_gui(index, total, current_url=url, download_link=download_link)

        video_title_tag = soup.select_one("#result > div.flex-container > div.flex-item.text")
        video_title = sanitize_filename(video_title_tag.get_text(strip=True) if video_title_tag else "video")

        os.makedirs("videos", exist_ok=True)
        output_path = f"videos/{video_title}.mp4"

        update_gui(index, total, current_url=url, download_link=download_link, title=video_title)
        mp4_file = urlopen("https://tikmate.app/" + download_link)
        with open(output_path, "wb") as f:
            while True:
                chunk = mp4_file.read(4096)
                if not chunk:
                    break
                f.write(chunk)

        update_gui(index, total, current_url=url, download_link=download_link, title=video_title, status="success")

    except Exception as e:
        update_gui(index, total, current_url=url, status="fail")
        print(Fore.RED + f"Exception: {e}" + Fore.RESET)
    finally:
        browser.quit()

# 🔽 Start Download Process
if __name__ == "__main__":
    print("🎯 TikTok Video Scraper")
    print("1️⃣  Paste a TikTok video link to download a video")
    print("2️⃣  Paste a TikTok profile link to scrape and download all videos")
    mode = input("👉 Choose an option (1 or 2): ").strip()

    if mode == "1":
        while(True):
            video_url = input("\n📋 Paste the TikTok video link:\n").strip()
            download_with_tikmate(video_url, 1, 1)
            mode = input("❓ Would you like to download another? (y/n) ").strip()
            if mode != "y":	break

    elif mode == "2":
        profile = input("\n📋 Paste the TikTok profile link:\n").strip()
        urls = find_tiktoks_videos(profile)

        if not urls:
            sys.exit(1)

        total = len(urls)
        for i, link in enumerate(urls, start=1):
            update_gui(i, total, current_url=link)
            try:
                download_with_tikmate(link, i, total)
            except Exception:
                update_gui(i, total, current_url=link, status="fail")
            time.sleep(1)

    else:
        print(Fore.RED + "❌ Invalid selection. Exiting." + Fore.RESET)
        sys.exit(1)
        
    print()
    print("🌟 If you liked this project or helped you, please consider starring it on GitHub!")
    print("🔗 https://github.com/matthewdotpy/Tiktok-Video-Scraper")
    input(Fore.GREEN + "😀 Thanks for using!" + Fore.RESET)
