/*
© 2025 Matthew Licari. All rights reserved.
This code is part of https://github.com/matthewdotpy/Tiktok-Video-Scraper.

Licensed under the MIT License. See LICENSE file in the project root for full license information.

📜 TikTok Video Link Extractor Script
🔹 Runs in-browser via Selenium to auto-scroll and collect all TikTok video links from a public profile.
*/

// Scrolls page fully and extracts video links after scroll is done
async function autoScrollAndExtract() {
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    const screenHeight = window.screen.height;
    let i = 1;

	// 🖱️ Scroll to load all content
    while (true) {
        window.scrollTo(0, screenHeight * i * 2);
        await delay(2500); // Adjust based on network speed
        const scrollHeight = document.body.scrollHeight;
        if (screenHeight * i > scrollHeight) break;
        i++;
    }

	//https://www.tiktok.com/@codewithvincent

    // 🔗 Scrape video links
    const className = "css-gamknx-DivVideoFeedV2 ecyq5ls0";
    let links = [];

    try {
        const videoFeedDiv = document.querySelector('[data-e2e="user-post-item-list"]');
        const elements = videoFeedDiv.querySelectorAll(
            "#main-content-others_homepage > div > div.css-833rgq-DivShareLayoutMain.e6y15914 > div.css-1qb12g8-DivThreeColumnContainer.eegew6e2 > div > div > div > div > div > a"
        );

        elements.forEach(element => {
            const link = element.getAttribute("href");
            if (link) links.push(link);
        });
    } catch (error) {
        return "Error while extracting links: " + error;
    }

    return links;
}

const links = await autoScrollAndExtract();
return links