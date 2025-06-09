# 🎥 TikTok Video Scraper (No Watermark)

A simple Cloudflare Worker that downloads TikTok videos without watermarks using the public Tikwm API.

> ⚡ Built by [@matthewdotpy](https://github.com/matthewdotpy)

---

## 📦 Features
- 🔍 Fetches TikTok pages and parses metadata using `cheerio`
- 💧 Retrieves clean video URLs via the Tikwm API
- 🖱️ Provides a small HTML form for easy downloads
- ✅ Deployable to Cloudflare Workers using `wrangler`

---

## 🚀 Installation

```bash
git clone https://github.com/matthewdotpy/Tiktok-Video-Scraper.git
cd Tiktok-Video-Scraper
npm install
```

## 🛠️ Usage
Start the worker locally:
```bash
npx wrangler dev
```
Then open the provided URL in your browser and paste a TikTok link into the form.

## 🌐 Deployment
Configure your Cloudflare account in `wrangler.toml` and run:
```bash
npx wrangler publish
```

## 🌟 Star the Repo
If you liked this project or it helped you, please ⭐ the repo 😀
