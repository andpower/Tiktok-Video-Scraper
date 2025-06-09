addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

import cheerio from 'cheerio';

async function handleRequest(request) {
  const url = new URL(request.url);
  if (request.method === 'POST' || (url.pathname === '/download' && url.searchParams.has('url'))) {
    let tiktokUrl;
    if (request.method === 'POST') {
      const form = await request.formData();
      tiktokUrl = form.get('url');
    } else {
      tiktokUrl = url.searchParams.get('url');
    }
    if (!tiktokUrl) {
      return new Response('Missing TikTok url', { status: 400 });
    }

    const tiktokRes = await fetch(tiktokUrl, {
      headers: { 'user-agent': 'Mozilla/5.0' }
    });
    const html = await tiktokRes.text();
    const $ = cheerio.load(html);
    const canonical = $('link[rel="canonical"]').attr('href') || tiktokUrl;

    const apiRes = await fetch('https://www.tikwm.com/api/?url=' + encodeURIComponent(canonical));
    const apiData = await apiRes.json();
    if (apiData.code !== 0 || !apiData.data.play) {
      return new Response('Failed to fetch video', { status: 500 });
    }
    return Response.redirect(apiData.data.play, 302);
  }

  return new Response(`<!DOCTYPE html>
<html><head><title>TikTok Downloader</title></head>
<body>
<h1>TikTok Video Downloader</h1>
<form method="POST">
<input type="url" name="url" placeholder="TikTok link" style="width:80%" required />
<button type="submit">Download</button>
</form>
</body></html>`, {
    headers: { 'content-type': 'text/html;charset=UTF-8' }
  });
}
